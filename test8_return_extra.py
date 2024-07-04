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

    # click each 1st viewing button
    viewing_btn = viewing_btns[0]
    driver.execute_script("arguments[0].click();", viewing_btn)  # Click the button using JavaScript
    # re-fetching the table element after clicking
    table = driver.find_element(By.XPATH, '//div[@id="dTable"]')
    # extracting table rows
    body_elements = table.find_element(By.XPATH, './/div[@class="t-body"]//div[contains(@class, "iload")]')
    row_elements = body_elements.find_element(By.XPATH, './/div[contains(@class, "wrp")]')      
    row = row_elements.find_elements(By.XPATH, '//div[contains(@class, "row")]')


    #row 2 but index 1
    try:
        age = row[1].find_element(By.XPATH, '//div[contains(@class, "time-ago")]').get_attribute('datetime')
        print("Age:", age)
        if age:
            return age
        else:
            return 'n/a'
    except:
        print("Age: None")

    time.sleep(0.2)

    try:
        ref = row[1].find_element(By.XPATH, '//div[contains(@class, "tracking")]').text
        print("Ref:", ref)
        if ref:
            return ref
        else:
            return 'n/a'        
    except:
        print("Ref: None")

    #row 3 but index 2
    # linfo 1 

    linfo_rows1 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

    try:
        pickup_date = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
        print("Pickup Date:", pickup_date)
        if pickup_date:
            return pickup_date
        else:
            return 'n/a'
    except:
        print("Pickup Date:None")

    try:
        pickup_address = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]').text
        origin = pickup_address
        print("Pickup Address:", pickup_address)
        print("Origin:", origin)
        if pickup_address:
            return pickup_address
        else:
            return 'n/a'
    except:
        print("Pickup Address: None")


    #linfo 3
    linfo_rows3 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

    try:
        drop_date = linfo_rows3[3].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
        print("drop Date:", drop_date)
        if drop_date:
            return drop_date
        else:
            return 'n/a'
    except:
        print("drop Date:None")

    try:
        drop_address = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]')[1].text
        print("drop Address:", drop_address)
        if drop_address:
            return drop_address
        else:
            return 'n/a'
    except:
        print("drop_address: None")

    try:
        truck_type_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Truck Type')]/following-sibling::div[@class='val']").text
        print(f"Truck Type: {truck_type_element}")
        if truck_type_element:
            return truck_type_element
        else:
            return 'n/a'
    except:
        print("Truck type: None")

    try:
        distance_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Distance')]/following-sibling::div[@class='val']").text
        print(f"Distance: {distance_element}")
        if distance_element:
            return distance_element
        else:
            return 'n/a'
    except:
        print("Distance: None")

    try:
        weight_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Weight')]/following-sibling::div[@class='val']").text
        print(f"Weight: {weight_element}")
        if weight_element:
            return weight_element
        else:
            return 'n/a'
    except:
        print("Weight: None")

    try:
        size_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Size')]/following-sibling::div[@class='val']").text
        print(f"Size: {size_element}")
        if size_element:
            return size_element
        else:
            return 'n/a'
    except:
        print("Size: None")

    try:
        length_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Length')]/following-sibling::div[@class='val']").text
        print(f"Length: {length_element}")
        if length_element:
            return length_element
        else:
            return 'n/a'
    except:
        print("Length: None")

    try:
        fuel_cost_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Est. Fuel Costs')]/following-sibling::div[@class='val']").text
        print(f"Est. Fuel Cost: {fuel_cost_element}")
        if fuel_cost_element:
            return fuel_cost_element
        else:
            return 'n/a'
    except:
        print("Est. Fuel Cost: None")

    #row 4 but index 3
    # linfo 1 
    linfo_rows31 = row[3].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

    try:
        contact_element = linfo_rows31[2].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        print("Contact:", contact_element)
        if contact_element:
            return contact_element
        else:
            return 'n/a'
    except:
        print("Contact: None")

    try:
        phone_element = linfo_rows31[3].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"]/following-sibling::div[@class="val"]//button[contains(@class, "call-shipper-btn")]').get_attribute('data-phone-num')
        print("phone:", phone_element)
        if phone_element:
            return phone_element
        else:
            phone_element = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Phone")]/following-sibling::div[@class="val"]').text
            if phone_element:
                return phone_element
            else:
                return 'n/a'
    except:
        phone_element = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Phone")]/following-sibling::div[@class="val"]').text
        print("phone:", phone_element)
        

    try:
        email_element = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Email")]/following-sibling::div[@class="val"]').text
        print("email:", email_element)
        if email_element:
            return email_element
        else:
            return 'n/a'
    except:
        print("email: Reply back to this email")

    try:
        company_element = linfo_rows31[0].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="val l-shipper"]').text
        print("Company:", company_element)
        if company_element:
            return company_element
        else:
            return 'n/a'
    except:
        print("Company: None")

    try:
        contact = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        print("Contact:", contact)
        if contact:
            return contact
        else:
            return 'n/a'
    except:
        print("Contact: None")

    try:
        website_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Website")]/following-sibling::div[@class="val"]').text
        print("website:", website_element)
        if website_element:
            return website_element
        else:
            return 'n/a'
    except:
        print("website: None")

    try:
        dot_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Dot")]/following-sibling::div[@class="val"]').text
        print("Dot:", dot_element)
        if dot_element:
            return dot_element
        else:
            return 'n/a'
    except:
        print("Dot: None")

    try:
        Docket_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Docket")]/following-sibling::div[@class="val"]').text
        print("Docket:", Docket_element)
        if Docket_element:
            return Docket_element
        else:
            return 'n/a'
    except:
        print("Docket: None")

    print('\n')



if __name__ == "__main__":

    start = time.time()
    i = 0
    while i < 3:
        # start_while = time.time()
        extract_data(driver)
        driver.refresh()
        # end_while = time.time()
        # print(f"While Time taken: {end_while - start_while}")
        i += 1

    end = time.time()

    print(f"Time taken: {end - start}")

    driver.quit()
