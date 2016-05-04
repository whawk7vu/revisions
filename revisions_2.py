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
#output urls to csv
#urls.to_csv('urls.csv')

###
#2.0 Read in 164 excel files
###

x=0
#Range should be 1 to 150. using 10 just to test.
for x in range(1, 10):
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
        col_names[0] = 'Line'
        col_names[1] = 'Description'
        col_names[2] = 'Code'
        hist_file.columns = col_names
        
        #drop NAs
        hist_file.dropna(inplace=True)
        
        #add date_pub to the files
        hist_file['date_pub'] = date_pub
        #test = hist_file[list(hist_file.columns[:2]) + list(hist_file.columns[:-2])].copy()

        #Save these files to show what I want:        
       #hist_file.to_csv('mock'+str(x)+'.csv')


###        
#This is where I can't figure it out
###
        
test = hist_file[hist_file.columns[0:3], hist_file.columns[4]] 

newdf = df[df.columns[2:4]]


        result =  pd.DataFrame()
                
        for hist_row in hist_file.iterrows():
            for urls_row in urls.iterrows():
                result['Code'] = hist_row['Code']
                result['date'] = urls_row['date']
                result['est'] = urls_row['est']
                result['date_pub'] = urls_row['date_pub']
                result['value'] = urls_row['value']
            
        for hist_row in hist_file:
            for urls_row in urls:
                if hist_row['date_pub'] == urls_row['date_pub']:
                    print("True")
                else:
                    print("False")
'''                   
#Use this when you get the code going                    
    elif '101 Qtr' in xls_file.sheet_names:
        xls_file = xls_file.parse(sheetname = '101 Qtr', header=None)
        hist_file = xls_file.parse(sheetname = '101 Qtr', skiprows=7, skip_footer=0)
'''                   
                    
#Testing ground

hist_test = hist_file  
urls_test = urls     
final_test = urls  

for index1, row1 in hist_test.iterrows():
    
    for index2, row2 in urls_test.iterrows():
        
        if row1['date_pub'] == row2['date_pub']:
            final_test['value'] = hist_test.ix[:,-2]
            print("True")
        else:
            print("False")
        



for r in hist_test:
    print(hist_test['Code'][0])

if hist_test['date_pub'] == urls_test['date_pub']:
    print("True")
else:
    print("False")
            
                    
xls_file = pd.ExcelFile('histData2.xls')

hist_date = xls_file.parse(sheetname = '10105 Qtr', header=None)

my_list = hist_date[0].astype(str)
matching = [s for s in my_list if "Data published" in s]
matching = [matching.replace("Data published","") for matching in matching]
date_pub = datetime.datetime.strptime(matching[0].strip(' '), '%B %d, %Y').date()

hist_file = xls_file.parse(sheetname = '10105 Qtr', skiprows=7, header=None)
hist_col = hist_file[:2].transpose()

hist_col["period"] = hist_col[0].apply(str).str[:4] + '_Q' + hist_col[1].apply(str).str[:1]

col_names = hist_col['period'].tolist()
col_names[0] = 'Line'
col_names[1] = 'Description'
col_names[2] = 'Code'

hist_file.columns = col_names
hist_file.dropna(inplace=True)
hist_file['date_pub'] = date_pub
#Save these files to show what I want:        
hist_file.to_csv('mock2.csv')