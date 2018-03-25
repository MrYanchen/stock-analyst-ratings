# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
from bs4 import BeautifulSoup
import pandas as pd
import Scraper

class Briefing(Scraper.Ratings):
    """docstring for ClassName"""
    def __init__(self):
        Scraper.Ratings.__init__(self);

    '''
    function: parse data from website to get exact info
    input: url: string
    output: dataframe
    exception: 
    '''
    def parse(self, url, category):
        html = self.browse(url);
        soup = BeautifulSoup(html, "lxml");

        table = pd.DataFrame();
        # extract desired information from the parsed data
        t = soup.find('table', attrs={'class':'calendar-table'});

        data = [];
        # append columns from the table to data array
        if (t != None):
            rows = t.find_all('tr');
            for row in rows:
                columns = row.find_all('td');
                columns = [col.text.strip() for col in columns];
                data.append([col for col in columns if col]);

            if (data != None):
                del data[0];

            r = pd.DataFrame(data);
            r['5'] = category;
            # change data array to data frame
            table = table.append(r, ignore_index=True);
        return table;
        pass;

    '''
    function: parse data from website to get exact info
    input: date: date string
    output: dataframe
    exception: 
    '''
    def category(self, datetime):
        # url of briefing website
        url = "https://www.briefing.com/Investor/Calendars/Upgrades-Downgrades/";
        category = ["Upgrades", 'Downgrades', 'Initiated', 'Resumed', 'Reiterated'];
        
        # split date to year, month, day
        d = datetime.split('-');

        table = pd.DataFrame();

        # iterate through different urls
        for cat in category:
            u = url + cat + '/' + d[0] + '/' + d[1] + '/' + d[2];
            t = self.parse(u, cat)
            table = table.append(t);

        # modify the data frame to desired format
        if (not table.empty):
            table.columns = ['Brokerage', 'Date', 'Action', 'Company', 'Rating', 'Price_Target'];
            table['Brokerage'] = None;
            table['Brokerage'] = table['Action'];
            table['Action'] = table['Price_Target'];
            table['Price_Target'] = table['Rating'];
            table['Rating'] = table['Company'];
            table['Company'] = table['Date'];
            table['Date'] = datetime;

        return table;
        pass;

    '''
    function: process scraper from website
    input: start_date: date string, end_date: date string
    output: 
    exception: 
    '''
    def process(self, start_date, end_date, filepath, filetype):
        for date in date_range(start_date, end_date):
            datetime = date.strftime("%Y-%m-%d");
            table = self.category(datetime);
            self.save(table, date, filepath, filetype);
        pass;

def main(start_date, end_date, filepath, filetype):
    briefing = Briefing();
    # table = briefing.category("2017-12-11");
    briefing.process(start_date, end_date, filepath, filetype);
    
    pass

if __name__ == "__main__":
    start_date = sys.argv[1];
    end_date = sys.argv[2];
    filepath = sys.argv[3];
    filetype = sys.argv[4];
    main(start_date, end_date, filepath, filetype);
    pass;