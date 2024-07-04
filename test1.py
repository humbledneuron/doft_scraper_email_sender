from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

for btn in viewing_btns:
    driver.execute_script("arguments[0].click();", btn)  # opens using javaScript to click the buttons
    print("Viewing button clicked")

driver.implicitly_wait(5)
# Extract table rows
row_elements = table.find_element(By.XPATH, './/div[@class="t-body"]').find_element(By.XPATH, './/div[contains(@class, "iload")]').find_elements(By.XPATH, './/div[contains(@class, "wrp")]')
len_row_elements = len(row_elements)   
print("row_elements", len_row_elements)
for rows in row_elements:
    row = rows.find_elements(By.XPATH, './/div[contains(@class, "row")]')
    print("row")
    for r in row:
        print('r')
        print(r.text)
        
# i_load = row_elements.find_elements(By.XPATH, './/div[contains(@class, "row")]')
# # driver.execute_script("arguments[0].click();", btn) # closes
# rows = []
# for row in row_elements:
#     # cell_elements = row.find_elements(By.XPATH, './/div[contains(@class, "row")]')
#     # cells = [cell.text for cell in cell_elements]
#     # rows.append(cells)
#     rows.append(row.text)


# # Print headers and rows
# print("Headers:", headers)
# for row in rows:
#     print(row)

# Close the browser
driver.quit()
