StockFind is a web application that can be used to watch your current stocks price history and current sentiment using machine learning as well as find new trending stocks that pass a certain criteria.

Once cloned please update:

plt.savefig('C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\static\\stockData.png') in line 32 of OptimalPortfolio.py tp a path on your computer
plt.savefig("C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\static\\optimalPortfolio.png") in line 128 of OptimalPortfolio.py to a path on your computer
set env variables ALPHAKEY and MONGODB_URI
dataFolder = 'C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\Server\\downloadedData' in line 113 in main.py to a path to a downloadedData folder on your computer to store the data
self.processPath = 'C:\\Users\\ljlco\\PycharmProjects\\end\\stockFind\\Server\\Processed' in line 55 of findStockClasses must also be updated to a processed folder path on your computer


NOTE: If you do not have a premium version of the AlphaVantage API, analyze trending stocks can only be done once per day as there is a limit on the amount of calls to the API
If you would like to continue looking at the same analysis, you must comment out mydownload(stocklist, dataFolder, apikey) in line 120 of main.py
NOTE: Current analysis of trending stocks is not too strict due to current economy, hence once things change, criteria for a good stock may need to be updated
