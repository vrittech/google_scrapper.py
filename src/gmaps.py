from src import scraper
from botasaurus import bt
from botasaurus.string_utils import ht
from botasaurus.request import request
from botasaurus.task import task
from botasaurus.cache import DontCache
from src.sort_filter import filter_places, sort_dict_by_keys
from src.write_output import write_output
from src.sort_filter import filter_places, sort_places

from typing import List, Optional, Dict

from .cities import Cities
from .lang import Lang
from .category import Category

from .fields import ALL_FIELDS, ALL_SOCIAL_FIELDS, DEFAULT_SOCIAL_FIELDS, Fields, DEFAULT_FIELDS, DEFAULT_FIELDS_WITHOUT_SOCIAL_DATA, ALL_FIELDS_WITHOUT_SOCIAL_DATA
from .social_scraper import FAILED_DUE_TO_CREDITS_EXHAUSTED, FAILED_DUE_TO_NOT_SUBSCRIBED, FAILED_DUE_TO_UNKNOWN_ERROR, get_website_contacts, scrape_social


def create_place_data(query, max, lang, geo_coordinates, zoom, links):
    place_data = {
            "query": query,
            "max": max,
            "lang": lang,
            "geo_coordinates": geo_coordinates,
            "zoom": zoom, 
            "links":links
        }
    return place_data


def create_social_scrape_data(places, key):
    social_scrape_data = []

    for place in places:
        if place.get('website'):
            social_data = {
                "place_id": place["place_id"],
                "website": place["website"], 
                "key":key,
            }
            social_scrape_data.append(social_data)

    return social_scrape_data


def clean_social(social_details):
    success, credits_exhausted, not_subscribed, unknown_error = [], [], [], []

    for detail in social_details:
        if detail.get("error") is None:
            success.append(detail)
        elif detail["error"] == FAILED_DUE_TO_CREDITS_EXHAUSTED:
            credits_exhausted.append(detail)
        elif detail["error"] == FAILED_DUE_TO_NOT_SUBSCRIBED:
            not_subscribed.append(detail)
        elif detail["error"] == FAILED_DUE_TO_UNKNOWN_ERROR:
            unknown_error.append(detail)

    return success, credits_exhausted, not_subscribed, unknown_error

def print_social_errors(credits_exhausted, not_subscribed, unknown_error):
    # print(credits_exhausted)
    if credits_exhausted:
        print(f"Could not get social details for {len(credits_exhausted)} places due to credit exhaustion. Please consider upgrading your plan by visiting https://rapidapi.com/Chetan11dev/api/website-social-scraper-api/pricing to continue scraping social details.")

    if not_subscribed:
        print(f"Could not get social details for {len(not_subscribed)} places as you are not subscribed to Website Social Scraper. Please subscribe to a free plan by visiting https://rapidapi.com/Chetan11dev/api/website-social-scraper-api/pricing to scrape social details.")

    if unknown_error:
        print(f"Could not get social details for {len(unknown_error)} places due to Unknown Error.")

def get_credits_exhausted_data():
  msg = "Could not get social detail due to credit exhaustion. Please consider upgrading your plan by visiting https://rapidapi.com/Chetan11dev/api/website-social-scraper-api/pricing to continue scraping social details."
  EMPTY_SOCIAL_DATA = {
      'emails': [msg],
      'phones': [msg],
      'linkedin': msg,
      'twitter': msg,
      'facebook': msg,
      'youtube': msg,
      'instagram': msg,
      'tiktok': msg,
      'github': msg,
      'snapchat': msg,
      'pinterest': msg,
  }
  return EMPTY_SOCIAL_DATA

def get_not_subscribed_data():
  msg = "Could not get social detail as you are not subscribed to Website Social Scraper. Please subscribe to a free plan by visiting https://rapidapi.com/Chetan11dev/api/website-social-scraper-api/pricing to scrape social details."
  
  EMPTY_SOCIAL_DATA = {
      'emails': [msg],
      'phones': [msg],
      'linkedin': msg,
      'twitter': msg,
      'facebook': msg,
      'youtube': msg,
      'instagram': msg,
      'tiktok': msg,
      'github': msg,
      'snapchat': msg,
      'pinterest': msg,
  }
  return EMPTY_SOCIAL_DATA


def get_unknown_error_data():
  msg = "Could not get social detail due to an unknown error."
  
  EMPTY_SOCIAL_DATA = {
      'emails': [msg],
      'phones': [msg],
      'linkedin': msg,
      'twitter': msg,
      'facebook': msg,
      'youtube': msg,
      'instagram': msg,
      'tiktok': msg,
      'github': msg,
      'snapchat': msg,
      'pinterest': msg,
      
  }
  return EMPTY_SOCIAL_DATA

def get_null_data():
  msg = None
  
  EMPTY_SOCIAL_DATA = {
      'emails': [],
      'phones': [],
      'linkedin': msg,
      'twitter': msg,
      'facebook': msg,
      'youtube': msg,
      'instagram': msg,
      'tiktok': msg,
      'github': msg,
      'snapchat': msg,
      'pinterest': msg,
  }
  return EMPTY_SOCIAL_DATA
def get_empty_data(msg = "Provide API Key"):
  
  EMPTY_SOCIAL_DATA = {
      'emails': [msg],
      'phones': [msg],
      'linkedin': msg,
      'twitter': msg,
      'facebook': msg,
      'youtube': msg,
      'instagram': msg,
      'tiktok': msg,
      'github': msg,
      'snapchat': msg,
      'pinterest': msg,
  }
  return EMPTY_SOCIAL_DATA

def merge_credits_exhausted(places, social_details):
    for place in places:
        found_social_detail = next((detail for detail in social_details if detail['place_id'] == place['place_id']), None)
        if found_social_detail:
            place.update(get_credits_exhausted_data())

    return places


def merge_not_subscribed(places, social_details):
    for place in places:
        found_social_detail = next((detail for detail in social_details if detail['place_id'] == place['place_id']), None)
        if found_social_detail:
            place.update(get_not_subscribed_data())

    return places


def merge_unknown(places, social_details):
    for place in places:
        found_social_detail = next((detail for detail in social_details if detail['place_id'] == place['place_id']), None)
        if found_social_detail:
            place.update(get_unknown_error_data())

    return places

def merge_social(places, social_details, should_scrape_socials):
    for place in places:
        found_social_detail = next((detail for detail in social_details if detail['place_id'] == place['place_id']), None)
        if found_social_detail:
            place.update(found_social_detail['data'])
        else:
            if place.get("website") is not None:
                if should_scrape_socials:
                    place.update(get_empty_data("Failed to get social details. Please check the logs for more information."))
                else:
                    place.update(get_empty_data())
            else: 
                place.update(get_null_data())

    return places

printed = False
def print_rvs_message(hl):
    global printed
    if not printed:
        pass
        # if "en" not in hl:
        # REMOVE CAN BE ADDED TO README LATER OR MAYBE FIXED?
        #     print("You have choes to scrape detailed reviews by using scrape_reviews, the published_at_date, response_from_owner_date is only provided in English Language. So published_at_date, response_from_owner_date will be null." ) 
        printed = True

def create_reviews_data(places, reviews_max, reviews_sort, lang):
    reviews_data = []
    
    chosen_lang = lang if lang else "en"
    
    print_rvs_message(chosen_lang)
    
    for place in places:
        n_reviews=place["reviews"]
        if reviews_max is None: 
                max_r = n_reviews
        else:
                max_r = min(reviews_max, n_reviews)        
        review_data = {
            "place_id": place["place_id"],
            "link": place["link"],
            "max": max_r,
            "reviews_sort": reviews_sort,
            "lang": chosen_lang, 
        }
        reviews_data.append(review_data)

    return reviews_data

def merge_reviews(places, reviews):
    for place in places:
        # Find the reviews for the current place based on place_id
        found_review = next((review for review in reviews if review['place_id'] == place['place_id']), None)

        # Add the 'reviews' from the found review to the place, or an empty list if no review is found
        place['detailed_reviews'] = found_review['reviews'] if found_review else []

    return places

default_addition = {
    "description":"*****",
    "is_spending_on_ads":"*****",
    "competitors":"*****",
    "website":"*****",
    "can_claim":"*****",
    "owner":"*****",
    "featured_image":"*****",
    "workday_timing":"*****",
    'is_temporarily_closed' : "*****", 
    'is_permanently_closed' : "*****", 
    "closed_on":"*****",
    "phone":"*****",
    "review_keywords":"*****",
    "status":"*****",
    "price_range":"*****",
    "reviews_per_rating":"*****",
    "featured_question":"*****",
    "reviews_link":"*****",
    "coordinates":"*****",
    "plus_code":"*****",
    "detailed_address":"*****",
    "time_zone":"*****",
    "cid":"*****",
    "data_id":"*****",
    "about":"*****",
    "images":"*****",
    "hours":"*****",
    "most_popular_times":"*****",
    "popular_times":"*****",
    "menu":"*****",
    "reservations":"*****",
    "order_online_links":"*****",
}


def process_result(key, scrape_reviews, reviews_max, reviews_sort,  lang, should_scrape_socials,places_obj):
      places = places_obj["places"]
      query = places_obj["query"]

      cleaned_places = places
        
        # 2. Scrape Emails
      if should_scrape_socials:
          places_with_websites = filter_places(cleaned_places, {"has_website": True})
          social_data = create_social_scrape_data(places_with_websites, key)
          social_details =  bt.remove_nones(scrape_social(social_data, ))
          success, credits_exhausted, not_subscribed, unknown_error = clean_social(social_details)
          print_social_errors(credits_exhausted, not_subscribed, unknown_error)
          cleaned_places = merge_social(cleaned_places, success, should_scrape_socials)
          cleaned_places = merge_credits_exhausted(cleaned_places, credits_exhausted)
          cleaned_places = merge_not_subscribed(cleaned_places, not_subscribed)
          cleaned_places = merge_unknown(cleaned_places, unknown_error)
      else:
          cleaned_places = merge_social(cleaned_places, [], should_scrape_socials)
          
        # 3. Scrape Reviews
      if scrape_reviews:
          placed_with_reviews = filter_places(cleaned_places, {"min_reviews": 1})
          reviews_data = create_reviews_data(placed_with_reviews, reviews_max, reviews_sort, lang)
          reviews_details =  scraper.scrape_reviews(reviews_data,)
            # print_social_errors
          cleaned_places = merge_reviews(cleaned_places, reviews_details)
      else:
        cleaned_places = merge_reviews(cleaned_places, [])
  
      result_item = {"query": query, "places": cleaned_places}
      return result_item


def merge_places(places):
    merged_places = []
    for place_group in places:
        merged_places.extend(place_group['places'])
    return merged_places


@request()
def google_maps_scraper(_, data):
    
    key = data['api_key']
    lang = data['lang']
    max_results = data['max_results']
    scrape_reviews = data['enable_reviews_extraction']
    reviews_max = data['max_reviews']
    reviews_sort = data['reviews_sort']
    geo_coordinates = data['coordinates']
    zoom = data['zoom_level']
    query = data['query']
    links = data.get('links',[])

    place_data = create_place_data(query,  max_results, lang, geo_coordinates, zoom, links)
    places_obj = scraper.scrape_places(place_data)
    print("************",places_obj)
    if places_obj is None:
        return DontCache([])
    should_scrape_socials = key  
    result_item = process_result(key, scrape_reviews, reviews_max, reviews_sort, lang, should_scrape_socials, places_obj)
    
    pc = result_item["places"]
    
    if key:
        socialMedia = ['emails', 'phones', 'linkedin', 'twitter', 'facebook', 'youtube', 'instagram', 'pinterest', 'github', 'snapchat', 'tiktok',]
    else:
        socialMedia = []
    all_fs = ['place_id', 'name', 'description', 'is_spending_on_ads', 'reviews', 'competitors', 'website', 'can_claim', ] +socialMedia + ['owner', 'featured_image', 'main_category', 'categories', 'rating', 'workday_timing', 'is_temporarily_closed',  'is_permanently_closed', 'closed_on', 'phone', 'address', 'review_keywords', 'link', 'status', 'price_range', 'reviews_per_rating', 'featured_question', 'reviews_link', 'coordinates', 'plus_code', 'detailed_address', 'time_zone', 'cid', 'data_id', 'about', 'images', 'hours', 'most_popular_times', 'popular_times', 'menu', 'reservations', 'order_online_links', 'featured_reviews', 'detailed_reviews', 'query']
    pc = [sort_dict_by_keys({**x, **default_addition}, all_fs) for x in pc]
    final_result = pc
    
    # fiels sorting is necessary as well
    return final_result

@task()
def website_contacts_scraper(data):
    websites = data["websites"]
    # Assuming get_website_contacts is a function that returns a list of tuples (item, index)
    items = get_website_contacts(websites, metadata=data["api_key"])
    output = []
    has_seen_error = False
    # Enumerate items to get both item and its index
    for index, item in enumerate(items):
        if item.get('error'):
            # Append error information for each field
            output.append({
                "website": websites[index],
                "emails": item['error'],
                "phones": item['error'],
                "linkedin": item['error'],
                "twitter": item['error'],
                "facebook": item['error'],
                "youtube": item['error'],
                "instagram": item['error'],
                "github": item['error'],
                "snapchat": item['error'],
                "tiktok": item['error']
            })
            has_seen_error = True
        else:
            # Spread the 'data' dictionary into the output dictionary
            x = item['data']
            output.append({"website": websites[index], **x})

    # Return a special object to prevent caching in case of error
    if has_seen_error:
        return DontCache(output)
    return output

def determine_fields(fields, should_scrape_socials, scrape_reviews):
      if fields == Gmaps.ALL_FIELDS:
          if should_scrape_socials:
            fields = ALL_FIELDS 
          else: 
            fields = ALL_FIELDS_WITHOUT_SOCIAL_DATA 
      elif fields == Gmaps.DEFAULT_FIELDS:              
          if should_scrape_socials:
            fields = DEFAULT_FIELDS
          else: 
            fields = DEFAULT_FIELDS_WITHOUT_SOCIAL_DATA

      if scrape_reviews:
        if Fields.DETAILED_REVIEWS not in fields:
                fields.append(Fields.DETAILED_REVIEWS)
      else: 
        if Fields.DETAILED_REVIEWS in fields:
            fields.remove(Fields.DETAILED_REVIEWS)
          
    # Check if should_scrape_socials is True and there are no occurrences of any ALL_SOCIAL_FIELDS in fields
      if should_scrape_socials:
        if not any(field in fields for field in ALL_SOCIAL_FIELDS):
            fields.extend(DEFAULT_SOCIAL_FIELDS)
      else:
        # Remove any occurrences of ALL_SOCIAL_FIELDS from fields
        fields = [field for field in fields if field not in ALL_SOCIAL_FIELDS]
    #   print(fields)
      return fields



class Gmaps:
  SORT_DESCENDING = "desc"
  SORT_ASCENDING = "asc"
  SORT_BY_REVIEWS_DESCENDING = [Fields.REVIEWS, SORT_DESCENDING]
  SORT_BY_RATING_DESCENDING = [Fields.RATING, SORT_DESCENDING]
  SORT_BY_NAME_ASCENDING = [Fields.NAME, SORT_ASCENDING]

  SORT_BY_NOT_HAS_WEBSITE = [Fields.WEBSITE, False]
  SORT_BY_HAS_WEBSITE = [Fields.WEBSITE, True]

  SORT_BY_IS_SPENDING_ON_ADS = [Fields.IS_SPENDING_ON_ADS, True]

  SORT_BY_NOT_HAS_LINKEDIN = [Fields.LINKEDIN, True]

  SORT_BY_NOT_HAS_PHONE = [Fields.PHONE, False]
  SORT_BY_HAS_PHONE = [Fields.PHONE, True]

  DEFAULT_SORT = [SORT_BY_REVIEWS_DESCENDING, SORT_BY_HAS_WEBSITE, SORT_BY_NOT_HAS_LINKEDIN, SORT_BY_IS_SPENDING_ON_ADS]
  ALL_REVIEWS = None

  MOST_RELEVANT = "most_relevant" 
  NEWEST  = "newest"
  HIGHEST_RATING = "highest_rating" 
  LOWEST_RATING= "lowest_rating"

  ALL_FIELDS = "all"

  DEFAULT_FIELDS = "default"

  Cities  = Cities()
  Lang  = Lang()
  Category  = Category()
  Fields = Fields()
  
  @staticmethod
  def places(queries: List[str],
             min_reviews: Optional[int] = None,
             max_reviews: Optional[int] = None,
             is_spending_on_ads: Optional[bool] = False,
             category_in: Optional[List[str]] = None,
             
             has_website: Optional[bool] = None,
             
             has_phone: Optional[bool] = None,
             min_rating: Optional[float] = None,
             max_rating: Optional[float] = None,
             
             sort: Optional[List[str]] = DEFAULT_SORT,
             
             max: Optional[int] = None,
             
             key: Optional[str] = None,
             
             convert_to_english: bool = True,
             use_cache: bool = True,

             scrape_reviews: bool = False,
             reviews_max: int = 20,
             reviews_sort: int = NEWEST,
             fields: Optional[List[str]] = DEFAULT_FIELDS,
             lang: Optional[str] = None,
             geo_coordinates: Optional[str] = None,
             zoom: Optional[float] = None) -> List[Dict]:
      """
      Function to scrape Google Maps places based on various criteria.

      :param queries: List of search queries or a single search query.
      :param min_reviews: Minimum number of reviews a place should have.
      :param max_reviews: Maximum number of reviews a place should have.
      :param category_in: List of categories the places should belong to.
      :param has_website: Boolean indicating if the place should have a website.
      :param has_phone: Boolean indicating if the place should have a phone number.
      :param min_rating: Minimum rating of the places.
      :param max_rating: Maximum rating of the places.
      :param sort: Sort criteria for the results.
      :param max: Maximum number of results to return.
      :param key: API key for Emails, Social Links Scraping.
      :param convert_to_english: Boolean indicating whether to convert non-English characters to English characters.
      :param use_cache: Boolean indicating whether to use cached data.
      :param scrape_reviews: Boolean indicating if the reviews should be scraped.
      :param reviews_max: Maximum number of reviews to scrape per place.
      :param reviews_sort: Sort order for reviews.
      :param fields: List of fields to return in the result.
      :param lang: Language in which to return the results.
      :param geo_coordinates: Geographical coordinates to scrape around.
      :param zoom: Zoom level for scraping.
      :return: List of dictionaries with the scraped place data.
      """

      result = []

      should_scrape_socials = key is not None      
      fields = determine_fields(fields, should_scrape_socials, scrape_reviews) 
          
      for query in queries:
        # 1. Scrape Places
                                        
        place_data = create_place_data(query, max, lang, geo_coordinates, zoom,links=[])
        places_obj = scraper.scrape_places(place_data, cache = use_cache)

        result_item = process_result(key, scrape_reviews, reviews_max, reviews_sort,  lang, should_scrape_socials,places_obj)

        result.append(result_item)
      
      all_places = sort_places(merge_places(result), sort)
      write_output("all", all_places, fields)

      scraper.scrape_places.close()
      return result



  @staticmethod
  def links(  
              links: List[str],
              output_folder: str,
              min_reviews: Optional[int] = None,
              max_reviews: Optional[int] = None,
              category_in: Optional[List[str]] = None,
              has_website: Optional[bool] = None,
              has_phone: Optional[bool] = None,
              min_rating: Optional[float] = None,
              max_rating: Optional[float] = None,
              sort: Optional[List[str]] = DEFAULT_SORT,
              max: Optional[int] = None,
              key: Optional[str] = None,
              convert_to_english: bool = True,
              use_cache: bool = True,
              scrape_reviews: bool = False,
              reviews_max: int = 20,
              reviews_sort: int = NEWEST,
              fields: Optional[List[str]] = DEFAULT_FIELDS,
              lang: Optional[str] = None) -> List[Dict]:
        """
        Function to scrape data from specific Google Maps place links.

        :param links: List of Google Maps place links to scrape data from.
        :param min_reviews: Minimum number of reviews a place should have.
        :param max_reviews: Maximum number of reviews a place should have.
        :param category_in: List of categories the places should belong to.
        :param has_website: Boolean indicating if the place should have a website.
        :param has_phone: Boolean indicating if the place should have a phone number.
        :param min_rating: Minimum rating of the places.
        :param max_rating: Maximum rating of the places.
        :param sort: Sort criteria for the results (not typically used with direct links).
        :param max: Maximum number of results to return.
        :param key: API key for Emails, Social Links Scraping.
        :param convert_to_english: Boolean indicating whether to convert non-English characters to English characters.
        :param use_cache: Boolean indicating whether to use cached data.
        :param scrape_reviews: Boolean indicating if the reviews should be scraped.
        :param reviews_max: Maximum number of reviews to scrape per place.
        :param reviews_sort: Sort order for reviews.
        :param fields: List of fields to return in the result.
        :param lang: Language in which to return the results.
        :return: List of dictionaries with the scraped data for each link.
        """

  
        should_scrape_socials = key is not None      
        fields = determine_fields(fields, should_scrape_socials, scrape_reviews) 

        if max is not None:
            links = links[:max]

        places = scraper.scrape_places_by_links({"links": links, "convert_to_english": convert_to_english, "cache": use_cache}, cache=use_cache)
        scraper.scrape_places_by_links.close()
        places_obj  = {"query":output_folder, "places": places }
        
        result_item = process_result(key, scrape_reviews, reviews_max, reviews_sort,  lang, should_scrape_socials,places_obj)
        
        return result_item
