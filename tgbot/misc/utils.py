from pprint import pprint
from numpy import format_float_positional
from dexscreener import DexscreenerClient
from bs4 import BeautifulSoup
import cloudscraper
import re
import requests
import json

# from etherscan import Etherscan
# import etherscan.tokens as token_lib
from etherscan.contracts import Contract

# 0x1b4c961a58578b5271f4d8ccfb907f0a498dce9f
TOKEN_ETHERSCAN = 'JKABW46GB1CSXXC413S9KP48WT8VU728X5'


async def get_response(url):
    post_body = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }
    response = requests.post('http://localhost:8191/v1', headers={'Content-Type': 'application/json'}, json=post_body)

    response = json.loads(response.text)
    return response


async def replace_symbol_html(string):
    pattern = r'[<>]'
    replaced_string = re.sub(pattern, lambda match: '&lt;' if match.group() == '<' else '&gt;', string)
    return replaced_string


async def extract_links(text):
    pattern = (r'(?:http[s]?://|www\.|t.me/|twitter.com/)'
               r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    link_pattern = re.compile(pattern)
    links = re.findall(link_pattern, text)

    results = {
        "Telegram": [],
        "Twitter": [],
        "Website": []
    }
    for link in links:
        if "t.me" in link.lower():
            results["Telegram"].append(link)
        elif "twitter" in link.lower():
            results["Twitter"].append(link)
        else:
            results["Website"].append(link)

    for key in results.keys():
        if len(results[key]) == 0:
            results[key].append("Информация отсутствует")
        results[key] = ", ".join(results[key])

    return results


async def get_all_info_token(token: str):
    info_dex = await get_info_from_dexscreener(token)
    info_eth = await get_info_from_etherscan(info_dex['pair'].base_token.address)
    info_sniffer = await get_info_from_tokensniffer(info_dex['pair'].base_token.address)

    results = (f"<b>{info_dex['name']}</b>  \n\n"
               f"<b>Оценка:</b>  \n\n"
               f"<b>Концепция:</b>  \n\n"
               f"<b>Идея:</b>  \n\n"
               f"<b>Монета:</b>  \n"
               f"Держатели: {info_eth['holders']}\n"
               f"Цена: ${format_float_positional(info_dex['price'], trim='-').replace('.', ',')}\n"
               f"Текущий пул: ${str(info_dex['liq']).replace('.', ',')}\n"
               f"Начальная ликвидность: {info_sniffer['liq_start']}\n"
               f"Лок: {info_sniffer['lock']}\n\n"
               f"<b>Текущее состояние:</b>  \n"
               f"Вышли: {info_dex['date_start']} {info_dex['time_start']}\n"
               f"ТА: \n\n"
               f"<b>Социальность:</b>  \n"
               f"TELEGRAM:\n"
               f"TWITTER:\n"
               f"WEBSITE:\n\n"
               f"<b>Рекомендации:</b>  \n\n"
               f"<b>Ссылки:</b>  \n"
               f"DEX:\n"
               f"{info_dex['dex_url']}\n"
               f"ETHERSCAN:\n"
               f"{info_eth['url']}\n"
               f"Telegram: {info_eth['links']['Telegram']}\n"
               f"Twitter: {info_eth['links']['Twitter']}\n"
               f"Website: {info_eth['links']['Website']}\n\n"
               f"")

    return results

    # api = Contract(address=info_dex['pair'].base_token.address, api_key=TOKEN_ETHERSCAN)
    # sourcecode = api.get_sourcecode()
    # # TODO: make this return something pretty
    # pprint(sourcecode)


async def get_info_from_dexscreener(token: str):
    # token = "0x1B4c961a58578B5271f4D8CcFb907f0a498DCE9F"
    # token = "0xaf3df2cc9f0227b9e45543df3d3770f450e80db8" # kitty
    client = DexscreenerClient()
    pair = client.get_token_pair("ethereum", token)
    print(pair)
    name = pair.base_token.name
    price = pair.price_usd
    liq = pair.liquidity.usd
    date_start = pair.pair_created_at.date()
    time_start = pair.pair_created_at.time()
    dex_url = pair.url

    return {
        "name": name,
        "price": price,
        "liq": liq,
        "date_start": date_start,
        "time_start": time_start,
        "dex_url": dex_url,
        "pair": pair
    }


async def get_info_from_etherscan(token: str):
    scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0', })
    url = f"https://etherscan.io/token/{token}#balances"
    response = scraper.get(url)
    # response = await get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    holders = (soup.
               find("div", {"id": "ContentPlaceHolder1_tr_tokenHolders"}).
               find('div', {"class": "d-flex flex-wrap gap-2"}).text.strip())
    code = soup.find('div', {"id": "dividcode"})
    links = await extract_links(code.getText())

    return {
        "holders": holders,
        "links": links,
        "url": url,
    }


async def get_info_from_tokensniffer(token: str):
    url = f"https://tokensniffer.com/token/eth/{token}"
    results = {
        "liq_start": "Информация отсутствует",
        "lock": "Информация отсутствует",
    }
    response = await get_response(url)
    soup = BeautifulSoup(response['solution']['response'], 'lxml')
    table = soup.find_all('table', {'class': 'Home_compact__2top4'})
    if len(table) == 0:
        return {
            "liq_start": "Информация отсутствует",
            "lock": "Информация отсутствует"
        }
    for element in table:
        states = element.find_all('td', {'class': 'Home_mono2__1lWiC'})
        for state in states:
            # print(state.text)
            if state.text.strip() == "Adequate initial liquidity":
                results["liq_start"] = state.next.next.text
                results["liq_start"] = await replace_symbol_html(results["liq_start"])
            elif "At least 95% of liquidity burned/locked for at least 15 days" in state.text.strip():
                lock_text = state.next.next.next.text
                pattern = r' in Unicrypt\s+until \d{1,2} \w{3} \d{4} \d{2}:\d{2}:\d{2} GMT'
                lock_text = re.sub(pattern, '', lock_text)
                results["lock"] = lock_text
                if not re.search(r"\d+(\.\d+)?\%", results["lock"]):
                    results["lock"] = "Информация отсутствует"
                results["lock"] = await replace_symbol_html(results["lock"])

    return results

    # keys = ['liq_start', 'lock']
    # values = [i.text if i else 'Информация отсутствует' for i in table.find_all('div', {'class': 'Home_note__1UGB7'})[1:]]
    # try:
    #     liq_start = table.find_all('div', {'class': 'Home_note__1UGB7'})[-2].text if table.find_all('div', {'class': 'Home_note__1UGB7'})[-2] else 'Информация отсутствует'
    # except:
    #     liq_start = 'Информация отсутствует'
    # try:
    #     lock = table.find_all('div', {'class': 'Home_note__1UGB7'})[-1].text if table.find_all('div', {'class': 'Home_note__1UGB7'})[-1] else 'Информация отсутствует'
    # except:
    #     lock = 'Информация отсутствует'
    # pattern = r' in Unicrypt  until \d{1,2} \w{3} \d{4} \d{2}:\d{2}:\d{2} GMT'
    # lock = re.sub(pattern, '', lock)
    # # results = dict(zip(keys, [re.sub(pattern, '', value) for value in values]))




    # results = {
    #     "liq_start": liq_start,
    #     "lock": lock
    # }
    # return results
