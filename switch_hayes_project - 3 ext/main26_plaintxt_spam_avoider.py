import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
import threading
import time
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
        # Create a plain text email template
        email_content = []

        line_1 = f"Age posted: {data.get('age', 'n/a')} (C.S.T.)"
        line_2 = f"Truck type: {data.get('truck_type', 'n/a')}"
        line_3 = f"Length: {data.get('length', 'n/a')}"
        line_4 = f"Origin (zip (if/app.)): {data.get('pickup_address', 'n/a')}"
        line_5 = f"Pick up date/ time: {data.get('pickup_date', 'n/a')}"
        line_6 = f"Pick Up Hours: {data.get('Pick Up Hours', 'n/a')}"
        line_7 = f"Dock Hours: {data.get('Dock Hours', 'n/a')}"
        line_8 = f"Destination (zip (if/app.)): {data.get('drop_address', 'n/a')}"
        line_9 = f"Drop off date/ time: {data.get('drop_date', 'n/a')}"
        line_10 = f"Price: {data.get('price', 'n/a')}"
        line_11 = f"Total trip mileage: {data.get('distance', 'n/a')}"
        line_12 = f"Est. Fuel Costs: {data.get('fuel_cost', 'n/a')}"
        line_13 = f"Full/ partial: {data.get('load_type', 'n/a')}"
        line_14 = f"Weight: {data.get('weight', 'n/a')}"
        line_15 = f"Commodity: {data.get('commodity', 'n/a')}"
        line_16 = f"DIMS: {data.get('dims', 'n/a')}"
        line_17 = f"Comments: {data.get('comments', 'n/a')}"
        line_18 = f"Company: {data.get('company', 'n/a')}"
        line_19 = f"Address: {data.get('address', 'n/a')}"
        line_20 = f"DOT: {data.get('dot', 'n/a')}"
        line_21 = f"Docket: {data.get('docket', 'n/a')}"
        line_22 = f"Contact: {data.get('contact', 'n/a')}"
        line_23 = f"Phone: {data.get('phone', 'n/a')}"
        line_24 = f"Fax: {data.get('fax', 'n/a')}"
        line_25 = f"Email: {data.get('email', 'n/a')}"
        line_26 = f"Website: {data.get('website', 'n/a')}"

        email_content.append(
            f"{line_1}\n\n{line_2}\n{line_3}\n\n{line_4}\n{line_5}\n{line_6}\n{line_7}\n\n{line_8}\n{line_9}\n\n"
            f"{line_10}\n{line_11}\n{line_12}\n\n{line_13}\n{line_14}\n\n{line_15}\n{line_16}\n\n{line_17}\n\n"
            f"{line_18}\n{line_19}\n{line_20}\n{line_21}\n{line_22}\n{line_23}\n{line_24}\n{line_25}\n{line_26}"
        )

        email_template = "\n".join(email_content)
        return email_template

    def send_email(self, smtp_server, smtp_port, sender_email, sender_pass, to_email, bcc_emails, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))  # Set email body as plain text

            if bcc_emails:
                msg['Bcc'] = ', '.join(bcc_emails)

            print(f"Sending email to: {to_email} with BCC: {', '.join(bcc_emails)}")
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
            subprocess.run(['python', 'doft_scraper.py'])
        except Exception as e:
            print(f"Error executing scraper script: {e}")

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

            email_present = data.get('email', 'n/a') != 'n/a' and data.get('email') is not None
            phone_present = data.get('phone', 'n/a') != 'n/a' and data.get('phone') is not None

            emojis = ""
            if email_present and phone_present:
                emojis = "🟩"
            elif email_present:
                emojis = "✉️"
            elif phone_present:
                emojis = "📞"

            email_subject = f"{emojis} - Bid: {data.get('price', 'n/a')} - Type: {data.get('truck_type', 'n/a')} - P.U. : {data.get('pickup_date', 'n/a')} - {data.get('pickup_address', 'n/a')} - D.O.: {data.get('drop_address', 'n/a')} - Miles: {data.get('distance', 'n/a')} - Ib: {data.get('weight', 'n/a')} - Ref: {data.get('docket', 'n/a')} - {data.get('company', 'n/a')}"
            email_content = self.format_email_template(data)
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.send_email_batch, sender_details, [smtp_server] * len(sender_details), [smtp_port] * len(sender_details), [recipient_email] * len(sender_details), [bcc_list] * len(sender_details), [email_subject] * len(sender_details), [email_content] * len(sender_details))

            time.sleep(self.send_interval)

    def start_click(self):
        self.send_interval = int(self.interval_entry.get())
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.stop_event.clear()

        threading.Thread(target=self.start_sending_emails, args=(self.smtp_server, self.smtp_port)).start()

    def stop_click(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.stop_event.set()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    email_sender = EmailSender()
    email_sender.run()
