import requests
from bs4 import BeautifulSoup as bs
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def figure_3(stock, save):
    # import data from macrotrends.net
    r = requests.get('https://www.macrotrends.net/stocks/charts/'+stock+'/company/cash-flow-statement')
    p = re.compile(r' var originalData = (.*?);\r\n\r\n\r',re.DOTALL)
    data = json.loads(p.findall(r.text)[0])
    headers = list(data[0].keys())
    headers.remove('popup_icon')
    result = []
    for row in data:
        soup = bs(row['field_name'])
        field_name = soup.select_one('a, span').text
        fields = list(row.values())[2:]
        fields.insert(0, field_name)
        result.append(fields)
    pd.option_context('display.max_rows', None, 'display.max_columns', None)
    df = pd.DataFrame(result, columns = headers)
    
    # transpose dataframe so that rows are years
    df = df.T
    
    # make first row the header
    new_header = df.iloc[0] 
    df = df[1:]
    df.columns = new_header 
    
    # reverse order so that dataframe is in chronological order
    df = df.iloc[::-1]
    
    # convert columns to numeric types
    cols = df.columns
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    
    # make index column only two diger year name
    df.index = df.index.str.slice(start=2,stop=4)
    
    # begin plotting
    plt.style.use('isaac_style.mplstyle')
    plt.ion()
    plt.clf()
    fig, ax = plt.subplots(num=1, nrows=2, ncols=2)
    fig.subplots_adjust(left=0.06, right=0.95, top=0.95, bottom=0.05,
                        hspace=0.35, wspace=0.35)
    fig.set_size_inches(10,7.5)
    
    # bar width
    bar_w = 0.90
    
    # plot cash flow from operating activites
    ax[0,0].bar(x=df.index,
                height=df['Cash Flow From Operating Activities'],
                color = np.where(df['Cash Flow From Operating Activities']>0,
                                 "green", "red"),
                width = bar_w)
    ax[0,0].set(title="Cash Flow From Operating Activities")
    
    
    # plot cash from investing activities 
    ax[0,1].bar(x=df.index,
                height=df['Cash Flow From Investing Activities'],
                color = np.where(df['Cash Flow From Investing Activities']>0,
                                 "red", "green"),
                width = bar_w)
    ax[0,1].set(title="Cash Flow From Investing Activities")
    
    # plot cash from financing activites
    ax[1,0].bar(x=df.index,
                height=df['Cash Flow From Financial Activities'],
                color = np.where(df['Cash Flow From Financial Activities']>0,
                                 "red", "green"),
                width = bar_w)
    ax[1,0].set(title="Cash Flow From Financial Activities")
    
    # Pretax Income
    ax[1,1].bar(x=df.index,
                height=df['Net Cash Flow'],
                color = "black",
                width = bar_w)
    ax[1,1].set(title="Net Cash Flow")
    
    if save == True:    
        fig.savefig("./portfolio/"+stock+"/figure_3.pdf")
    
figure_3('MLI', True)
