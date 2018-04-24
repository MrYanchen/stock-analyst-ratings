# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
from bs4 import BeautifulSoup
import pandas as pd
import Scraper
from queue import Queue, Empty
from threading import Thread

THREAD_POOL_SIZE = 5;

class MarketBeats(Scraper.Ratings):
    """docstring for ClassName"""
    def __init__(self):
        Scraper.Ratings.__init__(self);

    '''
    function: set up website scraper
    input: 
    output: 
    exception: 
    '''
    def setup(self):
        self.url = "https://www.marketbeat.com/ratings/USA/";
        pass;

    '''
    function: execute website scraper
    input: start_date: date string, end_date: date string, filepath: string, filetype: string
    output: boolean
    exception: 
    '''
    def execute(self, start_date, end_date, filepath, filetype):
        queue = Queue();

        for date in self.date_range(start_date, end_date):
            datetime = ("{:%Y-%m-%d}").format(date);
            queue.put(datetime);

        threads = [
            Thread(target=self.worker, args=(queue, filepath, filetype,))
            for _ in range(THREAD_POOL_SIZE)
        ];

        for thread in threads:
            thread.start();

        queue.join();
        while threads:
            threads.pop().join();
        
        return True;
        pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def dispose(self):
        pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def worker(self, queue, filepath, filetype):
        while not queue.empty():
            try:
                item = queue.get(block=False);
            except Empty:
                break;
            else:
                table = self.parse(item);
                if (not table.empty):
                    self.save(table, item, filepath, filetype);
                else:
                    print('Unable Save file in: %s' % item);
                queue.task_done();
        pass;

    '''
    function: parse data from website to get exact info
    input: url: string
    output: dataframe
    exception: 
    '''
    def parse(self, date):
        html = self.browse(self.url+date);
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
function: 
input: 
output: 
exception: 
'''
def main(start_date, end_date, filepath, filetype):
    markbeats = MarketBeats();
    markbeats.setup();
    markbeats.execute(start_date, end_date, filepath, filetype);
    markbeats.dispose();
    pass;

if __name__ == "__main__":
    start_date = sys.argv[1];
    end_date = sys.argv[2];
    filepath = sys.argv[3];
    filetype = sys.argv[4];
    main(start_date, end_date, filepath, filetype);
    pass;
