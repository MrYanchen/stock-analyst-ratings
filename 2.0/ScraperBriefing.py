# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
from bs4 import BeautifulSoup
import pandas as pd
import Ratings

class MarketBeats(Ratings.Ratings):
    """docstring for ClassName"""
    def __init__(self, url):
        Ratings.Ratings.__init__(self, url);

    '''
    function: parse data from website to get exact info
    input: date: date string
    output: dataframe
    exception: 
    '''
    def parse(self, category):
        html = self.browse();
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
            table = table.append(t, ignore_index=True);
        return table;
        pass;

    def category(self, datetime):
        # split date to year, month, day
        d = date_time.split('-');

        table = pd.DataFrame();

        category = ["Upgrades", 'Downgrades', 'Initiated', 'Resumed', 'Reiterated'];
        # iterate through different urls
        for cat in category:
            u = url + cat + '/' + d[0] + '/' + d[1] + '/' + d[2];
            
        pass;

    def save(self, start_date, end_date):
        for single_date in dateRange(start_date, end_date):
            date_time = single_date.strftime("%Y-%m-%d");
            table = save_date(date_time);
        pass;