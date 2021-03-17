import pandas_datareader as pdr
from datetime import datetime, timedelta
from dateutil.tz import gettz
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd
import math
import numpy as np

# function to get ticker data
def get(tickers, startdate, enddate):
  def data(ticker):
    return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
  datas = map (data, tickers)
  return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))
  
def portfolio_update(portfolio):
  
    # import data
    portfolio_data = pd.read_csv("./"+portfolio)
    portfolio_data['Trade_Date'] =  pd.to_datetime(portfolio_data['Trade_Date'],
                                                   format='%Y%m%d')
    # add time zone
    portfolio_data.Trade_Date = portfolio_data.Trade_Date.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')

    # unique tickers
    unique_symbols = portfolio_data.drop_duplicates(['Symbol'])
    
    # date of first investment
    purchase_date = unique_symbols.Trade_Date
    purchase_date = purchase_date.reset_index(drop=True)
    
    # get tickers for my stocks
    my_tickers = portfolio_data.Symbol.unique()
    my_companies = portfolio_data.Company.unique()
    
    # add SPY to ticker list -- to compare to S&P 500
    my_tickers = np.append(my_tickers, 'SPY')
    
    # import price history data
    all_data = get(my_tickers,
                   datetime(2015, 1, 1), 
                   pd.to_datetime("today"))
    # add time zone
    all_data.index = all_data.index.set_levels(all_data.index.levels[1].
                                               tz_localize(tz='US/Eastern'),
                                               level=1)
    
    # isolate the `Adj Close` values and transform the DataFrame
    daily_close = all_data[['Adj Close']].reset_index().pivot('Date',
                                                              'Ticker',
                                                              'Adj Close')
    daily_close_SPY = daily_close['SPY']
    
    # find percent change and cummulative return for SPY
    pct_change_SPY = daily_close_SPY.pct_change()
    pct_change_SPY.fillna(0, inplace=True)
    cum_return_SPY = (1 + pct_change_SPY).cumprod()
    
    # basic figure settings
    plt.style.use('isaac_style.mplstyle')
    plt.ioff()
    plt.clf()
    
    #subplot dimensions
    plt_width = math.floor(math.sqrt(len(my_tickers)))
    plt_length = math.ceil(len(my_tickers)/plt_width)
    num_plots = plt_width*plt_length
    extra_plots = num_plots - len(my_tickers) + 1
    
    # fig for cummulative returns
    CUM_fig, CUM = plt.subplots(figsize=(12,12),
                                num=3,
                                nrows=plt_length,
                                ncols=plt_width)
    CUM_fig.subplots_adjust(left=0.07,
                            right=0.98, 
                            top=0.90, 
                            bottom=0.055,
                            hspace=0.45, 
                            wspace=0.45)
    # delete extra subplots
    for ex in range(extra_plots):
        CUM_fig.delaxes(CUM[plt_length-1,
                            plt_width-1-ex])
    CUMr = CUM.ravel()
    
    
    # fig for cummulative returns since purchase
    CUM_zoom_fig, CUM_zoom = plt.subplots(figsize=(12,12),
                                          num=4,
                                          nrows=plt_length,
                                          ncols=plt_width,
                                          sharey = True)
    CUM_zoom_fig.subplots_adjust(left=0.07,
                                 right=0.98,
                                 top=0.90,
                                 bottom=0.055,
                                 hspace=0.45, 
                                 wspace=0.45)
    # delete extra subplots
    for ex in range(extra_plots):
        CUM_zoom_fig.delaxes(CUM_zoom[plt_length-1,
                                      plt_width-1-ex])
    CUM_zoomr = CUM_zoom.ravel()
    
    
    # fig for returns and portfolio value
    RET_fig, RET = plt.subplots(figsize=(12,4),
                                num=5, 
                                nrows=1, 
                                ncols=3)
    RET_fig.subplots_adjust(left=0.06, 
                            right=0.98, 
                            top=0.93, 
                            bottom=0.11,
                            hspace=0.4, 
                            wspace=0.25)
    (start, current, returns,
     returns_per_share, returns_per_dollar) = np.empty((5,
                                                        len(my_tickers)-1))
    
    
    # plot data by looping over subplots, calculate starting value and returns
    for ii in range(len(my_tickers)-1):
        
        # choose stock
        stock = my_tickers[ii]
        
        # performance since purchase
        daily_close_zoom = daily_close[(daily_close.index>
                                        (purchase_date[ii]-timedelta(days=1)))][stock]
        
        # calculate and plot cumulative returns 2015-present
        c_price = daily_close[stock]
        pct_change = c_price.pct_change()
        cum_return = (1 + pct_change).cumprod()
        CUMr[ii].plot(cum_return,
                      color = "black",
                      label = stock)
        CUMr[ii].plot(cum_return_SPY,
                      color = "grey",
                      label = 'S&P 500')
        CUMr[ii].set(title = my_companies[ii])
        CUMr[ii].legend(loc="upper left")
        CUMr[ii].xaxis.set_major_locator(mdates.YearLocator(1))
        CUMr[ii].xaxis.set_major_formatter(DateFormatter("%y"))
        plt.setp(CUMr[ii].get_xticklabels(),
                 rotation=45,
                 ha='right') 
        
        # calculate and plot cumulative returns since purchase
        pct_change_zoom = daily_close_zoom.pct_change()
        cum_return_pur = (1 + pct_change_zoom).cumprod()
        cum_return_pur = cum_return_pur.fillna(1)
        
        closing_price_zoom_spy = daily_close[(daily_close.index>
                                              (purchase_date[ii]-
                                               timedelta(days=1)))]['SPY']
        pct_change_zoom_spy = closing_price_zoom_spy.pct_change()
        cum_return_pur_spy = (1 + pct_change_zoom_spy).cumprod()
        cum_return_pur_spy = cum_return_pur_spy.fillna(1)

        CUM_zoomr[ii].plot(cum_return_pur, 
                           color = "black", 
                           label = stock)
        CUM_zoomr[ii].plot(cum_return_pur_spy,
                           color = "grey",
                           label = 'S&P 500')
        CUM_zoomr[ii].set(title = my_companies[ii])
        CUM_zoomr[ii].legend(loc="upper left")
        CUM_zoomr[ii].xaxis.set_major_formatter(DateFormatter("%m-%d"))
        CUM_zoomr[ii].xaxis.set_major_locator(mdates.DayLocator((1,15)))
        plt.setp(CUM_zoomr[ii].get_xticklabels(),
                 rotation=45,
                 ha='right') 
        
    # calculate starting value and returns
    portfolio_data['starting_value'] =  (portfolio_data['Shares']*
                                         portfolio_data['Purchase_Price'])
    for jj in range(len(portfolio_data.index)):
        ticker = portfolio_data.loc[jj, 'Symbol']
        current_price = daily_close[ticker].iloc[-1]
        portfolio_data.loc[jj, 'current_value'] = (current_price*
                                                   portfolio_data.loc[jj,
                                                                      'Shares'])
        
    # consolidate data if a given ticker has been purhased on different dates
    consolidated = portfolio_data.groupby(['Symbol']).sum()
        
    returns = consolidated['current_value'] - consolidated['starting_value']
    returns_per_share = returns/consolidated['Shares']
    returns_per_dollar = returns/consolidated['starting_value']
    
    # returns plot
    bars = [returns, returns_per_share, returns_per_dollar]
    titles = ["returns", "returns per share", "returns per invested dollar"]
    for ii in range(3):
        RET[ii].bar(x=consolidated.index[:-1], height=bars[ii][:-1],
                    color = np.where(bars[ii]>0, "xkcd:green", "xkcd:red"))
        RET[ii].set_xticklabels(consolidated.index[:-1], rotation=90)
        RET[ii].set(title = titles[ii],
                    ylabel = "US Dollars")
     
    # figure titles
    CUM_fig.suptitle('Cummulative Returns: 2015 -- Present')
    CUM_zoom_fig.suptitle('Cummulative Returns: Date of Purchase -- Present')
    
    # save files
    RET_fig.savefig('./portfolio/returns_bar.pdf')
    CUM_fig.savefig('./portfolio/performance.pdf')
    CUM_zoom_fig.savefig('./portfolio/performance_purchase.pdf')
    
    #clear all figures
    plt.close('all')