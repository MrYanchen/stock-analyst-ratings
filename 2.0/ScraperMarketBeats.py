# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
from bs4 import BeautifulSoup
import pandas as pd
import Scraper

class MarketBeats(Scraper.Ratings):
    """docstring for ClassName"""
    def __init__(self):
        Scraper.Ratings.__init__(self);

    '''
    function: parse data from website to get exact info
    input: date: date string
    output: dataframe
    exception: 
    '''
    def parse(self, url):
        html = self.browse(url);
        soup = BeautifulSoup(html, "lxml");

        # extract desired information from the parsed data
        table = soup.find("table");
        table = table.find("tbody");
        rows = table.find_all('tr');

        # append columns from the table to data array
        data = [];
        for row in rows:
            columns = row.find_all('td');
            columns = [col.text.strip() for col in columns];
            data.append([col for col in columns if col]);

        # change data array to data frame
        # modify the data frame to desired format
        table = pd.DataFrame(data);
        if (not table.empty):
            rows_len, columns_len = table.shape;
            if (columns_len == 6):
                table.columns = ['Brokerage', 'Action', 'Company', 'Rating', 'Price_Target', 'Impact'];
        
        # get the abbreviation name of the company
        for index, row in table.iterrows():
            string = row['Company'];
            if (string != None):
                row['Company'] = self.simplify(string);

        return table;
        pass;

    # def save(self, start_date, end_date):
    # 	pass

if __name__ == "__main__":
    url = "https://www.marketbeat.com/ratings/USA/2017-10-27/";
    markbeats = MarketBeats();
    table = markbeats.parse(url);
    markbeats.save(table, '11', 'D:\\', 'xlsx');
    markbeats.save(table, '11', 'D:\\', 'csv');
    pass;
