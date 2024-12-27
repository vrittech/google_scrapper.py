import re
import json
from playwright.sync_api import sync_playwright

# Keywords for validation
KEYWORDS_NAME = ["company", "solutions", "software", "IT", "Pvt", "Ltd", "services", "innovation"]
KEYWORDS_PHONE = ["call", "contact", "phone", "mobile", "tel", "number"]
KEYWORDS_WEBSITE = ["visit", "website", "url", "official", "site"]

def scrape_google_maps(query, max_results=30):
    """Scrape Google Local Search Results."""
    results = []
    seen_results = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        search_url = f"https://www.google.com/search?q={query}&num=10&tbm=lcl"
        print(f"Navigating to {search_url}")
        page.goto(search_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        while len(results) < max_results:
            containers = page.locator('div.VkpGBb').all()
            print(f"Found {len(containers)} results on this page.")

            for container in containers:
                try:
                    name = extract_text(container, 'span.OSrXXb', KEYWORDS_NAME)
                    details_raw = extract_text(container, 'div.rllt__details', [])
                    phone_number = extract_phone(details_raw)
                    website = extract_website(container)

                    if name in seen_results:
                        continue
                    seen_results.add(name)

                    results.append({
                        "name": name if name else "N/A",
                        "details": details_raw if details_raw else "N/A",
                        "phone_number": phone_number if phone_number else "N/A",
                        "website": website if website else "N/A"
                    })

                except Exception as e:
                    print(f"Error parsing container: {e}")

                if len(results) >= max_results:
                    break

            # Pagination
            if page.locator('a#pnnext').count() > 0:
                print("Navigating to next page...")
                page.locator('a#pnnext').click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(5000)
            else:
                print("No more pages.")
                break

        browser.close()

    # Save results
    with open("google_maps_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(results)} results.")
    return results

def extract_text(container, selector, keywords):
    """Extracts text from the given selector. Matches keywords if provided."""
    try:
        elements = container.locator(selector).all()
        for element in elements:
            text = element.inner_text(timeout=3000).strip()
            if not keywords or any(keyword.lower() in text.lower() for keyword in keywords):
                return text
        return elements[0].inner_text(timeout=3000).strip() if elements else "N/A"
    except Exception as e:
        print(f"Error extracting text: {e}")
        return "N/A"

def extract_phone(details):
    """Extract phone numbers from the details text if not already extracted."""
    if not details or details == "N/A":
        return "N/A"
    
    # Enhanced regex to match phone numbers (mobile and landline formats)
    phone_regex = r"\b(?:\d{3}-\d{7,8}|\d{7,8}|\d{2}-\d{7,8})\b"
    matches = re.findall(phone_regex, details)
    
    if matches:
        return ", ".join(matches)  # Return all matched numbers as a single string
    return "N/A"

def extract_website(container):
    """Extract website URLs."""
    try:
        links = container.locator("a").all()
        for link in links:
            href = link.get_attribute("href", timeout=3000)
            if href and "http" in href and "google.com" not in href and "maps" not in href:
                return href
            if href and "url?q=" in href:
                match = re.search(r"url\?q=(https?://[^\s&]+)", href)
                if match:
                    return match.group(1)
        return "N/A"
    except Exception as e:
        print(f"Error extracting website: {e}")
        return "N/A"

if __name__ == "__main__":
    query = input("Enter search query (e.g., Schools in Kathmandu): ").strip()
    while True:
        try:
            num_results = int(input("How many unique results do you want to scrape? "))
            if num_results > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    results = scrape_google_maps(query, max_results=num_results)

    # Print results
    print("\nResults:")
    for item in results:
        print(json.dumps(item, indent=4, ensure_ascii=False))
