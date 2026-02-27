from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1400,900")
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari/537.36"
)

driver = webdriver.Chrome(options=opts)
driver.get("https://www.baseball-almanac.com/yearmenu.shtml")
print("TITLE:", driver.title)
print("URL:", driver.current_url)
driver.quit()
