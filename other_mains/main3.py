import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os

# Function to read CSV file
def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Function to save sender details to a text file
def save_sender_details(email, app_password):
    file_name = 'sender_details.txt'
    with open(file_name, 'w') as f:
        f.write(f"{email}    {app_password}")
    print(f"Sender details saved to {file_name}")

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
def send_email(gmail_user, gmail_pass, to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))  # Set email body as HTML

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to start sending emails
def start_sending_emails(recipient_email, stop_event, cli_process):
    global df, sample_gmail_user, sample_gmail_pass

    if recipient_email.strip() == "":
        messagebox.showwarning("Warning", "Please enter a recipient email address.")
        return

    df = read_csv_file('scraped_data.csv')

    if df is not None:
        num_rows = 10
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(0, len(df), num_rows):
                if stop_event.is_set():
                    break
                email_content = format_email_template(df.iloc[i:i+num_rows].to_dict('records'))
                futures.append(executor.submit(send_email, sample_gmail_user, sample_gmail_pass, recipient_email, 'Your Subject', email_content))
                print(email_content, file=cli_process.stdin)
                time.sleep(1)  # Adjust the interval between emails as needed
            for future in futures:
                future.result()  # Ensure all emails are sent before proceeding
        print("Email sending stopped.")
    else:
        messagebox.showwarning("Warning", "Failed to load data from scraped_data.csv.")

# Function to stop sending emails
def stop_sending_emails(stop_event):
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Function to handle Start button click
def start_sending_click():
    recipient_email = recipient_email_entry.get()
    cli_process = subprocess.Popen(["python", "cli_display.py"], stdin=subprocess.PIPE, text=True)
    threading.Thread(target=start_sending_emails, args=(recipient_email, stop_event, cli_process), daemon=True).start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# GUI setup
def main():
    global root, sample_gmail_user, sample_gmail_pass, start_button, stop_button, recipient_email_entry, stop_event

    root = tk.Tk()
    root.title("Email Sender")

    # Sample variables
    sample_gmail_user = 'dmarketer161@gmail.com'
    sample_gmail_pass = 'cyho cgkc evfk pljl'

    # Save sender details to a text file
    save_sender_details(sample_gmail_user, sample_gmail_pass)

    # Label and Entry for recipient email
    recipient_email_label = tk.Label(root, text="Recipient Email:")
    recipient_email_label.pack(pady=10)
    recipient_email_entry = tk.Entry(root, width=50)
    recipient_email_entry.pack()

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
