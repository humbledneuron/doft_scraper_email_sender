from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Chrome driver
service = Service(r"D:\\BHaSH\\GHub\\fl\\switch_hayes\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Read credentials from file
with open("doft_details.txt", "r") as file:
    username, password = file.read().splitlines()

# Navigate to doft.com
driver.get("https://loadboard.doft.com/login")

# Log in
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input#driver_email"))
)
uname_element = driver.find_element(By.CSS_SELECTOR, "input#driver_email")
uname_element.click()
uname_element.send_keys(username)
pwd_element = driver.find_element(By.CSS_SELECTOR, "input#driver_password")
pwd_element.click()
pwd_element.send_keys(password + Keys.RETURN)

# Wait for the table to be present
table = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//div[@id="dTable"]'))
)

# Extract table headers
header_elements = table.find_element(By.XPATH, './/div[@class="t-head"]').find_elements(By.XPATH, './/div')
headers = [header.text for header in header_elements]
print("Headers:", headers)

# Get all viewing buttons
viewing_btns = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, './/div[@class="t-body"]//div[contains(@class, "b-load")]'))
)

total_btns = len(viewing_btns)

for index in range(total_btns):

    # Click each viewing button
    viewing_btn = viewing_btns[index]
    driver.execute_script("arguments[0].click();", viewing_btn)  # Click the button using JavaScript
    print(f"Viewing button {index+1}/{total_btns} clicked")
    time.sleep(2)  # Short sleep to ensure the action is completed

    # Re-fetch the table element after clicking
    table = driver.find_element(By.XPATH, '//div[@id="dTable"]')

    # Extract table rows
    body_element = table.find_element(By.XPATH, './/div[@class="t-body"]').find_element(By.XPATH, './/div[contains(@class, "iload")]')

    # Process each viewing button and extract data
    row_elements = body_element.find_elements(By.XPATH, './/div[contains(@class, "wrp")]')
    
    for row_element in row_elements:
        rows = row_element.find_elements(By.XPATH, './/div[contains(@class, "row")]')
        for row in rows:
            print("Row:", row.text)
        print("\nrow_elements")
    print("\nbody_elements\n")
# Close the browser
driver.quit()
