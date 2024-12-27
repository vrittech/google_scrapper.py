import asyncio
import re
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import phonenumbers
from urllib.parse import urljoin


def validate_email(email):
    """
    Validate email address format.
    """
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return email_pattern.match(email) is not None


def validate_and_format_phone(phone, default_country="NP"):
    """
    Normalize and validate phone numbers using `phonenumbers`.
    Ensures consistent international format and avoids incorrect country codes.
    """
    try:
        # Parse the phone number with the provided default country
        parsed_number = phonenumbers.parse(phone, default_country)

        # Reparse as Nepal if the number lacks a country code and default is Nepal
        if not phone.startswith("+") and parsed_number.country_code != phonenumbers.country_code_for_region(default_country):
            parsed_number = phonenumbers.parse(phone, default_country)

        # Validate and return the number in international format
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return None


def deduplicate_phone_numbers(phone_numbers):
    """
    Deduplicate phone numbers and resolve conflicts between different country codes.
    Prioritize explicit country codes over inferred ones.
    """
    seen_numbers = {}
    for phone in phone_numbers:
        try:
            parsed_number = phonenumbers.parse(phone)
            national_number = parsed_number.national_number  # Extract the national number part

            if national_number not in seen_numbers:
                seen_numbers[national_number] = phone
            else:
                # Prioritize numbers with explicit country codes
                existing_number = seen_numbers[national_number]
                if phone.startswith("+") and not existing_number.startswith("+"):
                    seen_numbers[national_number] = phone
        except phonenumbers.NumberParseException:
            continue

    return list(seen_numbers.values())


def extract_emails(html_content):
    """
    Extract and validate emails from HTML content.
    """
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", re.IGNORECASE)
    emails = set(re.findall(email_pattern, html_content))

    # Known invalid placeholder patterns
    invalid_patterns = [
        "example.com",
        "yourname.com",
        "yourdomain.com",
        "test.com",
        "placeholder.com"
    ]

    # Filter out invalid or placeholder emails
    valid_emails = [
        email for email in emails
        if validate_email(email) and not any(pattern in email for pattern in invalid_patterns)
    ]

    return valid_emails



def extract_phone_numbers(html_content, default_country="NP"):
    """
    Extract and validate phone numbers from HTML content, ensuring Nepalese numbers are correctly interpreted.
    """
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    phone_numbers = set()
    keywords = ['tel', 'contact', 'mobile', 'phone', '📞', '☎️', 'call']

    # Extract numbers from "tel:" links
    phone_numbers.update(
        tag["href"].split("tel:")[-1].strip()
        for tag in soup.find_all("a", href=True)
        if "tel:" in tag["href"].lower()
    )

    # Extract numbers from relevant text associated with keywords or emojis
    phone_pattern = r"\+?\(?\d{1,4}\)?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}"
    for tag in soup.find_all(["p", "span", "div", "li", "a"]):
        text = tag.get_text()
        if any(keyword in text.lower() for keyword in keywords) or any(emoji in text for emoji in ['📞', '☎️']):
            raw_numbers = re.findall(phone_pattern, text)
            phone_numbers.update(raw_numbers)

    # Debug: Log raw phone numbers
    print("Raw Phone Numbers Extracted:", phone_numbers)

    # Normalize and validate the numbers
    normalized_numbers = {
        validate_and_format_phone(phone, default_country)
        for phone in phone_numbers
        if validate_and_format_phone(phone, default_country) is not None
    }

    # Deduplicate numbers
    deduplicated_numbers = deduplicate_phone_numbers(normalized_numbers)

    # Debug: Log normalized and deduplicated numbers
    print("Normalized Phone Numbers:", deduplicated_numbers)

    return deduplicated_numbers


async def scrape_additional_pages(base_url, page, keywords, default_country="NP"):
    """
    Scrape additional pages such as "Contact Us", "About Us", or "Footer".
    """
    additional_emails = set()
    additional_phone_numbers = set()

    try:
        links = await page.eval_on_selector_all(
            "a",
            "elements => elements.map(e => e.href).filter(link => link)"
        )
        for link in links:
            if any(keyword in link.lower() for keyword in keywords):
                full_url = urljoin(base_url, link)
                if not full_url:
                    continue
                try:
                    await page.goto(full_url, timeout=120000, wait_until="load")
                    content = await page.content()
                    additional_emails.update(extract_emails(content))
                    additional_phone_numbers.update(extract_phone_numbers(content, default_country))
                except Exception as e:
                    print(f"Error scraping additional page {full_url}: {e}")
    except Exception as e:
        print(f"Error finding additional links: {e}")

    return list(additional_emails), list(additional_phone_numbers)


async def scrape_website(website, browser, retries=3, default_country="NP"):
    """
    Scrape contact information (emails and phone numbers) from a website.
    """
    for attempt in range(retries):
        try:
            if not website.startswith("http://") and not website.startswith("https://"):
                website = "http://" + website

            context = await browser.new_context()
            page = await context.new_page()

            print(f"Visiting {website} (Attempt {attempt + 1})")
            await page.goto(website, timeout=120000, wait_until="load")

            # Get HTML content
            html_content = await page.content()

            # Extract emails and phone numbers from the main page
            emails = set(extract_emails(html_content))
            phone_numbers = set(extract_phone_numbers(html_content, default_country))

            # Check additional pages
            additional_keywords = ['contact', 'about', 'impressum']
            additional_emails, additional_phone_numbers = await scrape_additional_pages(
                website, page, additional_keywords, default_country
            )

            # Merge results
            emails.update(additional_emails)
            phone_numbers.update(additional_phone_numbers)

            await context.close()

            # Filter garbage and irrelevant data
            emails = [email for email in emails if validate_email(email)]
            phone_numbers = [phone for phone in phone_numbers if phonenumbers.is_possible_number(phonenumbers.parse(phone))]

            return {
                "Website": website,
                "Contact Details": {
                    "Emails": emails,
                    "Phone Numbers": phone_numbers
                }
            }

        except Exception as e:
            print(f"Error scraping {website} (Attempt {attempt + 1}): {e}")
            if attempt == retries - 1:
                return {"Website": website, "Error": f"Failed after {retries} attempts."}


async def main():
    """
    Main function to scrape websites.
    """
    user_input = input("Enter URLs separated by commas: ").strip()
    websites = [url.strip() for url in user_input.split(",")]

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        tasks = [scrape_website(website, browser) for website in websites]
        results = await asyncio.gather(*tasks)

        await browser.close()

    # Save results to a JSON file
    output_file = "contact_details.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print(f"Scraping complete. Results saved to '{output_file}'.")


# if __name__ == "__main__":
#     asyncio.run(main())
