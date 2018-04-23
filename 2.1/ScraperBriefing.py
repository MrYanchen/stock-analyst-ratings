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

class Briefing(Scraper.Ratings):
    """docstring for ClassName"""
    def __init__(self):
        Scraper.Ratings.__init__(self);

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def setup(self):
        # url of briefing website
        self.url = "https://www.briefing.com/Investor/Calendars/Upgrades-Downgrades/";
        self.category = ["Upgrades", 'Downgrades', 'Initiated', 'Resumed', 'Reiterated'];
        pass

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
        pass

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
                table = self.process(item);
                table = self.parse(table, item);
                if (not table.empty):
                    self.save(table, item, filepath, filetype);
                else:
                    print('Unable Save file in: %s' % item);
                queue.task_done();
        pass;

        '''
    function: scrape data from website
    input: 
    output: 
    exception: 
    '''
    def process(self, datetime):
        # url of briefing website
        url = "https://www.briefing.com/Investor/Calendars/Upgrades-Downgrades/";
        category = ["Upgrades", 'Downgrades', 'Initiated', 'Resumed', 'Reiterated'];
        
        # split date to year, month, day
        d = datetime.split('-');

        table = pd.DataFrame();
        # iterate through different urls
        for cat in category:
            u = url + cat + '/' + d[0] + '/' + d[1] + '/' + d[2];

            # read in the parsed data from website
            html = self.browse(u);
            soup = BeautifulSoup(html, "lxml");

            # extract desired information from the parsed data
            table_parse = soup.find('table', attrs={'class':'calendar-table'});
            
            data = [];
            # append columns from the table to data array
            if (table_parse != None):
                rows = table_parse.find_all('tr');
                for row in rows:
                    columns = row.find_all('td');
                    columns = [col.text.strip() for col in columns];
                    data.append([col for col in columns if col]);
                
                if (data != None):
                    del data[0];
                
                t = pd.DataFrame(data);
                t['5'] = cat;
                # change data array to data frame
                table = table.append(t, ignore_index=True);
    
        return table;
        pass;

    '''
    function: parse data from website to get exact info
    input: date: datetime
    output: dataframe
    exception: 
    '''
    def parse(self, table, datetime):       
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

def main(start_date, end_date, filepath, filetype):
    briefing = Briefing();
    briefing.setup();
    briefing.execute(start_date, end_date, filepath, filetype);
    briefing.dispose();
    pass;

if __name__ == "__main__":
    start_date = sys.argv[1];
    end_date = sys.argv[2];
    filepath = sys.argv[3];
    filetype = sys.argv[4];
    main(start_date, end_date, filepath, filetype);
    pass;