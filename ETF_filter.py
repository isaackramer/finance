import pandas as pd
from ETF_holdings import get_holdings
from finvizfinance.quote import finvizfinance

def ETF_filter(ETF):
    # get holdings for ETF to analyze
    holdings = get_holdings(ETF)
    
    # use test case to get column values
    stock = finvizfinance('tsla')
    stats = stock.TickerFundament()
    
    # dataframe to hold values
    df = pd.DataFrame(index=holdings, columns = list(stats.keys()))
    
    # get data
    for ticker in holdings:
        try:
            stock = finvizfinance(ticker)
            stats = stock.TickerFundament()
            df.loc[ticker] = stats
        except:
            print(ticker+" ticker not found, continuing without")
        
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
    
    cols=[i for i in df.columns if i not in ["Company","Sector"]]
    for col in cols:
        df[col]=pd.to_numeric(df[col], errors='coerce')
    
    # Filter for companies which are quoted at low valuations 
    df_filter = df[(df['P/E'].astype(float)<30) &
                        (df['P/B'].astype(float) < 3) &
                        (df['Debt/Eq'].astype(float) < 2) &
                        (df['P/S'].astype(float) < 2) &
                        (df['Market Cap'].astype(float) > 2) &
                        (df['PEG'].astype(float) < 3)]
    
    return df_filter





