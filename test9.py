import time
from doft_scraper import DoftScraper

scraper = DoftScraper(r"D:\\BHaSH\\GHub\\fl\\switch_hayes\\chromedriver.exe", "doft_details.txt")
scraper.setup_driver()
scraper.read_credentials()
scraper.login()

start = time.time()
i = 0
while i < 3:
    scraper.extract_data()
    scraper.driver.refresh()
    i += 1
end = time.time()

print(f"Time taken: {end - start}")
scraper.quit_driver()
