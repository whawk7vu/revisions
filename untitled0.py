# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:44:10 2016

@author: Swan
"""

#test

import pandas as pd
import datetime

xls_file = pd.ExcelFile('histData1.xls')

hist_file = xls_file.parse(sheetname = '10502 Qtr', skiprows=7, header=None)

#Change rows into column names
hist_col = hist_file.transpose()
hist_col["period"] = hist_col[0].apply(str).str[:4] + '_Q' + hist_col[1].apply(str).str[:1]
col_names = hist_col['period'].tolist()
col_names[0] = 'line'
col_names[1] = 'description'
col_names[2] = 'code'
#col_names[-1] = 'value'
hist_file.columns = col_names

#drop NAs
hist_file.dropna(inplace=True)
hist_col.dropna(inplace=True)

'''
# change codes for consistency
hist_file.ix[hist_file['code']=='A002RY2', 'code'] = 'DPCERY2'
hist_file.ix[hist_file['code']=='A003RY2', 'code'] = 'DDURRY2'
hist_file.ix[hist_file['code']=='A004RY2', 'code'] = 'DNDGRY2'
hist_file.ix[hist_file['code']=='A005RY2', 'code'] = 'DSERRY2'
'''

#add date_pub to the files
hist_file['date_pub'] = date_pub
#test = hist_file[list(hist_file.columns[:2]) + list(hist_file.columns[:-2])].copy()

# keep columns 1-3 and the last 2
hist_file = hist_file.ix[:,[0,1,2,-1,-2]]
#Save these files to show what I want:        
#hist_file.to_csv('mock'+str(x)+'.csv')

#create a large file with all the data together
hist_file_all = pd.concat([hist_file_all, hist_file])

#if reading in the most recent vintage, create a long_file with the current GDP codes
if x==1:
    hist_file_current = hist_file
    codes = hist_file['code']
    descrip = hist_file[['code','description']]
    urls_all = urls
    for item in codes:
        urls_all['code'] = item
        long_file = pd.concat([long_file, urls_all])