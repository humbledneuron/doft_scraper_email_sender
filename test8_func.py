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

def extract_data(driver):
    # Wait for the table to be present
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="dTable"]'))
    )

    # Get all viewing buttons
    viewing_btns = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, './/div[@class="t-body"]//div[contains(@class, "b-load")]'))
    )

    # total_btns = len(viewing_btns)

    # click each 1st viewing button
    viewing_btn = viewing_btns[0]
    driver.execute_script("arguments[0].click();", viewing_btn)  # Click the button using JavaScript
    # print(f"Viewing button {0+1}/{total_btns} clicked")
    # time.sleep(1)  # short sleep to ensure the action is completed

    # re-fetching the table element after clicking
    table = driver.find_element(By.XPATH, '//div[@id="dTable"]')

    # extracting table rows
    body_elements = table.find_element(By.XPATH, './/div[@class="t-body"]//div[contains(@class, "iload")]')

    row_elements = body_elements.find_element(By.XPATH, './/div[contains(@class, "wrp")]')
        
    row = row_elements.find_elements(By.XPATH, '//div[contains(@class, "row")]')

    # print("Row:", len(row))

    #row 2 but index 1
    try:
        age = row[1].find_element(By.XPATH, '//div[contains(@class, "time-ago")]').get_attribute('datetime')
        print("Age:", age)
    except:
        print("Age:None")

    time.sleep(0.2)

    try:
        ref = row[1].find_element(By.XPATH, '//div[contains(@class, "tracking")]').text
        print("Ref:", ref)
    except:
        print("Ref: None")

    #row 3 but index 2
    # linfo 1 
    # time.sleep(1)

    linfo_rows1 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

    try:
        pickup_date = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
        print("Pickup Date:", pickup_date)
    except:
        print("Pickup Date:None")

    try:
        pickup_address = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]').text
        origin = pickup_address
        print("Pickup Address:", pickup_address)
        print("Origin:", origin)
    except:
        print("Pickup Address: None")

    # time.sleep(1)

    #linfo 3
    linfo_rows3 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

    try:
        drop_date = linfo_rows3[3].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
        print("drop Date:", drop_date)
    except:
        print("drop Date:None")

    try:
        drop_address = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]')[1].text
        print("drop Address:", drop_address)
    except:
        print("drop_address: None")

    try:
        truck_type_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Truck Type')]/following-sibling::div[@class='val']")
        truck_type = truck_type_element.text
        truck_type = truck_type.replace("Truck Type: ", "")
        print(f"Truck Type: {truck_type}")
    except:
        print("Truck type: None")

    try:
        distance_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Distance')]/following-sibling::div[@class='val']")
        distance = distance_element.text
        truck_type = truck_type.replace("Distance: ", "")
        print(f"Distance: {distance}")
    except:
        print("Distance: None")

    try:
        weight_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Weight')]/following-sibling::div[@class='val']")
        weight = weight_element.text
        truck_type = truck_type.replace("Weight: ", "")
        print(f"Weight: {weight}")
    except:
        print("Weight: None")

    try:
        size_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Size')]/following-sibling::div[@class='val']")
        size = size_element.text
        truck_type = truck_type.replace("Size: ", "")
        print(f"Size: {size}")
    except:
        print("Size: None")

    try:
        length_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Length')]/following-sibling::div[@class='val']")
        length = length_element.text
        truck_type = truck_type.replace("Length: ", "")
        print(f"Length: {length}")
    except:
        print("Length: None")

    try:
        fuel_cost_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Est. Fuel Costs')]/following-sibling::div[@class='val']")
        fuel_cost = fuel_cost_element.text
        truck_type = truck_type.replace("Est. Fuel Cost: ", "")
        print(f"Est. Fuel Cost: {fuel_cost}")
    except:
        print("Est. Fuel Cost: None")

    #row 4 but index 3
    # linfo 1 
    linfo_rows31 = row[3].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

    try:
        contact = linfo_rows31[2].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        print("Contact:", contact)
    except:
        print("Contact: None")

    try:
        phone = linfo_rows31[3].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"]/following-sibling::div[@class="val"]//button[contains(@class, "call-shipper-btn")]').get_attribute('data-phone-num')
        print("phone:", phone)
    except:
        phone = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Phone")]/following-sibling::div[@class="val"]').text
        print("phone:", phone)
    else:
        print("phone: None")

    try:
        email = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Email")]/following-sibling::div[@class="val"]').text
        print("email:", email)
    except:
        print("email: Reply back to this email")

    try:
        Company = linfo_rows31[0].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="val l-shipper"]').text
        print("Company:", Company)
    except:
        print("Company: None")

    try:
        contact = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        print("Contact:", contact)
    except:
        print("Contact: None")

    try:
        website = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Website")]/following-sibling::div[@class="val"]').text
        print("website:", website)
    except:
        print("website: None")

    try:
        Dot = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Dot")]/following-sibling::div[@class="val"]').text
        print("Dot:", Dot)
    except:
        print("Dot: None")

    try:
        Docket = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Docket")]/following-sibling::div[@class="val"]').text
        print("Docket:", Docket)
    except:
        print("Docket: None")

    print('\n\n')



# Call the function
# extract_data(driver)

#21.67702865600586
def con_extrtract_data(driver):
    # time.sleep(3)

    # open a new tab
    driver.execute_script("window.open('');")

    # switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # navigates to Google
    driver.get("https://loadboard.doft.com/panel#fid=521786")
    # time.sleep(1)
    # closes the previous tab (initial URL)
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

    # switch back to the current tab 
    driver.switch_to.window(driver.window_handles[0])
    extract_data(driver)
    # driver.refresh()

    # time.sleep(1)

start = time.time()
i = 0
while i < 3:
    # start_while = time.time()

    # con_extrtract_data(driver)
    extract_data(driver)
    # time.sleep(0.3)
    driver.refresh()

    # end_while = time.time()

    # print(f"While Time taken: {end_while - start_while}")
    i += 1
    # time.sleep(0.3)

end = time.time()

print(f"Time taken: {end - start}")

driver.quit()
