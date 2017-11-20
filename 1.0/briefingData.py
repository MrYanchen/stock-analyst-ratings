# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 15:01:50 2016
Version: python 2.7
@author: MrYanc
"""
import pandas as pd
import os
from bs4 import BeautifulSoup
# self defined function in saveBasics
from saveBasics import getOpener
from saveBasics import dateRange
from saveBasics import getCurrentDate
from saveBasics import getLastDate
from saveBasics import xlsxToCsv

'''
function to save data from website: www.briefing.com
input: date
output: stock rating table
exception: connection abortion
'''
def save_date(date_time):
	# split date to year, month, day
	d = date_time.split('-');
	
	table = pd.DataFrame();

	# iterate through different urls
	for cat in category:
		u = url + cat + '/' + d[0] + '/' + d[1] + '/' + d[2];

		# read in the parsed data from website
		text = opener.open(u).read();
		soup = BeautifulSoup(text, "lxml");

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

def main():
	# get web browser
	opener = getOpener();

	# url of briefing website
	url = "https://www.briefing.com/Investor/Calendars/Upgrades-Downgrades/";
	category = ["Upgrades", 'Downgrades', 'Initiated', 'Resumed', 'Reiterated'];

	# get the start date
	start_date = getLastDate('DataBriefing');
	# get the current date
	end_date = getCurrentDate();

	for single_date in dateRange(start_date, end_date):
		date_time = single_date.strftime("%Y-%m-%d");
		table = save_date(date_time);
		if (not table.empty):
			# modify the data frame to desired format
			table.columns = ['Brokerage', 'Date', 'Action', 'Company', 'Rating', 'Price_Target'];
			table['Brokerage'] = None;
			table['Brokerage'] = table['Action'];
			table['Action'] = table['Price_Target'];
			table['Price_Target'] = table['Rating'];
			table['Rating'] = table['Company'];
			table['Company'] = table['Date'];
			table['Date'] = date_time;

			# file path
			filename = date_time + ".xlsx";
			path = os.path.join(os.getcwd(), 'DataBriefing');
			filepath = os.path.join(path, filename);
			
			try:
				# save file
				table.to_excel(filepath);
				print('Save file: %s' % filename);
			except Exception as e:
				print('Unable to save file: %s' % filename);
		
		else:
			print('No data in %s' % single_date);

	#xlsxToCsv('BriefingData');
	pass;

if __name__ == "__main__":
	main();