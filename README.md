# StockFind

## Overview
StockFind is a comprehensive web application designed to aid investors in identifying financially strong trending stocks and constructing optimal portfolios. The application leverages sentiment analysis and financial metric analysis to provide valuable insights for investment strategy formulation. Built using Python and Flask, StockFind integrates data from Yahoo Finance and Alpha Vantage APIs, and utilizes the nltk library for sentiment analysis.

## Features

### Sentiment Analysis
- **Financial Document Analysis**: Uses the nltk library to perform sentiment analysis on financial documents.
- **Trending Stocks Identification**: Identifies trending stocks based on sentiment scores from news articles and financial reports.

### Financial Metric Analysis
- **Integration with Yahoo Finance and Alpha Vantage APIs**: Retrieves and analyzes financial metrics for various stocks.
- **Comprehensive Financial Metrics**: Analyzes financial documents to assess the financial health of stocks.

### Optimal Portfolio Construction
- **Markowitz Model**: Implements the Markowitz Model to construct optimal investment portfolios.
- **Performance Metrics**: Displays the predicted annual return, volatility, and Sharpe ratio of the optimal portfolio.

### Web Interface
- **Flask Web Application**: Provides a user-friendly interface for investors to interact with the application and access analysis results.
- **Data Storage**: Utilizes MongoDB for efficient data storage and retrieval.

## Technology Stack
- **Backend**: Python, Flask
- **Database**: MongoDB
- **APIs**: Yahoo Finance, Alpha Vantage
- **Libraries**: nltk for sentiment analysis

## Benefits
- **Improved Investment Strategies**: Helps investors make informed decisions by identifying financially strong and trending stocks.
- **Optimal Portfolio Construction**: Assists in constructing portfolios with favorable risk-reward profiles based on the Markowitz Model.
- **Comprehensive Analysis**: Provides detailed insights into stock performance and sentiment, aiding in strategic investment planning.

  

## Once cloned please update:

plt.savefig('C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\static\\stockData.png') in line 32 of OptimalPortfolio.py tp a path on your computer
plt.savefig("C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\static\\optimalPortfolio.png") in line 128 of OptimalPortfolio.py to a path on your computer
set env variables ALPHAKEY and MONGODB_URI
dataFolder = 'C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\Server\\downloadedData' in line 113 in main.py to a path to a downloadedData folder on your computer to store the data
self.processPath = 'C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\Server\\Processed' in line 55 of findStockClasses must also be updated to a processed folder path on your computer


NOTE: If you do not have a premium version of the AlphaVantage API, analyze trending stocks can only be done once per day as there is a limit on the amount of calls to the API
If you would like to continue looking at the same analysis, you must comment out mydownload(stocklist, dataFolder, apikey) in line 120 of main.py
NOTE: Current analysis of trending stocks is not too strict due to current economy, hence once things change, criteria for a good stock may need to be updated
