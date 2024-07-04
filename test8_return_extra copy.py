from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Doft_extracter:
    def __init__(self, driver_path):
        # Set up the Chrome driver
        self.service = Service(driver_path) #r"D:\\BHaSH\\GHub\\fl\\switch_hayes\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)

    def extract_data(self):

        data = {}

        # Read credentials from file
        with open("doft_details.txt", "r") as file:
            username, password = file.read().splitlines()

        # Navigate to doft.com
        self.driver.get("https://loadboard.doft.com/login")

        # Log in
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#driver_email"))
        )
        uname_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_email")
        uname_element.click()
        uname_element.send_keys(username)
        pwd_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_password")
        pwd_element.click()
        pwd_element.send_keys(password + Keys.RETURN)

        # Wait for the table to be present
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="dTable"]'))
        )
        # Get all viewing buttons
        viewing_btns = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="t-body"]//div[contains(@class, "b-load")]'))
        )

        # click each 1st viewing button
        viewing_btn = viewing_btns[0]
        self.driver.execute_script("arguments[0].click();", viewing_btn)  # Click the button using JavaScript
        # re-fetching the table element after clicking
        table = self.driver.find_element(By.XPATH, '//div[@id="dTable"]')
        # extracting table rows
        body_elements = table.find_element(By.XPATH, './/div[@class="t-body"]//div[contains(@class, "iload")]')
        row_elements = body_elements.find_element(By.XPATH, './/div[contains(@class, "wrp")]')
        row = row_elements.find_elements(By.XPATH, '//div[contains(@class, "row")]')


        #row 2 but index 1
        try:
            age = row[1].find_element(By.XPATH, '//div[contains(@class, "time-ago")]').get_attribute('datetime')
            print("Age:", age)
            data['Age'] = age if age else 'n/a'
        except:
            print("Age: None")
            data['Age'] = 'None'

        time.sleep(0.2)

        try:
            ref = row[1].find_element(By.XPATH, '//div[contains(@class, "tracking")]').text
            data['Ref'] = ref if ref else 'n/a'
            print("Ref:", ref)
    
        except:
            print("Ref: None")
            data['Ref'] = 'None'

        #row 3 but index 2
        # linfo 1 

        linfo_rows1 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            pickup_date = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
            print("Pickup Date:", pickup_date)
            data['Pickup Date'] = pickup_date if pickup_date else 'n/a'
        except:
            print("Pickup Date:None")
            data['Pickup Date'] = 'None'

        try:
            pickup_address = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]').text
            print("Pickup Address:", pickup_address)
            data['Pickup Address'] = pickup_address if pickup_address else 'n/a'
            data['Origin'] = pickup_address if pickup_address else 'n/a'
        except:
            print("Pickup Address: None")
            data['Pickup Address'] = 'None'
            data['Origin'] = 'None'


        #linfo 3
        linfo_rows3 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            drop_date = linfo_rows3[3].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
            print("drop Date:", drop_date)
            data['Drop Date'] = drop_date if drop_date else 'n/a'
        except:
            print("drop Date:None")
            data['Drop Date'] = 'None'

        try:
            drop_address = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]')[1].text
            print("drop Address:", drop_address)
            data['Drop Address'] = drop_address if drop_address else 'n/a'
        except:
            print("drop_address: None")
            data['Drop Address'] = 'None'

        try:
            truck_type_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Truck Type')]/following-sibling::div[@class='val']").text
            print(f"Truck Type: {truck_type_element}")
            data['Truck Type'] = truck_type_element if truck_type_element else 'n/a'
        except:
            print("Truck type: None")
            data['Truck Type'] = 'None'

        try:
            distance_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Distance')]/following-sibling::div[@class='val']").text
            print(f"Distance: {distance_element}")
            data['Distance'] = distance_element if distance_element else 'n/a'
        except:
            print("Distance: None")
            data['Distance'] = 'None'

        try:
            weight_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Weight')]/following-sibling::div[@class='val']").text
            print(f"Weight: {weight_element}")
            data['Weight'] = weight_element if weight_element else 'n/a'
        except:
            print("Weight: None")
            data['Weight'] = 'n/a'

        try:
            size_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Size')]/following-sibling::div[@class='val']").text
            print(f"Size: {size_element}")
            data['Size'] = size_element if size_element else 'n/a'
        except:
            print("Size: None")
            data['Size'] = 'n/a'

        try:
            length_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Length')]/following-sibling::div[@class='val']").text
            print(f"Length: {length_element}")
            data['Length'] = length_element if length_element else 'n/a'
        except:
            print("Length: None")
            data['Length'] = 'n/a'

        try:
            fuel_cost_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Est. Fuel Costs')]/following-sibling::div[@class='val']").text
            print(f"Est. Fuel Cost: {fuel_cost_element}")
            data['Est. Fuel Cost'] = fuel_cost_element if fuel_cost_element else 'n/a'
        except:
            print("Est. Fuel Cost: None")
            data['Est. Fuel Cost'] = 'n/a'

        #row 4 but index 3
        # linfo 1 
        linfo_rows31 = row[3].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            contact_element = linfo_rows31[2].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
            print("Contact:", contact_element)
            data['Contact'] = contact_element if contact_element else 'n/a'
        except:
            print("Contact: None")
            data['Contact'] = 'n/a'

        try:
            phone_element = linfo_rows31[3].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"]/following-sibling::div[@class="val"]//button[contains(@class, "call-shipper-btn")]').get_attribute('data-phone-num')
            print("phone:", phone_element)
            data['Phone'] = phone_element if phone_element else 'n/a'
        except:
            phone_element = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Phone")]/following-sibling::div[@class="val"]').text
            print("phone:", phone_element)
            data['Phone'] = phone_element if phone_element else 'n/a'
            

        try:
            email_element = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Email")]/following-sibling::div[@class="val"]').text
            print("email:", email_element)
            data['Email'] = email_element if email_element else 'Reply back to this email'
        except:
            print("email: Reply back to this email")
            data['Email'] = 'Reply back to this email'

        try:
            company_element = linfo_rows31[0].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="val l-shipper"]').text
            print("Company:", company_element)
            data['Company'] = company_element if company_element else 'n/a'
        except:
            print("Company: None")
            data['Company'] = 'n/a'

        try:
            contact = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
            print("Contact:", contact)
            data['Contact'] = contact if contact else 'n/a'
        except:
            print("Contact: None")
            data['Contact'] = 'n/a'

        try:
            website_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Website")]/following-sibling::div[@class="val"]').text
            print("website:", website_element)
            data['Website'] = website_element if website_element else 'n/a'
        except:
            print("website: None")
            data['Website'] = 'n/a'

        try:
            dot_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Dot")]/following-sibling::div[@class="val"]').text
            print("Dot:", dot_element)
            data['Dot'] = dot_element if dot_element else 'n/a'
        except:
            print("Dot: None")
            data['Dot'] = 'n/a'

        try:
            docket_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Docket")]/following-sibling::div[@class="val"]').text
            print("Docket:", docket_element)
            data['Docket'] = docket_element if docket_element else 'n/a'
        except:
            print("Docket: None")
            data['Docket'] = 'n/a'

        print('\n')



if __name__ == "__main__":

    driver_path = r"D:\\BHaSH\\GHub\\fl\\switch_hayes\\chromedriver.exe"

    de = Doft_extracter(driver_path)
    start = time.time()
    i = 0
    while i < 3:
        # start_while = time.time()
        data = de.extract_data()
        print(data)
        de.driver.refresh()
        # end_while = time.time()
        # print(f"While Time taken: {end_while - start_while}")
        i += 1

    end = time.time()

    print(f"Time taken: {end - start}")

    de.driver.quit()
