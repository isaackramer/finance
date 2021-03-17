# Finance with Python

This repository is designed to analyze stocks. The functions can be used to help evaluate stocks before purchase. Functions to evaluate portfolio performance are also included.

## Evaluating a stock before purchase 

These functions be used to help evaluate whether to purchase a company's stock. Main functions are in `analyze_stock.py`

`analyze_figure_1.py` This function provides basic information about a company's historical performance, recent price trends, recent earnings and revenue history, volatility, and dividends.

`analyze_figure_2.py` This function takes a closer look at a company's earning's history, since 2005. Data is scrapped from macrotrends.net. Our goal is to find company's with rising revenue and rising income. In addition to revenue and net income, we plot operating and pre-tax income. Operating income does not include interest expense, taxes, and special items, and can therefore be a better indicator of a company's current business performance. Elimanting taxes can help account for the effect of different state tax policies.

`analyze_figure_3.py` This function takes a closer look at a company's cash flow history, since 2005. Data is scrapped from macrotrends.net. Our goal is to find company's with rising incomes, and cash flow information can supplement what we learn from the income statement. 

* Cash flows from operating activities: Cash from day-to-day operations. Want to see this growing.
* Cash flow from business activities: Investments back into business are negative, while income from investments the business has. Negative numbers indicate that the business is growing. Positive numbers can indicate that the business is failing, as they are selling assets in order to sustain cash flow.
* Cash from financing activities: This primarily refers to cash associated with new debts and dividends payments. It can also refer to common stock repurchasing – buying back its own shares. Whether this is a good thing depends on stock price and company’s position. 
* Net cash flow: Want to see growing positive numbers

`analyze_metrics.py` This function relies on the finvizfinance package to gather important metrics such as the price-earnings ratio, price-sales ratio, debt-equity ratio, and price-book ratio. These ratios can be used to evaluate whether a paticular company's stock is overvalued or fairly priced.

## Earnings Calendar

`earnings_calendar.py` This function checks when the next earning announcment is scheduled for stocks in `my_portfolio_public.csv`.

## Portfolio Performance 

`analyze_portfolio.py` This function can be used to analyze the performance of your portfolio. To use, update the `my_portfolio_public.csv` file in the `portfolio` directory. Output includes three PDFs. (1) the cummulative returns of each stock in your portfolio from 2015 -- Present, as compared to the S&P 500, (2) (1) the cummulative returns of each stock in your portfolio from your intital date of purchase -- Present, as compared to the S&P 500, (3) total returns for each stock in your portfolio, returns per share, and returns per dollar invested

## ETF Filter -- Find Value Stocks

`ETF_filter.py` This function can be used to filter a given ETF to find value stocks. This function relies on the finvizfinance package to gather important metrics such as the price-earnings ratio, price-sales ratio, debt-equity ratio, and price-book ratio. 