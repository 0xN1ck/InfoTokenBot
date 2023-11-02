import requests, asyncio, time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import ChromeOptions
from pprint import pprint
from dexscreener import DexscreenerClient
# 0x1b4c961a58578b5271f4d8ccfb907f0a498dce9f

# options = ChromeOptions()
# options.add_argument("--headless=new")
# options.add_argument('--auto-open-devtools-for-tabs')
# options.add_argument("--disable-blink-features=AutomationControlled")
# driver = uc.Chrome(
#     options=options
# )


# async def get_html(url: str):
    # try:
    # driver.get(url)
    # time.sleep(20)
    # await asyncio.sleep(20)
    # driver.save_screenshot("datacamp.png")
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # html = driver.page_source
    # return html
    # except TypeError:
    #     get_html(url)


async def get_info_token(token: str) -> dict:
    # html = await get_html(url)
    # soup = BeautifulSoup(html, 'lxml')
    # pprint(soup)
    client = DexscreenerClient()
    # pair = client.get_token_pair("harmony", "0xcd818813f038a4d1a27c84d24d74bbc21551fa83")
    # pairs = client.get_token_pairs("7qbrf6ysyguluvs6y1q64bdvrfe4zcuuz1jrdovnujnm")
    # print(pairs)
    search = client.search_pairs(token)
    print(search)
