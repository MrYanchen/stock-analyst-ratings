# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:19:38 2016
Version: python 2.7
@author: MrYanc
"""

from bs4 import BeautifulSoup
import pandas as pd
import os
# self defined function in saveBasics
from saveBasics import getOpener
from saveBasics import dateRange
from saveBasics import getCurrentDate
from saveBasics import getLastDate
from saveBasics import xlsxToCsv

'''
function to save data from website
input: date: date string
output: dataframe
exception: connection abortion
'''
def saveDate(date):
    # read in the parsed data from website
    text = opener.open(url + date).read();
    soup = BeautifulSoup(text, "lxml");

    # extract desired information from the parsed data
    table = soup.find("table");
    table = table.find("tbody");
    rows = table.find_all('tr');
    
    data = [];
    # append columns from the table to data array
    for row in rows:
		columns = row.find_all('td');
		columns = [col.text.strip() for col in columns];
		data.append([col for col in columns if col]);

    # change data array to data frame   
    table = pd.DataFrame(data);
    
    if (not table.empty):
        # modify the data frame to desired format
        table[1] = date;
        table.columns = ['Brokerage', 'Date', 'Action', 'Company', 'Rating', 'Price_Target', 'Impact'];
        
        # get the abbreviation name of the company
        for index, row in table.iterrows():
            string = row['Company'].encode('utf-8');
            if (string.find('(') != -1):
                string = string[string.rfind('(') + 1 : string.rfind(')')];
                row['Company'] = string;

    return table;

def main():
    # get web browser
    opener = getOpener();

    # url of marketbeat website
    url = 'https://www.marketbeat.com/ratings/USA/';

    # get the start date
    start_date = getLastDate('DataMarketBeats');
    # get the current date
    end_date = getCurrentDate();

    for single_date in dateRange(start_date, end_date):
        date = single_date.strftime("%Y-%m-%d");
        table = saveDate(date);

        if (not table.empty):
            # file path
            filename = date + ".xlsx";
            path = os.path.join(os.getcwd(), 'DataMarketBeats');
            filepath = os.path.join(path, filename);
            
            try:
                # save file
                table.to_excel(filepath);
                print('Save file: %s' % filename);
            except Exception as e:
                print('Unable to save file: %s' % filename);

        else:
            print('No data in %s' % single_date);

    #xlsxToCsv('MarketBeatsData');
    pass

if __name__ == "__main__":
    main();