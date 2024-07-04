import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
import threading
import time
import subprocess

# Global variables
stop_event = threading.Event()
send_interval = 6  # Interval in seconds between sending emails
scrape_interval = 5  # Interval in seconds to execute the scraper script

# Function to read email addresses and passwords from sender_details.txt
def read_sender_details(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            sender_details = [tuple(line.strip().split(', ')) for line in lines]
        return sender_details
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Function to read email addresses from a text file
def read_email_list(file_path):
    try:
        with open(file_path, 'r') as f:
            emails = [line.strip() for line in f.readlines()]
        return emails
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

# Function to format email content
def format_email_template(data):
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

# Function to send email
def send_email(gmail_user, gmail_pass, to_email, bcc_emails, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
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

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, [to_email] + bcc_emails, msg.as_string())
        print(f"Email sent to {to_email} with BCC to {', '.join(bcc_emails)}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to execute scraper script
def run_scraper_script():
    try:
        while True:
            subprocess.run(['python', 'doft_scraper.py'])
            time.sleep(scrape_interval)
    except Exception as e:
        print(f"Error executing scraper script: {e}")

# Function to start sending emails
def start_sending_emails():
    sender_details = read_sender_details('sender_details.txt')
    bcc_list = read_email_list('bcc_list.txt')
    recipient_email = read_email_list('recipient_email.txt')[0]  # Assuming there is only one recipient email but multiple BCC and sender emails   

    if not sender_details or not recipient_email:
        print("Failed to load email details.")
        return

    while not stop_event.is_set():
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

        email_content = format_email_template(data)  # Format data into email content

        for sender_email, sender_pass in sender_details:
            send_email(sender_email, sender_pass, recipient_email, bcc_list, email_subject, email_content)
            print(f"Sending data to {recipient_email} with BCC to {', '.join(bcc_list)}")
        
        time.sleep(send_interval)

    print("Email sending stopped.")

# Function to stop sending emails
def stop_sending_emails():
    stop_event.set()

# Function to handle Start button click
def start_click():
    threading.Thread(target=start_sending_emails, daemon=True).start()
    threading.Thread(target=run_scraper_script, daemon=True).start()  # Start scraper script concurrently
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# Function to handle Stop button click
def stop_click():
    stop_sending_emails()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Email Sender")

start_button = tk.Button(root, text="Start Sending", command=start_click)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Sending", command=stop_click, state=tk.DISABLED)
stop_button.pack(pady=10)

root.mainloop()
