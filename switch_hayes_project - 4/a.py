import re

stri = "07/05/2024 - 10:50 PM"
a = re.sub(r'^.*?-', '', stri)
print(a)

c = 13
print("%.2f"%c)