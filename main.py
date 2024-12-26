from botasaurus.browser import browser, Driver

from botasaurus.browser import browser, Driver

@browser(driver_path="/usr/bin/chromedriver")
def scrape_heading_task(driver: Driver, data):
    driver.get("https://www.omkar.cloud/")
    heading = driver.get_text("h1")
    return {"heading": heading}

# Initiate the web scraping task
scrape_heading_task()