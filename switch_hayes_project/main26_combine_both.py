import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
import threading
import time
import subprocess
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
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
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#driver_email"))
        )
        uname_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_email")
        uname_element.click()
        uname_element.send_keys(self.username)
        pwd_element = self.driver.find_element(By.CSS_SELECTOR, "input#driver_password")
        pwd_element.click()
        pwd_element.send_keys(self.password + Keys.RETURN)

    def generate_random_string(self, length=16):
        characters = string.ascii_letters + string.digits #+ "!@#$%^&*()_+-=[]{}|;:',.<>/?"
        
        random_string = ''.join(random.choice(characters) for _ in range(length))
        
        return random_string
    
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

        time.sleep(2)

         
        try:
            data['ref'] = self.generate_random_string(16)
            # data['ref'] = row[1].find_element(By.XPATH, '//div[contains(@class, "tracking")]').text
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

    def refresh_session(self):
        self.driver.refresh()

    def quit_driver(self):
        if self.driver:
            self.driver.quit()



class EmailSender:
    def __init__(self):
        self.stop_event = threading.Event()
        self.send_interval = 20  # Default interval between sending emails (20 secs)
        self.scrape_interval = 3  # Interval to execute the scraper script (3 secs)
        self.batch_size = 1  # Number of emails to send concurrently
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

        self.root = tk.Tk()
        self.root.title("Email Sender")

        self.interval_label = tk.Label(self.root, text="Send Interval (seconds):")
        self.interval_label.pack(pady=5)

        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, str(self.send_interval))

        self.start_button = tk.Button(self.root, text="Start Sending", command=self.start_click)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Sending", command=self.stop_click, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def read_sender_details(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                sender_details = [tuple(line.strip().split(', ')) for line in lines]
            return sender_details
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None

    def read_email_list(self, file_path):
        try:
            with open(file_path, 'r') as f:
                emails = [line.strip() for line in f.readlines()]
            return emails
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []

    def format_email_template(self, data):
        def bold(text):
            return f"<strong>{text}</strong>"

        email_content = []

        email_present = data.get('email', 'n/a') != 'n/a' and data.get('email') is not None
        phone_present = data.get('phone', 'n/a') != 'n/a' and data.get('phone') is not None

        emojis = ""
        if email_present and phone_present:
            emojis = "🟩"
        elif email_present:
            emojis = "✉️"
        elif phone_present:
            emojis = "📞"

        first_line = f"{emojis} - {bold(data.get('price', 'n/a'))} - {bold(data.get('truck_type', 'n/a'))} - {bold(data.get('pickup_date', 'n/a'))} - {bold(data.get('pickup_address', 'n/a'))} - {bold(data.get('drop_address', 'n/a'))} - {bold(data.get('distance', 'n/a'))} - {bold(data.get('weight', 'n/a'))} - {bold(data.get('ref', 'n/a'))}"
        second_line = f"Age posted: {bold(data.get('age', 'n/a'))} (C.S.T.)"
        third_line = f"Truck type: {bold(data.get('truck_type', 'n/a'))}"
        fourth_line = f"Length: {bold(data.get('length', 'n/a'))}"
        fifth_line = f"Origin (zip (if/app.)): {bold(data.get('pickup_address', 'n/a'))} - Pick up date/ time: {bold(data.get('pickup_date', 'n/a'))} - Pick Up Hours: {bold(data.get('Pick Up Hours', 'n/a'))} - Dock Hours: {bold(data.get('Dock Hours', 'n/a'))}"
        sixth_line = f"Destination (zip (if/app.)): {bold(data.get('drop_address', 'n/a'))} - Drop off date/ time: {bold(data.get('drop_date', 'n/a'))}"
        seventh_line = f"Price: {bold(data.get('price', 'n/a'))} - Total trip mileage: {bold(data.get('distance', 'n/a'))} - Est. Fuel Costs: {bold(data.get('fuel_cost', 'n/a'))}"
        eighth_line = f"Full/ partial: {bold(data.get('load_type', 'n/a'))} - Weight: {bold(data.get('weight', 'n/a'))}"
        ninth_line = f"Commodity: {bold(data.get('commodity', 'n/a'))} - DIMS: {bold(data.get('dims', 'n/a'))}"
        tenth_line = f"Comments: {bold(data.get('comments', 'n/a'))}"
        eleventh_line = f"Company: {bold(data.get('company', 'n/a'))} - Address: {bold(data.get('address', 'n/a'))} - DOT: {bold(data.get('dot', 'n/a'))} - Docket: {bold(data.get('docket', 'n/a'))} - Contact: {bold(data.get('contact', 'n/a'))} - Phone: {bold(data.get('phone', 'n/a'))} - Fax: {bold(data.get('fax', 'n/a'))} - Email: {bold(data.get('email', 'n/a'))} - Website: {bold(data.get('website', 'n/a'))}"

        email_content.append(f"""
        <div style="text-align: center;">{first_line}</div>
        <div style="text-align: center;">{second_line}</div>
        <div style="text-align: center;">{third_line}</div>
        <div style="text-align: center;">{fourth_line}</div>
        <div style="text-align: center;">{fifth_line}</div>
        <div style="text-align: center;">{sixth_line}</div>
        <div style="text-align: center;">{seventh_line}</div>
        <div style="text-align: center;">{eighth_line}</div>
        <div style="text-align: center;">{ninth_line}</div>
        <div style="text-align: center;">{tenth_line}</div>
        <div style="text-align: center;">{eleventh_line}</div><br><br>
        """)

        email_template = f"""
        <html>
        <body style="font-family: Verdana; font-size: small;">
        <em>
        {''.join(email_content)}
        </em>
        </body>
        </html>
        """
        return email_template

    def send_email(self, smtp_server, smtp_port, sender_email, sender_pass, to_email, bcc_emails, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))  # Set email body as HTML

            if bcc_emails:
                msg['Bcc'] = ', '.join(bcc_emails)
            
            # Print email content to terminal
            print(f"Sending email to: {to_email} with BCC: {', '.join(bcc_emails)}")
            print(f"Subject: {subject}")
            print("Email Content:")
            print(body)

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_pass)
                server.sendmail(sender_email, [to_email] + bcc_emails, msg.as_string())
            print(f"Email sent to {to_email} with BCC to {', '.join(bcc_emails)}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def run_scraper_script(self):
        # try:
        #     subprocess.run(['python', 'doft_scraper.py'])
        # except Exception as e:
        #     print(f"Error executing scraper script: {e}")
        global scraper

        current_dir = os.getcwd()
        print(f"Current Directory: {current_dir}")

        scraper = DoftScraper(f"{current_dir}\\chromedriver.exe", "doft_details.txt")
        scraper.setup_driver()
        scraper.read_credentials()
        scraper.login()
        start = time.time()
        data = scraper.extract_data()
        with open('scraped_data.json', 'w') as file:
            file.write(json.dumps(data))
        end = time.time()
        print(f"Time taken: {end - start}")
        # scraper.quit_driver()
        scraper.refresh_session()

    def send_email_batch(self, sender_detail, smtp_server, smtp_port, recipient_email, bcc_list, email_subject, email_content):
        sender_email, sender_pass = sender_detail
        self.send_email(smtp_server, smtp_port, sender_email, sender_pass, recipient_email, bcc_list, email_subject, email_content)

    def start_sending_emails(self, smtp_server, smtp_port):
        sender_details = self.read_sender_details('sender_details.txt')
        bcc_list = self.read_email_list('bcc_list.txt')
        recipient_email = self.read_email_list('recipient_email.txt')[0]  # Assuming there is only one recipient email but multiple BCC and sender emails   

        if not sender_details or not recipient_email:
            print("Failed to load email details.")
            return

        while not self.stop_event.is_set():
            self.run_scraper_script()  # Extract data first

            try:
                with open("scraped_data.json", "r") as file:
                    data = json.load(file)
                    if not isinstance(data, dict):
                        raise ValueError("Loaded data is not a dictionary")
            except FileNotFoundError:
                print("File not found: scraped_data.json")
                continue
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                continue
            except ValueError as ve:
                print(f"Invalid data format in JSON: {ve}")
                continue

            email_subject = 'Insert your email subject here'
            email_content = self.format_email_template(data)  # Format data into email content

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.batch_size) as executor:
                futures = [executor.submit(self.send_email_batch, sender_detail, smtp_server, smtp_port, recipient_email, bcc_list, email_subject, email_content) for sender_detail in sender_details]
                concurrent.futures.wait(futures)

            print(f"Sending data to {recipient_email} with BCC to {', '.join(bcc_list)}")
            
            time.sleep(self.send_interval)

        print("Email sending stopped.")

    def stop_sending_emails(self):
        self.stop_event.set()

    def start_click(self):
        try:
            self.send_interval = int(self.interval_entry.get())
        except ValueError:
            print("Invalid interval value. Using default.")
        
        threading.Thread(target=self.start_sending_emails, args=(self.smtp_server, self.smtp_port), daemon=True).start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_click(self):
        self.stop_sending_emails()
        scraper.quit_driver()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    email_sender = EmailSender()
    email_sender.run()
