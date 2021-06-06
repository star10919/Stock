#종목 외부에서 주입받기(네이버 증권이용하기-셀레니움사용)
#oop로 짜기(class x, 바로 def)
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

class Stock(object):
    url = 'https://finance.naver.com/sise/lastsearch2.nhn'
    driver_path = 'c:/Program Files/Google/Chrome/chromedriver'
    st_name = []
    st_price = []
    dict = {}
    df = None

    def scrap(self):
        driver = webdriver.Chrome(self.driver_path)
        driver.get(self.url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print('<<<종목명>>>')
        ls = soup.find_all("table", {"class": "type_5"})
        for i in ls:
            print(f'{i.find("a").text}')
            self.st_name.append(i.find("a").text)

        print('<<<현재가>>>')
        ls = soup.find_all("table", {"class": "type_5"})
        ls2 = ls.find('tbody')
        ls3 = ls2.find_all("tr")
        ls4 = ls3.find("td", {"class": "number"})
        for i in ls3[1]:
            print(f'{i.find("td").text}')
            self.st_price.append(i.find("td").text)
        driver.close()

    def insert_dict(self):
        print('=== enter_insert_dict===')
        for i, j in zip(self.st_name, self.st_price):
            self.dict[i] = j
            print(f'{i}:{j}')

    def dict_to_dataframe(self):
        dt = self.dict
        self.df = pd.DataFrame.from_dict(dt, orient='index')
        print(self.df)

    def df_to_csv(self):
        path = './data/stock.csv'
        self.df_to_csv(path, sep=',', na_rep='Nan')

    @staticmethod
    def main():
        s = Stock()
        while 1:
            m = int(input('0-break\n1-get stock\n2-dict\n3-dataframe\n4-csv'))
            if m == 0:
                break
            elif m == 1:
                s.scrap()
            elif m == 2:
                s.insert_dict()
            elif m == 3:
                s.dict_to_dataframe()
            elif m == 4:
                s.df_to_csv()
            else:
                continue

Stock.main()