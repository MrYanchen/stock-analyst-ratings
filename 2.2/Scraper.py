# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""

import requests
import os
import pandas as pd
import datetime

class Ratings(object):
    """docstring for ClassName"""
    def __init__(self):
        pass;

    '''
    function: get the data from website
    input: website url
    output: scrapy data
    exception: url not found exception; connection lost exception
    '''
    def browse(self, url):
        # custom header
        headers = {'User-agent': 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'};

        try:
            r = requests.get(url, headers=headers);
            return r.text;
        except Exception as e:
            raise e;
        pass;

    '''
    function: save dataframe to file
    input: dataframe, filename: string, filepath: string, filetype: string
    output: file
    exception: filepath not exist
    '''
    def save(self, table, filename, filepath, filetype):
        name = filename+"."+filetype;
        path = os.path.join(filepath, name);
        try:
            if filetype == "csv":
                table.to_csv(path);
                print('Save file: %s' % name);
                pass;
            elif filetype == "xlsx":
                table.to_excel(path);
                print('Save file: %s' % name);
                pass;
            else:
                print('Unable to save file: %s' % name);
        except Exception as e:
            raise e
        pass;

    '''
    function: change company name to abbreviation
    input: stringg: company name
    output: string: abbreviation
    exception:
    '''
    def simplify(self, name):
        if (name.find("(") != -1):
            name = name.split("(")[1];
        if (name.find(")") != -1):
            name = name.split(")")[0];
        return name;
        pass;

    '''
    function return single date between start date and end date
    input: start date: date string, end date: date string, start date < end date
    output: date list
    exception: start date > end date
    '''
    def date_range(self, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date();
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date();
        # start date should prior to end date
        for n in range(int ((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n);

if __name__ == "__main__":
    pass;