# cli_display.py
import sys

for line in sys.stdin:
    print(line, end='')


# this cli_displayer.py will be called by our original program

# import sys
# import codecs

# def display_data(email_content):
#     print(email_content)
#     sys.stdout.flush()

# if __name__ == "__main__":
#     sys.stdin = codecs.getreader('utf-8')(sys.stdin.detach())
#     while True:
#         try:
#             line = sys.stdin.readline()
#             if not line:
#                 break
#             display_data(line.strip())
#         except KeyboardInterrupt:
#             break
