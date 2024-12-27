import os
import logging
from typing import List, Dict, Any
from botasaurus.decorators_utils import create_directory_if_not_exists
# from botasaurus.decorators import print_filenames
from botasaurus import bt
from src.fields import Fields
from src.utils import kebab_case, sort_dict_by_keys, unicode_to_ascii

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for file paths
OUTPUT_DIR = "output"
JSON_DIR = "json"
CSV_DIR = "csv"

# Utility Functions
def create_folders(base_path: str, subfolders: List[str]):
    """
    Create base folder and subfolders if they do not exist.

    Args:
        base_path (str): Base folder path.
        subfolders (List[str]): List of subfolder names to create inside base_path.
    """
    create_directory_if_not_exists(base_path)
    for subfolder in subfolders:
        create_directory_if_not_exists(os.path.join(base_path, subfolder))

# Transformation Functions
def transform_about(about_list: List[Dict[str, Any]]) -> Dict[str, str]:
    """Transform about list into a dictionary."""
    transformed_about = {}
    for item in about_list:
        enabled_options = [opt['name'] for opt in item.get('options', []) if opt['enabled']]
        disabled_options = [opt['name'] for opt in item.get('options', []) if not opt['enabled']]
        transformed_about[f"{item['id']}_enabled"] = ", ".join(enabled_options)
        transformed_about[f"{item['id']}_disabled"] = ", ".join(disabled_options)
    return transformed_about

def featured_question_to_string(data: Dict[str, Any]) -> str:
    """Format featured question data into a string."""
    question = data.get("question", "No Question")
    answer = data.get("answer", "No Answer")
    question_ago = data.get("question_ago", "")
    answer_ago = data.get("answer_ago", "")
    return f"Question: {question} ({question_ago})\n\nAnswer: {answer} ({answer_ago})"

def competitors_to_string(data: List[Dict[str, Any]]) -> str:
    """Format competitors data into a string."""
    return '\n'.join(
        f"Name: {comp.get('name', 'No Name')}\nlink: {comp.get('link', 'No Link')}\nReviews: {comp.get('reviews', 'No Reviews')} reviews\n"
        for comp in data
    ) if isinstance(data, list) else str(data)

def popular_times_to_string(data: Dict[str, Any]) -> str:
    """Format popular times data into a string."""
    formatted_output = ""
    for day, times in data.items():
        formatted_output += f"{day}:\n"
        for time_slot in times:
            time_label = time_slot.get("time_label", "No Time Label")
            popularity_percentage = time_slot.get("popularity_percentage", 0)
            popularity_description = time_slot.get("popularity_description", "No description")
            formatted_output += f"    {time_label}: {popularity_percentage}% | {popularity_description}\n"
        formatted_output += "\n"
    return formatted_output.strip()

def most_popular_times_to_string(data: List[Dict[str, Any]]) -> str:
    """Format most popular times data into a string."""
    formatted_strings = []
    time_labels = []
    for el in data:
        average_popularity = el.get("average_popularity", "No Average Popularity")
        time_label = el.get("time_label", "No Time Label")
        time_labels.append(time_label)
        formatted_strings.append(f"Time Label: {time_label}\nAverage Popularity: {average_popularity}\n")
    return ', '.join(time_labels) + '\n---\n' + '\n'.join(formatted_strings).strip()

def format_field_data(field: str, data: Any) -> Any:
    """Handle field-specific formatting."""
    if field == Fields.FEATURED_QUESTION:
        return featured_question_to_string(data)
    elif field == Fields.COMPETITORS:
        return competitors_to_string(data)
    elif field == Fields.POPULAR_TIMES:
        return popular_times_to_string(data)
    elif field == Fields.MOST_POPULAR_TIMES:
        return most_popular_times_to_string(data)
    elif field == Fields.ORDER_ONLINE_LINKS:
        return '\n'.join(link['link'] for link in data)
    elif field == Fields.RESERVATIONS:
        return '\n'.join(link['link'] for link in data)
    elif field == Fields.EMAILS:
        return ', '.join(email['value'] for email in data)
    elif field == Fields.PHONES:
        return ', '.join(phone['value'] for phone in data)
    elif field == Fields.CATEGORIES:
        return ', '.join(data or [])
    elif field == Fields.REVIEW_KEYWORDS:
        return ', '.join(keyword['keyword'] for keyword in data)
    elif field == Fields.COORDINATES:
        return f"{data['latitude']},{data['longitude']}"
    elif field == Fields.CLOSED_ON:
        return ', '.join(data) if isinstance(data, list) else data
    elif field == Fields.HOURS:
        return '\n'.join(f"{day['day']}: {', '.join(day['times'])}" for day in data)
    elif field == Fields.ABOUT:
        return transform_about(data)
    return data

def transform_places(places: List[Dict[str, Any]], fields: List[str]) -> List[Dict[str, Any]]:
    """Transform raw places data into a structured format."""
    transformed_places = []
    for place in places:
        transformed_place = {}
        for field in fields:
            if field in place:
                transformed_place[field] = format_field_data(field, place[field])
        transformed_places.append(transformed_place)
    return transformed_places

# File Creation Functions
def write_json(path: str, data: Any):
    """Write data to a JSON file."""
    bt.write_json(data, path, False)


def write_csv(path: str, data: List[Dict[str, Any]]):
    """Write data to a CSV file."""
    bt.write_csv(data, path, False)

# Main Output Creation
def create_outputs(places: List[Dict[str, Any]], fields: List[str], query: str):
    """
    Create all output files for the given places and fields.

    Args:
        places (List[Dict[str, Any]]): Raw places data.
        fields (List[str]): Fields to include in the output.
        query (str): Search query for naming output files.
    """
    query_kebab = kebab_case(query)
    base_path = os.path.join(OUTPUT_DIR, query_kebab)
    create_folders(base_path, [JSON_DIR, CSV_DIR])

    # File paths
    json_path = os.path.join(base_path, JSON_DIR, f"places-{query_kebab}.json")
    csv_path = os.path.join(base_path, CSV_DIR, f"places-{query_kebab}.csv")

    # Transform and write data
    transformed_data = transform_places(places, fields)
    write_json(json_path, transformed_data)
    write_csv(csv_path, transformed_data)

    logging.info(f"Files written: {json_path}, {csv_path}")

# Example Entry Point
def write_output(query: str, places: List[Dict[str, Any]], fields: List[str]):
    """Entry point for creating output files."""
    try:
        create_outputs(places, fields, query)
    except Exception as e:
        logging.error(f"Error creating outputs: {e}")
