import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.options import Options
from pprint import pprint


# options = Options()
# options.add_argument("--headless")
driver = uc.Chrome()


def get_html(url: str):
    # try:
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = driver.page_source
    return html
    # except TypeError:
    #     get_html(url)


async def get_info_token(url: str) -> dict:
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pprint(soup)
