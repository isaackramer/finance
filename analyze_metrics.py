import pandas as pd
from finvizfinance.quote import finvizfinance

def metrics(stock, save):

    # get data
    fin_stock = finvizfinance(stock)
    metrics = fin_stock.TickerFundament()
    
    # dataframe to hold values
    df = pd.DataFrame(index=[stock],
                      columns = list(metrics.keys()))
    
    # add data to dataframe
    df.loc[stock] = metrics
    
    # keep only relevant columns
    df = df[['Company','Sector', 'Price',  'Target Price',
             'P/E', 'P/B', 'Debt/Eq', 'P/S', 'Market Cap', 'PEG',
             'Dividend %', 'Beta', 'Forward P/E', 'Sales Q/Q',
             'EPS Q/Q', 'EPS (ttm)',  'EPS next Y',  'EPS next 5Y',
             'ROA', 'Cash/sh', 'ROE', 'P/FCF', 'ROI',
             'Insider Own',  'Inst Own']]
        
    # parse dataframe into numeric types
    df['Dividend %'] = df['Dividend %'].str.replace('%', '')
    df['ROE'] = df['ROE'].str.replace('%', '')
    df['ROI'] = df['ROI'].str.replace('%', '')
    df['EPS Q/Q'] = df['EPS Q/Q'].str.replace('%', '')
    df['Sales Q/Q'] = df['Sales Q/Q'].str.replace('%', '')
    df['EPS next Y'] = df['EPS next Y'].str.replace('%', '')
    df['EPS next 5Y'] = df['EPS next 5Y'].str.replace('%', '')
    df['ROA'] = df['ROA'].str.replace('%', '')
    df['Insider Own'] = df['Insider Own'].str.replace('%', '')
    df['Inst Own'] = df['Inst Own'].str.replace('%', '')
    df['Market Cap'] = df['Market Cap'].str.replace('B', '')
    
    if save == True:
     df.to_csv("./portfolio/analyze_output/metrics.csv")
    
    return df
