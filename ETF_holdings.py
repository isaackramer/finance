# https://stackoverflow.com/questions/64908086/using-python-to-identify-etf-holdings
import requests
import re
import pandas as pd

def get_holdings(ETF):
    url = "https://www.zacks.com/funds/etf/{}/holding"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}
    with requests.Session() as req:
        req.headers.update(headers)
        r = req.get(url.format(ETF))
        holdings = re.findall(r'etf\\\/(.*?)\\', r.text)
        df = pd.DataFrame(data={"holdings": holdings})        
    return holdings
            

