from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

class DoftScraper:
    def __init__(self, driver_path, credentials_file):
        self.driver_path = driver_path
        self.credentials_file = credentials_file
        self.driver = None

    def setup_driver(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    def read_credentials(self):
        with open(self.credentials_file, "r") as file:
            self.username, self.password = file.read().splitlines()

    def login(self):
        self.driver.get("https://loadboard.doft.com/login")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#driver_email"))
        )
        uname_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_email")
        uname_element.click()
        uname_element.send_keys(self.username)
        pwd_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_password")
        pwd_element.click()
        pwd_element.send_keys(self.password + Keys.RETURN)

    def extract_data(self):
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="dTable"]'))
        )
        viewing_btns = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="t-body"]//div[contains(@class, "b-load")]'))
        )
        viewing_btn = viewing_btns[0]
        self.driver.execute_script("arguments[0].click();", viewing_btn)
        table = self.driver.find_element(By.XPATH, '//div[@id="dTable"]')
        body_elements = table.find_element(By.XPATH, './/div[@class="t-body"]//div[contains(@class, "iload")]')
        row_elements = body_elements.find_element(By.XPATH, './/div[contains(@class, "wrp")]')
        row = row_elements.find_elements(By.XPATH, '//div[contains(@class, "row")]')

        data = {}

        try:
            data['age'] = row[1].find_element(By.XPATH, '//div[contains(@class, "time-ago")]').get_attribute('datetime')
        except:
            data['age'] = 'None'

        try:
            data['ref'] = row[1].find_element(By.XPATH, '//div[contains(@class, "tracking")]').text
        except:
            data['ref'] = 'None'

        linfo_rows1 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            data['pickup_date'] = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
        except:
            data['pickup_date'] = 'None'

        try:
            data['pickup_address'] = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]').text
        except:
            data['pickup_address'] = 'None'

        linfo_rows3 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            data['drop_date'] = linfo_rows3[3].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
        except:
            data['drop_date'] = 'None'

        try:
            data['drop_address'] = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]')[1].text
        except:
            data['drop_address'] = 'None'

        try:
            data['truck_type'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Truck Type')]/following-sibling::div[@class='val']").text
        except:
            data['truck_type'] = 'None'

        try:
            data['distance'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Distance')]/following-sibling::div[@class='val']").text
        except:
            data['distance'] = 'None'

        try:
            data['weight'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Weight')]/following-sibling::div[@class='val']").text
        except:
            data['weight'] = 'None'

        try:
            data['size'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Size')]/following-sibling::div[@class='val']").text
        except:
            data['size'] = 'None'

        try:
            data['length'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Length')]/following-sibling::div[@class='val']").text
        except:
            data['length'] = 'None'

        try:
            data['fuel_cost'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Est. Fuel Costs')]/following-sibling::div[@class='val']").text
        except:
            data['fuel_cost'] = 'None'

        linfo_rows31 = row[3].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            data['contact'] = linfo_rows31[2].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        except:
            data['contact'] = 'None'

        try:
            data['phone'] = linfo_rows31[3].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"]/following-sibling::div[@class="val"]//button[contains(@class, "call-shipper-btn")]').get_attribute('data-phone-num')
        except:
            try:
                data['phone'] = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Phone")]/following-sibling::div[@class="val"]').text
            except:
                data['phone'] = 'None'

        try:
            data['email'] = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Email")]/following-sibling::div[@class="val"]').text
        except:
            data['email'] = 'Reply back to this email'

        try:
            data['company'] = linfo_rows31[0].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="val l-shipper"]').text
        except:
            data['company'] = 'None'

        try:
            data['contact'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        except:
            data['contact'] = 'None'

        try:
            data['website'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Website")]/following-sibling::div[@class="val"]').text
        except:
            data['website'] = 'None'

        try:
            data['dot'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Dot")]/following-sibling::div[@class="val"]').text
        except:
            data['dot'] = 'None'

        try:
            data['docket'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Docket")]/following-sibling::div[@class="val"]').text
        except:
            data['docket'] = 'None'

        print(data)
        return data

    def quit_driver(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Current Directory: {current_dir}")

    scraper = DoftScraper(f"{current_dir}\\chromedriver.exe", "doft_details.txt")
    scraper.setup_driver()
    scraper.read_credentials()
    scraper.login()
    
    data = scraper.extract_data()
    with open('scraped_data.json', 'w') as file:
        file.write(json.dumps(data))      

    scraper.quit_driver()