from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(r"D:\BHaSH\GHub\fl\switch_hayes\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Read credentials from file
with open("doft_details.txt", "r") as file:
    username, password = file.read().splitlines()

# Navigate to doft.com
driver.get("https://loadboard.doft.com/login")

# Logins here
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

# Click the viewing buttons
viewing_btns = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, './/div[@class="t-body"]//div[contains(@class, "b-load")]'))
)

# Extract table headers
header_elements = table.find_element(By.XPATH, './/div[@class="t-head"]').find_elements(By.XPATH, './/div')
headers = [header.text for header in header_elements]
print("Headers:", headers)

total_btns = 0
for btn in viewing_btns:
    driver.execute_script("arguments[0].click();", btn)  # opens using JavaScript to click the buttons
    print("Viewing button clicked")
    total_btns += 1 
    time.sleep(1)  # short sleep to ensure the action is completed

driver.implicitly_wait(10)

# Extract table rows
body_element = table.find_element(By.XPATH, './/div[@class="t-body"]').find_element(By.XPATH, './/div[contains(@class, "iload")]')

# Process each viewing button and extract data
row_elements = body_element.find_elements(By.XPATH, './/div[contains(@class, "wrp")]')
len_row_elements = len(row_elements)

print("Number of row elements:", len_row_elements)

for i in range(len_row_elements):
    
    if i < len_row_elements:
        current_row_wrapper = row_elements[i]
        current_rows = current_row_wrapper.find_elements(By.XPATH, './/div[contains(@class, "row")]')
        print(f"Number of rows in element current_rows {i + 1}: {len(current_rows)}")
        
        for r in current_rows:
            print("Row:", r.text)
        print("\nrow_elements")
    else:
        print(f"No more rows for button {i + 1}")
print("\nbody_elements\n")

# Close the browser
driver.quit()
