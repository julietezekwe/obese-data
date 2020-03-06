import requests
import datetime
import os
from bs4 import BeautifulSoup

class ObeseData:
    ENDPOINT = 'https://en.wikipedia.org/wiki/List_of_countries_by_body_mass_index'
    OUTPUT_DIR = 'data/'
    OBESE_DATA = OUTPUT_DIR + 'data.csv'

    def __init__(self):
        self.html_doc = None
        self.data_node = None
        self.dataset = []

    def country_by_bmi_count(self):
        self.__run()

        if self.__file_already_exit(self.OBESE_DATA):
            print(self.OBESE_DATA, 'already exit and will be overwritten! \n')

        with open(self.OBESE_DATA, 'w') as csv_handle:
            csv_handle.write('Country,Overall rank,Overall mean BMI (kg/m2),Female rank,Male rank,Female mean BMI (kg/m2),Male mean BMI (kg/m2)')
            for datapoint in self.dataset:
                csv_handle.write(','.join(datapoint))
                csv_handle.write('\n')
    
        print('Completed! ')
        print('Open', os.path.join(os.getcwd(), self.OBESE_DATA))
    
    def __run(self):
        if len(self.dataset) == 0:
            self.__load_page()
            self.__extract_data_node()
            self.__extract_data()

    def __load_page(self):
        try:
            req = requests.get(self.ENDPOINT)
            if req.status_code == 200:
                self.html_doc = req.content
                print('HTML fetched...')
            else:
                print('Server error...')
        except Error as e:
            print('Unknown network error...')
    
    def __extract_data_node(self):
        html_node = BeautifulSoup(self.html_doc, 'html5lib')
        self.data_node = html_node.find("table", {"class": "wikitable"})
    
    def __extract_data(self):
        for node in self.data_node.find_all('tr'):
            self.dataset.append([val.text.replace("\n", "").replace("\xa0", "").replace("-", '') for val in node.find_all('td')])
    
    def __file_already_exit(self, filename):
        return os.path.exists(filename)

def main():
  obeseData = ObeseData()
  obeseData.country_by_bmi_count()

if __name__ ==  '__main__':
  main()