# code from Sahaj Godhani, https://sahajgodhani777.medium.com/analyzing-stock-price-news-sentiment-with-machine-learning-models-in-python-1d94fb680b3d
# Import libraries
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time as tme
import random
from datetime import datetime

def returnSentiment(tickers, n):
    # Get the current date
    current_date = datetime.now()
    # Format the date as 'Dec-19-23'
    formatted_date = current_date.strftime('%b-%d-%y')

    # Parameters
    #n = 10 # number of articles to print
    #tickers = ['AAPL', 'TSLA', 'AMZN']

    # Get Data
    finwiz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    for ticker in tickers:
        url = finwiz_url + ticker
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})

        try:
            resp = urlopen(req)
            html = BeautifulSoup(resp, features="lxml")
            news_table = html.find(id='news-table')
            news_tables[ticker] = news_table
        except Exception as e:
            print(f"Error accessing {ticker}: {e}")

        tme.sleep(random.uniform(1, 3))  # Introduce a delay between requests

    try:
        for ticker in tickers:
            df = news_tables[ticker]
            df_tr = df.findAll('tr')

            #print('\n')
            #print('Recent News Headlines for {}: '.format(ticker))

            for i, table_row in enumerate(df_tr):
                a_text = table_row.a.text
                td_text = table_row.td.text
                td_text = td_text.strip()
                #print(a_text, '(', td_text, ')')
                if i == n - 1:
                    break
    except KeyError:
        pass

    # Iterate through the news
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]

            # API sometimes gives today as date so change formatting
            if date == "Today":
                date = formatted_date

            parsed_news.append([ticker, date, time, text])

    # Sentiment Analysis
    nltk.download('vader_lexicon')
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Date', 'Time', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    # View Data
    news['Date'] = pd.to_datetime(news.Date).dt.date

    unique_ticker = news['Ticker'].unique().tolist()
    news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

    values = []
    for ticker in tickers:
        dataframe = news_dict[ticker]
        dataframe = dataframe.set_index('Ticker')
        dataframe = dataframe.drop(columns=['Headline'])
        #print('\n')
        #print(dataframe.head())

        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)

    df = pd.DataFrame(list(zip(tickers, values)), columns=['Ticker', 'Mean Sentiment'])
    df = df.set_index('Ticker')
    df = df.sort_values('Mean Sentiment', ascending=False)
    #print('\n')
    #print(df)
    return df['Mean Sentiment'].tolist()