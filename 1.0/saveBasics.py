# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:39:13 2016
Version: python 2.7
@author: MrYanc
"""

import urllib2
import datetime
import os
import pandas as pd

'''
function return web browser
input: none
output: browser
exception: none
'''
def getOpener():
    opener = urllib2.build_opener();
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')];
    return opener;

'''
function return single date between start date and end date
input: start date: date string, end date: date string, start date < end date
output: date list
exception: start date > end date
'''
def dateRange(start_date, end_date):
    # start date should prior to end date
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n);

'''
function return current date
input: none
output: current date string
exception:
'''
def getCurrentDate():
    now = datetime.datetime.now();
    return now.date();

'''
function return last date in the specified file
input: file name
output: last date in the file folder
exception: file not found exception
'''
def getLastDate(filename):
    path = os.path.join(os.getcwd(), filename + '\\xlsx');
    list = os.listdir(path);
    lastFile = list[list.__len__() - 1];
    del list;
    lastDate = lastFile.split('.')[0];
    lastDate = datetime.datetime.strptime(lastDate, "%Y-%m-%d");
    lastDate = lastDate.date() + datetime.timedelta(1);
    return lastDate;

'''
function change xlsx file to csv file
input: xlsxFile: string, source: string
output: csv file list
exception: path not exist exception
'''
def xlsxToCsv(xlsxFile, source):
    filepath = os.path.join(os.getcwd(), xlsxFile + '\\csv');
    complist = os.listdir(filepath);
    filepath = os.path.join(os.getcwd(), xlsxFile + '\\xlsx');
    filelist = os.listdir(filepath);

    for filename in filelist[:]:
        name = filename.split('.')[0] + '.csv';
        if (name in complist):
            filelist.remove(filename);

    for filename in filelist:
        change_file(filepath, filename, source);
        print("Change file %s to csv" % filename);

'''
function change xlsx file to csv file
input: filepath: string, filename: string, source: string
output: csv file list
exception: path not exist exception
'''
def change_file(filepath, filename, source):
    table = pd.read_excel(os.path.join(filepath, filename));
    
    for index, row in table.iterrows():
        for i in range(0, 6):
            if (type(row[i]) == float):
                row[i] = str(row[i]);
            else:
                row[i] = row[i].encode('utf-8'); 
                if ('\xc2\xbb' in row[i]):
                    row[i] = row[i].replace('\xc2\xbb', '->');

    filename = filename.split('.')[0];
    table.to_csv(os.path.join(os.getcwd(), source + '\\csv') + '\\' + filename + '.csv');

'''
function return the summary of frequency of given source
input: filepath: string, filelist: string, column: string
output: summary file
exception: path not exist exception
'''
def getSummary(filepath, filelist, column):
    dictionary = {};

    for filename in filelist:
        table = pd.read_excel(os.path.join(filepath, filename));

        for index, row in table.iterrows():
            temp = row[column];
            if (temp in dictionary):
                dictionary[temp] = dictionary[temp] + 1;
            else:
                dictionary[temp] = 1;

    return dictionary;

'''
function save summary to file
input: source: string, column: string
output: summary excel file
exception: path not exist exception
'''
def Summary(source, column):
    filepath = os.path.join(os.getcwd(), source + '\\xlsx');
    filelist = os.listdir(filepath);

    dictionary = getSummary(filepath, filelist, column);

    summary = pd.DataFrame(dictionary.items(), columns = [column, 'Number']);
    summary = summary.sort_values(by = ['Number'], ascending = False);
    summary.index = range(0, summary.shape[0]);

    print(summary.head(20));

    filepath = os.path.join(os.getcwd(), 'sum_' + source + '_' + column + '.xlsx');
    summary.to_excel(filepath);

'''
function combine multiple files to single file
input: source: string, folder: string
output: excel file
exception: path not exist exception
'''
def Summarize(source, folder):
    filepath = os.path.join(os.getcwd(), source + '\\' + folder);
    filelist = os.listdir(filepath);
    
    table = pd.DataFrame();

    for f in filelist:
        t = pd.read_excel(os.path.join(filepath, f));
        table = pd.concat([table, t]);

    table.index = range(0, table.shape[0]);
    table.to_excel(os.path.join(os.getcwd(), source + '_' + folder + '.xlsx'));
    print('Saving file: %s'% (source + '_' + folder + '.xlsx'));

'''
split '->' in specific column
input: table: dataframe, column: string
output: dataframe
exception:
'''
def processTable(table, column):
    for i in range(len(table)):
        row = table.loc[i];
        rating = row[column];
        try:
            if ("->" in rating):
                rating = rating.split("->")[1].strip();
                row[column] = rating;
                table.loc[i] = row;
        except Exception as e:
            print("%d has problem in % s:" % (i, column));
            print(e);
            continue;
    return table;