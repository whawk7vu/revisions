# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:40:20 2016

@author: Swan
"""

import pandas as pd
import datetime

###
### Step 1.0 Create URLS dataframe 
###

#clean  up urls
urls = pd.read_csv('url.csv', index_col = 0)
urls.x = urls.x.str.upper()
urls.x = urls.x.str.replace('HTTP://WWW.BEA.GOV/HISTDATA/RELEASES/GDP_AND_PI/','')
urls.x = urls.x.str.replace('_','/')

#change to pandas dataframe
urls = pd.DataFrame(urls.x.str.split('/').tolist())

#rename columns
urls.columns = ['year', 'quarter', 'est', 'date', 'section', 'xls']

#Change date to datetime.date() object
urls['date_pub'] = urls['date'].apply(lambda x: datetime.datetime.strptime(x,'%B-%d-%Y').date())

#Change Estimate names
urls.est.replace({'PRELIMINARY': 'SECOND', 'FINAL': 'THIRD'}, regex=True, inplace=True)

#sort by date
urls.sort_values('date_pub', inplace=True)

#create date variable year_Q
urls['date'] = urls['year'] + '_' + urls['quarter']

#keep relevent columns
urls = urls[['date','est', 'date_pub']]

#keep only files after 2004_Q1
urls = urls[urls['date_pub'] >= pd.datetime(2004, 4, 1).date()]


#output urls to csv

#urls.to_csv('urls.csv')

###
#2.0 Read in 164 excel files
###

x=0
hist_file_all = pd.DataFrame()
long_file = pd.DataFrame()
#Range should be 1 to 150. using 10 just to test.
for x in range(1, 149):
    #read in xls files
    xls_file = pd.ExcelFile('histData' + str(x) + '.xls')
    
    if '10105 Qtr' in xls_file.sheet_names:
        
        #This section is simply to get the date_pub variable to match with date_pub from urls
        hist_date = xls_file.parse(sheetname = '10105 Qtr', header=None)
        my_list = hist_date[0].astype(str)
        matching = [s for s in my_list if "Data published" in s]
        matching = [matching.replace("Data published","") for matching in matching]
        #change date into datime.date() format
        date_pub = datetime.datetime.strptime(matching[0].strip(' '), '%B %d, %Y').date()
        
        #Get the actual data values by parsing each xls file
        hist_file = xls_file.parse(sheetname = '10105 Qtr', skiprows=7, header=None)
        
        #Change rows into column names
        hist_col = hist_file[:2].transpose()
        hist_col["period"] = hist_col[0].apply(str).str[:4] + '_Q' + hist_col[1].apply(str).str[:1]
        col_names = hist_col['period'].tolist()
        col_names[0] = 'line'
        col_names[1] = 'description'
        col_names[2] = 'code'
        col_names[-1] = 'value'
        hist_file.columns = col_names
        
        #drop NAs
        hist_file.dropna(inplace=True)
        
        #add date_pub to the files
        hist_file['date_pub'] = date_pub
        #test = hist_file[list(hist_file.columns[:2]) + list(hist_file.columns[:-2])].copy()
        
        
        hist_file = hist_file.ix[:,[0,1,2,-1,-2]]
        #Save these files to show what I want:        
        #hist_file.to_csv('mock'+str(x)+'.csv')
        hist_file_all = pd.concat([hist_file_all, hist_file])
        
        if x==1:
            codes = hist_file['code']
            urls_all = urls
            for item in codes:
                urls_all['code'] = item
                long_file = pd.concat([long_file, urls_all])

hist_file_all.sort_values(by=['date_pub', 'line'], inplace=True)
hist_file_all.ix[hist_file_all['date_pub']==pd.datetime(2007, 1, 31).date(), 'date_pub'] = pd.datetime(2007, 1, 27).date()
hist_file_all.ix[hist_file_all['date_pub']==pd.datetime(2007, 3, 29).date(), 'date_pub'] = pd.datetime(2007, 3, 30).date()
final_data = pd.merge(long_file, hist_file_all, how='left', on=['date_pub', 'code'])


'''                   
#Use this when you get the code going                    
    elif '101 Qtr' in xls_file.sheet_names:
        xls_file = xls_file.parse(sheetname = '101 Qtr', header=None)
        hist_file = xls_file.parse(sheetname = '101 Qtr', skiprows=7, skip_footer=0)
'''                   
        

           