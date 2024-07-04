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

# Function to read CSV file
def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

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
        email_present = data.get('EMAIL', 'n/a') != 'n/a' and pd.notna(data.get('EMAIL'))
        phone_present = data.get('PHONE', 'n/a') != 'n/a' and pd.notna(data.get('PHONE'))

        emojis = ""
        if email_present and phone_present:
            emojis = "🟩"
        elif email_present:
            emojis = "✉️"
        elif phone_present:
            emojis = "📞"

        first_line = f"{emojis} - {bold(data.get('Price', 'n/a'))} - {bold(data.get('TRUCK_TYPE', 'n/a'))} - {bold(data.get('PICKUP_DATE', 'n/a'))} - {bold(data.get('ORIGIN', 'n/a'))} - {bold(data.get('DESTINATION', 'n/a'))} - {bold(data.get('DISTANCE', 'n/a'))} - {bold(data.get('WEIGHT', 'n/a'))} - {bold(data.get('REF', 'n/a'))}"
        second_line = f"Age Posted: {bold(data.get('AGE', 'n/a'))} (C.S.T) - {bold(data.get('LENGTH', 'n/a'))}"
        third_line = f"Origin (zip (if/app.)): {bold(data.get('PICKUP_ZIP', 'n/a'))} - Pick up date/ time: {bold(data.get('PICKUP_DATE', 'n/a'))} - Pick Up Hours: {bold(data.get('Pick Up Hours', 'n/a'))} - Dock Hours: {bold(data.get('Dock Hours', 'n/a'))} - Destination (zip (if/app.)): {bold(data.get('DESTINATION_ZIP', 'n/a'))} - Drop off date/ time: {bold(data.get('DROPOFF_DATE', 'n/a'))}"
        fourth_line = f"Price: {bold(data.get('Price', 'n/a'))} - Total trip mileage: {bold(data.get('DISTANCE', 'n/a'))} - Est. Fuel Costs: {bold(data.get('FUEL', 'n/a'))} - Full/ partial: {bold(data.get('LOAD_TYPE', 'n/a'))} - Weight: {bold(data.get('WEIGHT', 'n/a'))} - Commodity: {bold(data.get('Commodity', 'n/a'))} - DIMS: {bold(data.get('DIMS', 'n/a'))} - Comments: {bold(data.get('Comments', 'n/a'))}"
        fifth_line = f"Company: {bold(data.get('COMPANY', 'n/a'))} - Address: {bold(data.get('Address', 'n/a'))} - DOT: {bold(data.get('DOT', 'n/a'))} - Docket: {bold(data.get('Docket', 'n/a'))} - Contact: {bold(data.get('CONTACT', 'n/a'))} - Phone: {bold(data.get('PHONE', 'n/a'))} - Fax: {bold(data.get('Fax', 'n/a'))} - Email: {bold(data.get('EMAIL', 'n/a'))} - Website: {bold(data.get('Website', 'n/a'))}"

        email_content.append(f"""
        <div style="text-align: center;">{first_line}</div>
        <div style="text-align: center;">{second_line}</div>
        {third_line}<br>
        {fourth_line}<br>
        {fifth_line}<br><br>
        """)
        
    email_template = f"""
    <html>
    <body style="font-family: Verdana; font-size: xx-small;">
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

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, [to_email] + bcc_emails, msg.as_string())
        print(f"Email sent to {to_email} with BCC to {', '.join(bcc_emails)}")
    except Exception as e:
        print(f"Failed to send email: {e}")



# Function to start sending emails
def start_sending_emails(stop_event):
    global df, bcc_list, recipient_email, sender_details

    if recipient_email.strip() == "":
        messagebox.showwarning("Warning", "Please enter a recipient email address.")
        return

    df = read_csv_file('scraped_data.csv')
    email_subject = 'oooo \n iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii \n  oooooooooooooooooooooooooooooooo \n iiiiiiiii'
    if df is not None:
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
        messagebox.showwarning("Warning", "Failed to load data from scraped_data.csv.")

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
