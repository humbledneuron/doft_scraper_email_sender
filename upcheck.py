# this check if site is up or down for every 300 secs or 5 mind
# and in the end it'll pop a new windows if the site is up

import requests # pip install requests
import time
from tkinter import messagebox
# import winsound # pip install winaudio || uncomment for a beep and this works only on windows  


def check_site(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

   
def main():

    # site_url = input("Enter the site URL (google.com) : ") 
    # site_url = 'https://' + site_url #if not site_url.startswith("http") # or url.startswith("http") else url
    site_url = "https://raw.githubusercontent.com/tmofsb/cc/main/new.txt"
    while True:
        if check_site(site_url):
            print(f"{site_url} is up.")
            # winsound.Beep(500, 5000) # uncomment for a beep and this works only on windows  
            messagebox.showwarning("Sucess", f"The site {site_url} is back online.")
            # winsound.PlaySound("path/to/custom_sound.wav", winsound.SND_FILENAME) # if you want a custom music
            return
        
        else:
            print(f"{site_url} is down.")
        time.sleep(10)  # Check every 300 seconds


if __name__ == "__main__":
    main()