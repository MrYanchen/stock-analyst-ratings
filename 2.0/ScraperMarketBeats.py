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
    input: url: string
    output: dataframe
    exception: 
    '''
    def parse(self, date):
        url = "https://www.marketbeat.com/ratings/USA/";
        html = self.browse(url+date);
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

    '''
    function: process scraper from website
    input: start_date: date string, end_date: date string, filepath: string, filetype: string
    output: 
    exception: 
    '''
    def process(self, start_date, end_date, filepath, filetype):
        for date in date_range(start_date, end_date):
            table = self.parse(date);
            self.save(table, date, filepath, filetype);
    	pass;

def main(start_date, end_date, filepath, filetype):
    markbeats = MarketBeats();
    markbeats.process(start_date, end_date, filepath, filetype)
    pass;

if __name__ == "__main__":
    # date = "2017-10-27";
    # markbeats = MarketBeats();
    # table = markbeats.parse(date);
    # markbeats.save(table, '11', 'D:\\', 'xlsx');
    # markbeats.save(table, '11', 'D:\\', 'csv');
    start_date = sys.argv[1];
    end_date = sys.argv[2];
    filepath = sys.argv[3];
    filetype = sys.argv[4];
    main(start_date, end_date, filepath, filetype);
    pass;
