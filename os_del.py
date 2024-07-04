#import os
#from datetime import date

#today  = date.today()
#if today == date(2024, 7, 11):
#    print("Today is July 11, 2024  so boom")
#    #os.remove('C:'Program Files)
#else:
#    print(f"Today is {date.today()}")

#print("Today is July 4, 2024") if date.today() == date(2024, 7, 3) else print(f"{date.today()}")
#os.remove('C:'Program Files)

    
import requests
import os

#r = requests.get("https://github.com/humbledneuron/javaProjs/blob/main/abc.txt")
r = requests.get("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/abc.txt")
status = r.content.decode('utf-8').strip()
print(status) if status == "yes" else print("no")
cwd = os.getcwd()
rmd = f"{cwd}\\removing1.txt"
print(rmd)
os.remove(rmd)

"""
r = requests.get("https://raw.githubusercontent.com/Kichi779/Spotify-Streaming-Bot/main/version.txt")
        remote_version = r.content.decode('utf-8').strip()
        local_version = open('version.txt', 'r').read().strip()
        if remote_version != local_version:
"""
