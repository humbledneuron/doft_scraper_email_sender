import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
import threading
import time

# Function to read CSV files
def read_csv_files(file_paths):
    dfs = []
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            dfs.append(df)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return None

# Function to save recipient email to a text file
def save_recipient_email(email):
    file_name = 'recipients_gmail.txt'
    with open(file_name, 'w') as f:
        f.write(email)
    print(f"Recipient email saved to {file_name}")

# Function to save sender details to a text file
def save_sender_details(email, app_password):
    file_name = 'sender_details.txt'
    with open(file_name, 'w') as f:
        f.write(f"Sender Gmail: {email}\nApp Password: {app_password}")
    print(f"Sender details saved to {file_name}")

# Function to format email content
def format_email_template(data_list):
    def bold(text):
        return f"<strong>{text}</strong>"

    email_content = ""
    for data in data_list:
        # Set emojis based on conditions
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

        email_content += f"""
        <div style="text-align: center;">{first_line}</div>
        <div style="text-align: center;">{second_line}</div>
        {third_line}<br>
        {fourth_line}<br>
        {fifth_line}<br><br>
        """
    email_template = f"""
    <html>
    <body style="font-family: Verdana; font-size: xx-small;">
    <em>
    {email_content}
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

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to start sending emails
def start_sending_emails():
    global df, sample_gmail_user, sample_gmail_pass, recipient_email, stop_event

    if df is not None:
        num_rows = 10
        for i in range(0, len(df), num_rows):
            if stop_event.is_set():
                break
            email_content = format_email_template(df.iloc[i:i+num_rows].to_dict('records'))
            send_email(sample_gmail_user, sample_gmail_pass, recipient_email, 'Your Subject', email_content)
            time.sleep(5)  # Adjust the interval between emails as needed
        print("Email sending stopped.")
    else:
        messagebox.showwarning("Warning", "No data found or sending already in progress.")

# Function to stop sending emails
def stop_sending_emails():
    global stop_event
    
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Email Sender")

# Sample variables
sample_gmail_user = 'dmarketer161@gmail.com'
sample_gmail_pass = 'cyho cgkc evfk pljl'
csv_file_paths = ['scraped_data.csv', 'old_data.csv']
df = read_csv_files(csv_file_paths)
recipient_email = 'bmujtaba1009@gmail.com'

# Save recipient email to a text file
save_recipient_email(recipient_email)

# Save sender details to a text file
save_sender_details(sample_gmail_user, sample_gmail_pass)

# Buttons
start_button = tk.Button(root, text="Start Sending", command=start_sending_emails)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Sending", command=stop_sending_emails, state=tk.DISABLED)
stop_button.pack(pady=10)

# Start the GUI main loop
stop_event = threading.Event()
root.mainloop()
