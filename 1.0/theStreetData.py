# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 15:36:18 2016
Version: python 2.7
@author: MrYanc
"""

from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
from saveBasics import getOpener

opener = getOpener();

'''
input: n1: string, n2: string, n3: string
output: url list
exception: none
'''
def save_range(n1, n2, n3):
    urls = [];
    
    for i in range(n1, n2 + 1, n3):
        temp_urls = save_url(str(i));
        for t in temp_urls:
            urls.append(t);
    
    return urls;

'''
input: number: int
output: url list
exception: connection abortion
'''
def save_url(number):
    
    text = opener.open('https://www.thestreet.com/analyst-upgrades-downgrades?start=' + number).read()
    soup = BeautifulSoup(text, "lxml");
    
    urls = [];

    for div in soup.findAll("div", { "class" : "news-list__item" }):
        d = div.find('div', attrs={'class': 'news-list__body'})
        div_url = d.find('a')['href'];
        urls.append(div_url);
        
    return urls;

'''
input: url: string
output: string list
exception: connection abortion
'''    
def save_content(url):
    thestreet = "https://www.thestreet.com";

    text = opener.open(thestreet + url);
    soup = BeautifulSoup(text, "lxml");
    
    url_time = soup.find("time");
    url_date = url_time['datetime'];
    url_date = url_date.split("T");
    date = url_date[0]
    
    body = soup.find('div', {'class' : "article-standard__body article__body"});
    
    content = [];

    for p in body.findAll("p"):
        print p
        content.append(p.text);   
    
    next = soup.find("div", {"class" : "article__pagination-item"});
    if (next != None):
        next_url = next.find('a', {'class' : 'nav-link article__pagination-link article__pagination-link--next '});
        if (next_url != None):
            temp = save_content(next_url['href']);
            if (temp != None):
                for t in temp:
                    content.append(t);
    
    content = [date] + content;
       
    return content;    

'''
input: content: string list
output: excel file
exception: path not exist exception
'''     
def save_data(content):
    
    date = content[0];
    
    content.remove(content[0]);
    
#    for item in content:
#        if ('.' not in item or '(' not in item):
#            content.remove(item);
    
    frame = pd.DataFrame(content);
    frame[1] = frame[0];
    frame[0] = date;
    frame.columns = ['date', 'content'];
    for index, row in frame.iterrows():
        row['content'] = row['content'].decode('utf-8');
    
    filepath = date + ".xlsx";
    workbook = xlsxwriter.Workbook(filepath);
    worksheet = workbook.add_worksheet();
    workbook.close();
    
    writer = pd.ExcelWriter(filepath);
    frame.to_excel(writer, 'Sheet1');
    writer.save();
    print date + ' success'
