import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        fin_streams = web_content_div[0].find_all('fin-streamer')
        texts = [fin.get_text() for fin in fin_streams]
    except IndexError:
        texts = []
    return texts


def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, "D(ib) Mend(20px)")
        if texts != []:
            price, change, pct_change = texts[0], texts[1], texts[2]
        else:
            pric, change, pct_change = [], [], []

        texts = web_content_div(web_content,'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)')
        if texts != []:
            for count, vol in enumerate(texts):
                if vol == 'Volume':
                    volume = texts[count + 1]
        else:
            volume = []

        pattern = web_content_div(web_content, 'Fz(xs) Mb(4px)')
        try:
            latest_pattern = pattern[0]
        except IndexError:
            latest_pattern = []

        texts = web_content_div(web_content, "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)")
        if texts != []:
            for count, target in enumerate(texts):
                if target == '1y Target Est':
                    one_year_target = texts[count+1]
        else:
            one_year_target = []


    except ConnectionError:
        price, change, pct_change, volume, latest_pattern, one_year_target = [], [], [], [], [], []
    return price, change, pct_change, volume, latest_pattern, one_year_target


stock = ['BRK-B']
print(real_time_price('BRK-B'))
