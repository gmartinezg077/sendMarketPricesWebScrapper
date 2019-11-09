from sendMarketScrapper import StocksValuesScrapper;

stocksScrapper = StocksValuesScrapper("SDC")
stocksScrapper.scrape()
stocksScrapper.export2csv()




