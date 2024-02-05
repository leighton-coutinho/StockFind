import yahoo_fin.stock_info as yf
import csv
import os
import numpy as np

from stockFind.Server.downloadData import mydownload
from stockFind.Server.findStocksClasses import Stock
from stockFind.Server.findStocksUtils import saveAll, updateProcessed
from stockFind.Server.OptimalPortfolio import download_data, show_data, calculate_return, generate_portfolios, show_portfolios, optimize_portfolio, print_optimal_portfolio, show_optimal_portfolio


def get_most_active_stocklist():
    most_active = yf.get_day_most_active()

    return most_active['Symbol'].tolist()

def preliminaryTests(stock):
    """Run preliminary tests to see if stock failed and can be skipped."""
    # Preliminary tests to disqualify a stock
    stock.prelimTests()
    # Skip stock if it failed any of the preliminary tests
    if stock.errorMessage != 'processed':
        return

    # Check for negative income
    stock.checkNegativeIncome()

    # Skip stock if it has negative net income
    if stock.errorMessage != 'processed':
        return

    # Check if stock price has been decreasing recently, for NOW IGNORE AS MOST STOCK PRICES HAVE RECENTLY GONE DOWN DUE TO CURRENT CIRCUMSTANCES
    #stock.checkSlope()

    # Skip stock if it does not have increasing price change
    if stock.errorMessage != 'processed':
        return

    # Reduce income statement and balance sheet into one DF
    stock.reduceDF()


def manageBadData(stock, r):
    """Manage missing data."""
    # Identify missing data
    stock.miss[r] = stock.identifyMissing(stock.reports[r])

    # If user is not flexible, get user input when missing data is encountered
    if not stock.flex:
        stock.reports[r] = stock.getData(stock.reports[r],
                                         stock.miss[r])
    # Otherwise if user is flexible, copy recent data over to missing data
    else:
        stock.reports[r], stock.miss[r] = stock.copy(stock.reports[r],
                                                     stock.miss[r])

    # Change column type to numeric if is object
    stock.reports[r] = stock.checkType(stock.reports[r])

    # Check if shares are missing trailing zeros
    shares = 'commonStockSharesOutstanding'
    stock.reports[r][shares] = stock.checkSmallShares(stock.reports[r][shares])


def analyzeStock(stock, r):
    """Run important tests to determine if quality stock."""
    # Calculate ROE and EPS
    stock.reports[r] = stock.calculate(stock.reports[r])

    # Calculate the percentage change year over year
    stock.reports[r] = stock.percentChange(stock.reports[r], r)

    # Round DF for pretty saving
    stock.reports[r] = stock.roundReports(stock.reports[r])

    # Check the percentage change year over year
    stock.test(stock.reports[r], r)

    if r == 'q':
        # Calculate the average of the percent changes
        stock.averagePercentChange(stock.reports[r])


def saveResults(stock, s, stockFile, record):
    """Save results after processing stock."""
    # Save stock information
    stock.save()

    # Update the processed file
  #  updateProcessed(stockFile, s, stock.errorMessage)

    # Append record to later save
    record.append([x for x in stock.record.values()])

    return record


def getStocks():
    # Only test top 10 stocks everyday due to limits on API calls (25 request limit per day)
    stocklist = get_most_active_stocklist()[:10]
    stockFile = "mystocks.txt"
    file_exists = os.path.isfile(stockFile)

    with open(stockFile, 'a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Symbols'])

        for symbol in stocklist:
            writer.writerow([symbol])


    dataFolder = 'C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\Server\\downloadedData'
    apikey = os.environ.get("ALPHAKEY")
    record = []
    print(stocklist)

    # download data regarding the stocklist
    mydownload(stocklist, dataFolder, apikey)

    goodStocks = []
    for s in stocklist:
            print('>>>', s)

            # Initialize Stock object
            stock = Stock(s, dataFolder, False)

            # Run preliminary tests to check if stock is disqualified
            preliminaryTests(stock)

            # Skip stock if it failed preliminary tests (Might be because all companies have recently performed worse). Update the *Processed.csv
            if stock.errorMessage != 'processed':
                #updateProcessed(stockFile, s, stock.errorMessage)
                continue

            # only do anually
            #for r in stock.reports:
                # Manage missing data and other inconsistencies in data
            manageBadData(stock, 'a')

                # Calculate new metrics and run stock tests
            analyzeStock(stock, 'a')

            # if the stock fails less than 2 tests it is a good enough stock
            if stock.record['numfailed'] < 2:
             #   stock.s is stock name
                goodStocks.append(stock.s)

            # Save data and update files
            record = saveResults(stock, s, stockFile, record)

    # Assert can occur when all stocks fail preliminary tests
    assert record != [], 'No procssed stocks to save to *Results.csv'

    # Save the test results for all stocks
    columns = [x for x in stock.record.keys()]
    saveAll(record, columns)
    return goodStocks

def statistics(weights, returns):
        # on average there are 252 trading days in a year
    NUM_TRADING_DAYS = 252
    # we will generate random w (different portfolios)
    NUM_PORTFOLIOS = 10000
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()
                                                            * NUM_TRADING_DAYS, weights)))
    return np.array([portfolio_return, portfolio_volatility,
                     portfolio_return / portfolio_volatility])


def mainfunc():
    # on average there are 252 trading days in a year
    NUM_TRADING_DAYS = 252
    # we will generate random w (different portfolios)
    NUM_PORTFOLIOS = 10000

    # stocks we are going to handle
    stocks = getStocks()
    print("Good Stocks: " + str(stocks))

    # historical data - define START and END dates
    start_date = '2016-01-01'
    end_date = '2023-12-01'

    dataset = download_data(stocks)
    show_data(dataset)
    log_daily_returns = calculate_return(dataset)
    # show_statistics(log_daily_returns)

    pweights, means, risks = generate_portfolios(log_daily_returns, stocks)
    #show_portfolios(means, risks)
    optimum = optimize_portfolio(pweights, log_daily_returns, stocks)
    show_optimal_portfolio(optimum, log_daily_returns, means, risks)
    optPort =  optimum['x'].round(3)
    stats = statistics(optimum['x'].round(3), log_daily_returns)

    show_optimal_portfolio(optimum, log_daily_returns, means, risks)
    return (optPort, stats, stocks)
