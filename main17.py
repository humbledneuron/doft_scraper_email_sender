import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import os
from tkinter import filedialog
import subprocess

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
def format_email_template(data_list):
    def bold(text):
        return f"<strong>{text}</strong>"

    email_content = []
    for data in data_list:
        email_present = data.get('email', 'n/a') != 'n/a' and pd.notna(data.get('email'))
        phone_present = data.get('phone', 'n/a') != 'n/a' and pd.notna(data.get('phone'))

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
        fifth_line = f"Origin (zip (if/app.)): {bold(data.get('pickup_address', 'n/a'))} - Pick up date/ time: {bold(data.get('pickup_date', 'n/a'))} - Pick Up Hours: {bold(data.get('pickup_date', 'n/a'))} - Dock Hours: {bold(data.get('Dock Hours', 'n/a'))}"
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

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, [to_email] + bcc_emails, msg.as_string())
        print(f"Email sent to {to_email} with BCC to {', '.join(bcc_emails)}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to start sending emails
def start_sending_emails(stop_event):
    global bcc_list, recipient_email, sender_details

    if recipient_email.strip() == "":
        messagebox.showwarning("Warning", "Please enter a recipient email address.")
        return

    # Example of calling the scraper script and fetching data
    try:
        # Assuming doft_scraper.py outputs data to scraped_data.json
        subprocess.run(["python", "doft_scraper.py"])  # Modify as per your scraper script execution
        df = pd.read_json("scraped_data.json", orient='index')  # Load data from the output JSON file with 'index' orientation
    except Exception as e:
        print(f"Failed to fetch data from scraper: {e}")
        return


    email_subject = 'oooo \n iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii \n  oooooooooooooooooooooooooooooooo \n iiiiiii'

    if not df.empty:
        num_rows = 10
        for sender_email, sender_pass in sender_details:
            for i in range(0, len(df), num_rows):
                if stop_event.is_set():
                    break
                email_content = format_email_template(df.iloc[i:i+num_rows].to_dict('records'))
                send_email(sender_email, sender_pass, recipient_email, bcc_list, email_subject, email_content)
                print(f"Sending data to {recipient_email} with BCC to {', '.join(bcc_list)}")
                print(email_content)
                time.sleep(1)  # Adjust the interval between emails as needed
            if stop_event.is_set():
                break
            time.sleep(120)  # Wait 120 seconds before sending the next batch

        print("Email sending stopped.")
        messagebox.showinfo("Success", f"All emails have been successfully sent to {recipient_email} with BCC to {', '.join(bcc_list)}")
        time.sleep(60)  # Wait for 1 minute after completion
    else:
        messagebox.showwarning("Warning", "Failed to load data from scraper output.")

# Function to stop sending emails
def stop_sending_emails(stop_event):
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Function to handle Start button click
def start_sending_click():
    threading.Thread(target=start_sending_emails, args=(stop_event,), daemon=True).start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# GUI setup
def main():
    global root, start_button, stop_button, stop_event
    global sender_details, bcc_list, recipient_email

    root = tk.Tk()
    root.title("Email Sender")

    # Load sender details, BCC list, and recipient email from text files
    sender_details = read_sender_details('sender_details.txt')
    bcc_list = read_email_list('bcc_list.txt')
    recipient_email = read_email_list('recipient_email.txt')[0]  # Assuming there is only one recipient email but multiple BCC and sender emails   

    if not sender_details:
        messagebox.showwarning("Warning", "Failed to load sender email details.")
        return
    if not recipient_email:
        messagebox.showwarning("Warning", "Failed to load recipient email address.")
        return
    if not bcc_list:
        messagebox.showwarning("Warning", "Failed to load bcc email address.")
        return

    # Buttons
    start_button = tk.Button(root, text="Start Sending", command=start_sending_click)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Sending", command=lambda: stop_sending_emails(stop_event), state=tk.DISABLED)
    stop_button.pack(pady=10)

    # Event to stop sending emails
    stop_event = threading.Event()

    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
