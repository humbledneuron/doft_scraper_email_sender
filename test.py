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

#logins here
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CSS_SELECTOR ,"input#driver_email"))
)

uname_element = driver.find_element(By.CSS_SELECTOR ,"input#driver_email")
uname_element.click()
uname_element.send_keys("retr0arcade@icloud.com")

# time.sleep(2)
pwd_element = driver.find_element(By.CSS_SELECTOR ,"input#driver_password")
pwd_element.click()
pwd_element.send_keys("UpWork0Dann!" + Keys.RETURN)

driver.implicitly_wait(5)

# Locate the table
table = driver.find_element(By.XPATH, '//div[@id="dTable"]')

# Click the viewing button
viewing_btn = driver.find_element(By.XPATH, './/div[@class="t-body"]').find_elements(By.XPATH, './/div[contains(@class, "b-load")]')
for btn in viewing_btn:
    btn.click() 

# Extract table headers
header_elements = table.find_element(By.XPATH, './/div[@class="t-head"]').find_elements(By.XPATH, './/div')
headers = [header.text for header in header_elements]

driver.implicitly_wait(7)
# Extract table rows
row_elements = table.find_element(By.XPATH, './/div[@class="t-body"]').find_elements(By.XPATH, './/div[contains(@class, "b-load")]')
# rows = []
# for row in row_elements:
#     cell_elements = row.find_elements(By.XPATH, './/div[contains(@class, "cell")]')
#     cells = [cell.text for cell in cell_elements]
#     rows.append(cells)


# Print headers and rows
print("Headers:", headers)
for row in row_elements:
    print(row.text)

driver.implicitly_wait(30)
# Close the browser
driver.quit()
