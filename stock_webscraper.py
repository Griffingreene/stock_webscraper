import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


def web_content_div(web_content, class_path, tag_type):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        tags = web_content_div[0].find_all(tag_type)
        texts = [tag.get_text() for tag in tags]
    except IndexError:
        texts = []
    return texts


def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, "D(ib) Mend(20px)",'fin-streamer')
        if texts != []:
            price, change, pct_change = texts[0], texts[1], texts[2]
        else:
            pric, change, pct_change = [], [], []

        texts = web_content_div(web_content,"D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)",'td')
        if texts != []:
            for count, vol in enumerate(texts):
                if vol == 'Volume':
                    volume = texts[count + 1]

        else:
            volume = []

        pattern = web_content_div(web_content, 'Fz(xs) Mb(4px)','span')
        try:
            latest_pattern = pattern[0]
        except IndexError:
            latest_pattern = []

        texts = web_content_div(web_content, "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)",'td')

        if texts != []:
            for count, target in enumerate(texts):
                # print(target)
                if target == '1y Target Est':
                    try:
                        one_year_target = texts[count+1]
                    except IndexError:
                        one_year_target = []
        else:
            one_year_target = []


    except ConnectionError:
        price, change, pct_change, volume, latest_pattern, one_year_target = [], [], [], [], [], []

    return price, change, pct_change, volume, latest_pattern, one_year_target


stock_codes = ['BRK-B', 'AMD', 'TSLA', 'MARA', 'NIO', 'AAPL']



while True:
    stock_info = []
    col = []
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
    for code in stock_codes:
        stock_price, price_change, pct_change, volume, latest_pattern, one_year_target = real_time_price(code)

        stock_info.append(stock_price)
        stock_info.extend([price_change])
        stock_info.extend([pct_change])
        stock_info.extend([volume])
        stock_info.extend([latest_pattern])
        stock_info.extend([one_year_target])

        # stock_info.extend([stock_price, price_change, pct_change, volume, latest_pattern, one_year_target])

    col = [time_stamp]
    col.extend(stock_info)
    df = pd.DataFrame(col)
    df.T
    with open(str(time_stamp[0:11]) + '_stock_data.csv', 'w') as csv_file:
        df.to_csv(csv_file, mode='a', header=False)

    print(col)
