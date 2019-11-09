import csv
from bs4 import BeautifulSoup


class StocksValuesScrapper:

    def __init__(self, market):
        self.market = market
        self.scrapper_date = ""
        self.url = "http://www.bmerf.es"
        self.html_path = "/esp/aspx/comun/posiciones.aspx?Mercado=" + market
        self.data = [
            [self.market, '01/11/19', 'BONOS', 'ES0311843017',
                'BS AUCALSA- 2,900 05/2021', '17/05/2016', '17/05/2021',
                'EUR', 103.00, 0.8902, 31000.00],
            [self.market, '01/11/19', 'BONOS', 'ES03138603C7',
                'BS B. SABADELL-I 0,700 03/2022',  '28/03/2019', '28/03/2022',
                'EUR', 100.15, 0.1694, 150000.00],
        ]

    def __generate_csv_filepath(self):
        filepath = "../csv/" + self.market + "_stock_prices.csv"
        return filepath

    def scrape(self):
        print("Starting Web Scraping of BME Stocks of "
              + self.market + " market from " + "'" + self.url + "' source...")

    def export2csv(self):
        # Generating csv file path
        csv_path = self.__generate_csv_filepath()
        # Creating file
        file = open(csv_path, "w+")

        file_writer = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['market', 'date', 'type', 'isin', 'description', 'issue_date', 'expiration_date',
                              'currency', 'last_negociated_price', 'last_negociated_tir', 'nominal_price'])

        # Write down all data content
        for i in range(len(self.data)):
            file_writer.writerow(self.data[i])
