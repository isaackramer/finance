import pandas as pd
from datetime import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar

def earnings_calendar(portfolio_csv):

    #import tickers
    portfolio = pd.read_csv(portfolio_csv, index_col=0)
    tickers = list(portfolio.index.unique()) 
       
    # initiate the earnings calendar scrapper
    yec = YahooEarningsCalendar()
    
    # dataframe to hold values
    df = pd.DataFrame(index=tickers,
                      columns = ["Next_Earnings"])
    
    # get next earnings date    
    for ticker in tickers:
        try:
            # if next earnings date announced
            earnings_date = yec.get_next_earnings_date(ticker)
            earnings_date = datetime.utcfromtimestamp(earnings_date).strftime('%Y-%m-%d %H:%M:%S')
            df.loc[ticker, 'Next_Earnings'] = earnings_date
        except:
            # if next earnings date has not been announced
            df.loc[ticker, 'Next_Earnings'] = "TBA"
            
    # sort chronologically 
    df = df.sort_values(by=['Next_Earnings'])
    
    return df


