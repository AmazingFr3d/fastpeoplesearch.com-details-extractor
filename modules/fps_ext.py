import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import datetime


def fps_req(name: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
                      'Safari/537.36'}
    page = 1

    result = []

    while True:
        url = f'https://www.fastpeoplesearch.com/name/{name.lower()}/page/{page}'
        print(name)
        print(url)

        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.content, "html.parser")
        for person in soup.find_all("div", class_="card-block"):
            dom = etree.HTML(str(person))

            res_dict = {
                'name': person.find("span", class_="larger").text.strip(),
                'phone_number': "".join(dom.xpath("//strong/a[@class='nowrap']/text()"))
            }
            result.append(res_dict)
            print(res_dict)

        if soup.find("span", class_="fa-angle-double-right"):
            page += 1
        else:
            break

    return result


def multi_req(names: list):
    result = []
    for name in names:
        result.extend(fps_req(name))

    date_time = datetime.datetime.now()
    dt = date_time.strftime("%d_%m_%y_%H_%M")
    df = pd.DataFrame(result)
    df.to_csv(f'users_scraped_frm_fps_{dt}.csv', index=False)



