from botasaurus.browser import browser, Driver

# Define the function to add arguments
def add_arguments(data, options):
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

@browser(headless=True)
def scrape_heading_task(driver: Driver, data):
    # Visit the website
    driver.get("https://www.omkar.cloud/")
    
    # Retrieve the heading element's text
    heading = driver.get_text("h1")

    # Return the heading
    return {"heading": heading}

# Run the web scraping task
scrape_heading_task()
