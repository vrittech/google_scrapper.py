from botasaurus.browser import browser, Driver

@browser
def scrape_heading_task(driver: Driver, data):
    # Set the driver path manually
    driver.set_driver_path("/usr/bin/chromedriver")
    
    # Visit the website
    driver.get("https://www.omkar.cloud/")
    
    # Retrieve the heading element's text
    heading = driver.get_text("h1")

    # Save the data as a JSON file
    return {"heading": heading}

# Run the web scraping task
scrape_heading_task()
