from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd
from palettable.colorbrewer.qualitative import Set1_7
import numpy as np
import yfinance as yf
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def cum_returns(data):
    # daily close
    daily_close = data.Close
    
    # daily returns
    daily_pct_change = daily_close.pct_change()
    
    # replace NA values with 0
    daily_pct_change.fillna(0, inplace=True)
    
    # calculate cum returns
    cum_daily_return = (1 + daily_pct_change).cumprod()
    
    return cum_daily_return, daily_pct_change
    

def figure_1(stock, save):
    # basic figure settings
    plt.style.use('isaac_style.mplstyle')
    plt.ion()
    plt.clf()
    
    # plot historic daily close (year to date)
    fig, ax = plt.subplots(num=1, nrows=3, ncols=3)
    fig.subplots_adjust(left=0.06, right=0.95, top=0.95, bottom=0.05,
                        hspace=0.35, wspace=0.35)
    fig.set_size_inches(10,7.5)
    
    # initiate tickers
    tickers = yf.Tickers([stock, "VOO"])

    # labels
    labels = [stock, "S&P 500"]    

    for ii in range(2):
        
        # get data for the last 10 years
        data = tickers.tickers[ii].history(period="10y")
        
        # calculate plot cumulative daily returns (10 yrs)
        cum_d_return, d_pct_change = cum_returns(data)
        ax[0,0].plot(cum_d_return,
                      color=Set1_7.hex_colors[ii],
                      lw = 1,
                      label = labels[ii])
        
        # calculate and plot cumulative returns (1 yr)
        cum_d_return_zoom, d_pct_change_zoom = cum_returns(data[-255:])
        ax[0,1].plot(cum_d_return_zoom,
                      color=Set1_7.hex_colors[ii],
                      lw = 1,
                      label = labels[ii])
        
        # calculate and plot volatlity
        min_periods = 100 # define the minumum of periods to consider 
        vol = d_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)
        ax[2,1].plot(vol,
                      color=Set1_7.hex_colors[ii],
                      lw = 1,
                      label = labels[ii])
        
        # metrics that don't need to be compared to market
        if tickers.symbols[ii] != "VOO":
            
            # last month price
            ax[0,2].plot(data.Close[-25:],
                          color=Set1_7.hex_colors[ii],
                          lw = 1, label = stock)
            
           
            # helpful variables
            bar_gap = 0.45
            billion = 1000000000
            
            # get data
            earnings = tickers.tickers[ii].earnings
            earnings = earnings/billion
            
            # earnings
            ax[1,0].bar(x=earnings.index,
                        height=earnings.Earnings,
                        color = np.where(earnings.Earnings>0, 
                                         "green", 
                                         Set1_7.hex_colors[0]),
                        width = bar_gap)
            
            # revenue
            ax[1,1].bar(x=earnings.index,
                        height=earnings.Revenue,
                        color = "black",
                        width = bar_gap)
            
            # earnings-revenue ratio
            ax[1,2].bar(x=earnings.index, 
                        height=earnings.Earnings/earnings.Revenue,
                        color = "black",
                        width = bar_gap)
        
            # quarterly earnings and revenue
            q_earnings = tickers.tickers[ii].quarterly_earnings
            q_earnings = q_earnings/billion
            q_earnings.reset_index(drop=True, inplace = True)
            
            # quarterly earnings
            ax[2,2].bar(x=q_earnings.index,
                        height = np.abs(q_earnings.Earnings),
                        color = np.where(q_earnings.Earnings>0, "green", Set1_7.hex_colors[0]),
                        width = bar_gap/2)
            
            # quarterly revenue
            ax[2,2].bar(x=q_earnings.index+bar_gap/2,
                        height=q_earnings.Revenue,
                        color = "black",
                        width = bar_gap/2)
            
            # dividends
            div_df = data.loc[data.Dividends>0]
            div_per = div_df['Dividends']/div_df['Close']*100
            ax[2,0].plot(div_per,
                         color=Set1_7.hex_colors[ii],
                         lw = 1, 
                         label = stock)
        ii += 1
        
    # subplot labels
    ax[0,0].set(title="Cumulative Returns (10 Years)")
    ax[0,1].set(title="Cumulative Returns (1 Year)")
    ax[0,2].set(title="Closing Price (Last Month)")
    ax[1,0].set(title="Earnings (Billions)")
    ax[1,1].set(title="Revenue (Billions)")
    ax[1,2].set(title="Earnings to Revenue Ratio")
    ax[2,0].set(title="Dividend (Percent)")
    ax[2,1].set(title="Volatility")
    ax[2,2].set(title="Quarterly Earnings/Revenue (past 12 mo.)")
    
    # add legends
    ax[0,0].legend(loc="upper left")
    ax[0,1].legend(loc="upper left")    
    ax[0,2].legend(loc="upper left")  
    ax[2,0].legend(loc="upper left")  
    ax[2,1].legend(loc="upper left")  
    
    # axis labels
    ax[0,0].xaxis.set_major_locator(mdates.YearLocator(2))
    ax[0,0].xaxis.set_major_formatter(DateFormatter("%Y"))
    plt.setp(ax[0,0].get_xticklabels(), rotation=45, ha='right') 

    ax[0,1].xaxis.set_major_formatter(DateFormatter("%m-%d"))
    plt.setp(ax[0,1].get_xticklabels(), rotation=45, ha='right') 
    
    ax[0,2].xaxis.set_major_formatter(DateFormatter("%m-%d"))
    plt.setp(ax[0,2].get_xticklabels(), rotation=45, ha='right')
        
    ax[2,0].xaxis.set_major_locator(mdates.YearLocator(2))
    ax[2,0].xaxis.set_major_formatter(DateFormatter("%Y"))
    plt.setp(ax[2,0].get_xticklabels(), rotation=45, ha='right')

    ax[2,1].xaxis.set_major_locator(mdates.YearLocator(2))
    ax[2,1].xaxis.set_major_formatter(DateFormatter("%Y"))
    plt.setp(ax[2,1].get_xticklabels(), rotation=45, ha='right')
    
    if save == True:
      fig.savefig("./portfolio/analyze_output/figure_1.pdf")

