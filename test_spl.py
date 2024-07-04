from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DoftExtractor:
    def __init__(self, driver_path):
        # Set up the Chrome driver
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)

    def extract_data(self):

        data = {}

        # Read credentials from file
        with open("doft_details.txt", "r") as file:
            username, password = file.read().splitlines()

        # Navigate to doft.com
        self.driver.get("https://loadboard.doft.com/login")

        # Log in
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#driver_email"))
        )
        uname_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_email")
        uname_element.click()
        uname_element.send_keys(username)
        pwd_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_password")
        pwd_element.click()
        pwd_element.send_keys(password + Keys.RETURN)

        # Wait for the table to be present
        table = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="dTable"]'))
        )
        # Get all viewing buttons
        viewing_btns = WebDriverWait(self.driver, 20).until(
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

        # Row 2 but index 1
        try:
            age = row[1].find_element(By.XPATH, '//div[contains(@class, "time-ago")]').get_attribute('datetime')
            data['Age'] = age if age else 'n/a'
        except:
            data['Age'] = 'None'

        time.sleep(0.2)

        try:
            ref = row[1].find_element(By.XPATH, '//div[contains(@class, "tracking")]').text
            data['Ref'] = ref if ref else 'n/a'
        except:
            data['Ref'] = 'None'

        # Row 3 but index 2
        linfo_rows1 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            pickup_date = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
            data['Pickup Date'] = pickup_date if pickup_date else 'n/a'
        except:
            data['Pickup Date'] = 'None'

        try:
            pickup_address = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]').text
            data['Pickup Address'] = pickup_address if pickup_address else 'n/a'
            data['Origin'] = pickup_address if pickup_address else 'n/a'
        except:
            data['Pickup Address'] = 'None'
            data['Origin'] = 'None'

        linfo_rows3 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            drop_date = linfo_rows3[3].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
            data['Drop Date'] = drop_date if drop_date else 'n/a'
        except:
            data['Drop Date'] = 'None'

        try:
            drop_address = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]')[1].text
            data['Drop Address'] = drop_address if drop_address else 'n/a'
        except:
            data['Drop Address'] = 'None'

        try:
            truck_type_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Truck Type')]/following-sibling::div[@class='val']").text
            data['Truck Type'] = truck_type_element if truck_type_element else 'n/a'
        except:
            data['Truck Type'] = 'None'

        try:
            distance_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Distance')]/following-sibling::div[@class='val']").text
            data['Distance'] = distance_element if distance_element else 'n/a'
        except:
            data['Distance'] = 'None'

        try:
            weight_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Weight')]/following-sibling::div[@class='val']").text
            data['Weight'] = weight_element if weight_element else 'n/a'
        except:
            data['Weight'] = 'None'

        try:
            size_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Size')]/following-sibling::div[@class='val']").text
            data['Size'] = size_element if size_element else 'n/a'
        except:
            data['Size'] = 'None'

        try:
            length_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Length')]/following-sibling::div[@class='val']").text
            data['Length'] = length_element if length_element else 'n/a'
        except:
            data['Length'] = 'None'

        try:
            fuel_cost_element = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Est. Fuel Costs')]/following-sibling::div[@class='val']").text
            data['Est. Fuel Cost'] = fuel_cost_element if fuel_cost_element else 'n/a'
        except:
            data['Est. Fuel Cost'] = 'None'

        # Row 4 but index 3
        linfo_rows31 = row[3].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            contact_element = linfo_rows31[2].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
            data['Contact'] = contact_element if contact_element else 'n/a'
        except:
            data['Contact'] = 'None'

        try:
            phone_element = linfo_rows31[3].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"]/following-sibling::div[@class="val"]//button[contains(@class, "call-shipper-btn")]').get_attribute('data-phone-num')
            data['Phone'] = phone_element if phone_element else 'n/a'
        except:
            data['Phone'] = 'None'

        try:
            email_element = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Email")]/following-sibling::div[@class="val"]').text
            data['Email'] = email_element if email_element else 'n/a'
        except:
            data['Email'] = 'Reply back to this email'

        try:
            company_element = linfo_rows31[0].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="val l-shipper"]').text
            data['Company'] = company_element if company_element else 'n/a'
        except:
            data['Company'] = 'None'

        try:
            contact = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
            data['Contact'] = contact if contact else 'n/a'
        except:
            data['Contact'] = 'None'

        try:
            website_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Website")]/following-sibling::div[@class="val"]').text
            data['Website'] = website_element if website_element else 'n/a'
        except:
            data['Website'] = 'None'

        try:
            dot_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Dot")]/following-sibling::div[@class="val"]').text
            data['Dot'] = dot_element if dot_element else 'n/a'
        except:
            data['Dot'] = 'None'

        try:
            docket_element = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Docket")]/following-sibling::div[@class="val"]').text
            data['Docket'] = docket_element if docket_element else 'n/a'
        except:
            data['Docket'] = 'None'

        print('\n')
        return data

if __name__ == "__main__":
    driver_path = r"D:\\BHaSH\\GHub\\fl\\switch_hayes\\chromedriver.exe"
    de = DoftExtractor(driver_path)
    start = time.time()
    i = 0
    while i < 3:
        data = de.extract_data()
        print(data)
        de.driver.refresh()
        time.sleep(0.2)
        i += 1

    end = time.time()
    print(f"Time taken: {end - start}")
    de.driver.quit()
