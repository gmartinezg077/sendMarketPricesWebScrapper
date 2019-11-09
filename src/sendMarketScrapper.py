import csv
import requests
import time
from bs4 import BeautifulSoup


class StocksValuesScrapper:

    def __init__(self):
        self.markets = ['SDP', 'SDC', 'SDE']
        self.scrapper_date = ""
        self.url = "http://www.bmerf.es"
        self.html_stock_summary = "/esp/aspx/comun/posiciones.aspx?Mercado="
        self.html_stock_detail = "/esp/aspx/Comun/FichaEmision.aspx?r=SEND&t="
        self.isin_ids = []
        self.data = []

    @staticmethod
    def __get_html_page(url):
        html_page = requests.get(url)
        return html_page

    def scrape(self):
        # Start timer
        start_time = time.time()
        for market in self.markets:
            self.__scrape_market(market)
        # Show elapsed time
        end_time = time.time()
        print("Total time for scrapping data: " + str(round(((end_time - start_time) / 60), 2)) + " minutes")

    def __scrape_market(self, market):
        print("Starting Web Scraping of BME Stocks of "
              + market + " market from " + "'" + self.url + "' source...")
        html_page = self.__get_html_page(self.url + self.html_stock_summary + market)
        html_page_soup = BeautifulSoup(html_page.content, features="html.parser")
        #Getting date info
        market_date = html_page_soup.findAll('th', {"class": "sh_titulo"})[0].text
        trs = html_page_soup.findAll('tr')
        for i in range(len(trs)):
            tr_tag = trs[i]
            if 'data-isin' in tr_tag.attrs:
                isin = self.__extract_isin_info(tr_tag)
                description = tr_tag.findChildren("td", recursive=False)[0].text
                stock_data = self.__scrape_stock_detail(market_date,market, isin, description)
                self.data.append(stock_data)
        print("Processed " + str(len(self.isin_ids)) + " stocks from " + market)

    def __extract_isin_info(self, tr_tag):
        isin_attr = tr_tag['data-isin']
        self.isin_ids.append(isin_attr)
        return isin_attr

    def __scrape_stock_detail(self, date, market, isin, description):
        print("Starting Web Scraping of [" + isin + "] " + description + "...")
        stock_type = self.__get_stock_type(market)
        html_page = self.__get_html_page(self.url + self.html_stock_detail + stock_type + "&i=" + isin)
        html_page_soup = BeautifulSoup(html_page.content, features="html.parser")
        div_main_data = html_page_soup.find("div", {"id": "datosPrincipales"})
        div_main_data_cells = div_main_data.findChildren("td", {"class": "celda"}, recursive=True)
        stock_type_desc = div_main_data_cells[1].text.strip()
        stock_issuer = div_main_data_cells[2].text.strip()
        stock_issue_date = div_main_data_cells[3].text.strip()
        stock_expiration_date = div_main_data_cells[4].text.strip()
        stock_nominal_price = div_main_data_cells[5].text.strip()
        stock_currency = div_main_data_cells[6].text.strip()
        div_stock_detail_view = html_page_soup.find("div", {"id": "vistaFICHA"})
        stock_detail_view_rows = div_stock_detail_view.findChildren("tr", recursive=True)
        stock_price_detail_row = stock_detail_view_rows[5]
        stock_detail_view_cells = stock_price_detail_row.findChildren("td", {"class": "celda"}, recursive=True)
        stock_last_price = stock_detail_view_cells[0].text.strip()
        stock_last_price_date = stock_detail_view_cells[1].text.strip()
        # Append stock data
        stock_data = [market, date, stock_type_desc, isin, description, stock_issuer, stock_issue_date,
                      stock_expiration_date, stock_currency, stock_last_price, stock_last_price_date,
                      stock_nominal_price]
        return stock_data

    @staticmethod
    def __get_stock_type(market):
        stock_type = ""
        if market == "SDP":
            stock_type = "PUB"
        elif market == "SDC":
            stock_type = "PRV"
        else:
            stock_type = "EXT"
        return stock_type

    def export2csv(self):
        # Generating csv file path
        csv_path = "../csv/send_stock_prices.csv"
        # Creating file
        file = open(csv_path, "w+")
        file_writer = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['market', 'date', 'type', 'isin', 'description', 'issuer', 'issue_date',
                              'expiration_date', 'currency', 'last_price', 'last_price_date', 'nominal_price'])
        # Write down all data content
        for i in range(len(self.data)):
            file_writer.writerow(self.data[i])
