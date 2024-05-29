import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_PAGE_NUM = 66


def extract_addresses():
    # Set up Selenium options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Provide the path to the chromedriver executable
    service = Service()

    # Start a new Chrome session
    driver = webdriver.Chrome(service=service, options=options)

    # Open the website
    driver.get("https://mios.rs/strana/zdravstvene-ustanove.html")

    addresses = []
    actions = ActionChains(driver)

    for i in range(0, MAX_PAGE_NUM):
        # Wait until the table is loaded
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table#cmsDataTable tbody"))
        )

        # Extract all rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 3:
                city = columns[1].text.strip()
                address = columns[3].text.strip()
                if city.lower() == 'novi sad':
                    addresses.append(f"Srbija, {city}, {address}")

        # Find the 'Next' button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cmsDataTable_next"))
        )

        # Scroll to the 'Next' button
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

        # Click the 'Next' button
        next_button.click()
    driver.quit()
    return addresses


# Use the function to extract addresses
addresses = extract_addresses()

# Save addresses to a CSV file
with open('addresses.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Address', 'City', 'Country'])
    for address in addresses:
        writer.writerow([address])

print("Addresses exported to addresses.csv")
