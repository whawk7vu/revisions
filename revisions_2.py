# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:40:20 2016

@author: Swan
"""

import pandas as pd
import datetime

#Create URLS dataframe 
urls = pd.read_csv('url.csv', index_col = 0)

urls.x = urls.x.str.upper()

urls.x = urls.x.str.replace('HTTP://WWW.BEA.GOV/HISTDATA/RELEASES/GDP_AND_PI/','')

urls.x = urls.x.str.replace('_','/')

urls = pd.DataFrame(urls.x.str.split('/').tolist())

urls.columns = ['year', 'quarter', 'est', 'date', 'section', 'xls']

urls['date_pub'] = urls['date'].apply(lambda x: datetime.datetime.strptime(x,'%B-%d-%Y').date())

urls.est.replace({'PRELIMINARY': 'SECOND', 'FINAL': 'THIRD'}, regex=True, inplace=True)

urls.sort_values('date_pub', inplace=True)

urls['date'] = urls['year'] + '_' + urls['quarter']

urls = urls[['date','est', 'date_pub']]

urls.to_csv('urls.csv')





x=0
for x in range(1, 10):
    xls_file = pd.ExcelFile('histData' + str(x) + '.xls')
    
    if '10105 Qtr' in xls_file.sheet_names:
        p = xls_file.parse(sheetname = '10105 Qtr', header=None)
        my_list = p[0].astype(str)
        matching = [s for s in my_list if "Data published" in s]
        matching = [matching.replace("Data published","") for matching in matching]
        matching
        date_pub = datetime.datetime.strptime(matching[0].strip(' '), '%B %d, %Y').date()
        
        f = xls_file.parse(sheetname = '10105 Qtr', skiprows=7, header=None)
        fb = f[:2].transpose()
        
        fb["period"] = fb[0].apply(str).str[:4] + '_Q' + fb[1].apply(str).str[:1]
        
        col_names = fb['period'].tolist()
        col_names[0] = 'Line'
        col_names[1] = 'Description'
        col_names[2] = 'Code'
        
        f.columns = col_names
        f.dropna(inplace=True)
        f['date_pub'] = date_pub
        
        
        result =  pd.DataFrame()
        
        iterrows()
                
        for frow in f.iterrows():
            for r in urls.iterrows():
                result['Code'] = frow['Code']
                result['date'] = r['date']
                result['est'] = r['est']
                result['date_pub'] = r['date_pub']
                result['value'] = r['value']
            
            
        
        
        for row in values:
            for innerrow in f:
                if innerrow['date_pub'] == values['date_pub']:
                    print("True")
                else:
                    print("False")
                    
                    
                    
values['value'].append(f.ix[:,-2])
                    
f_test = f.iloc[0]
f_test['date_pub']
urls_test = urls.iloc[0]
urls_test['date_pub']

if f_test['date_pub'] == urls_test['date_pub']:
    print("True")
else:
    print("False")
            
            
            
            
            if values['date_pub'] == f
    
            print(row)
            
            result['Name']=row['Code']
            print(dictNames[result])
            for innerrow in urls:
                if innerrow['date_pub'] == row['date_pub']:
                    print(row['date_pub'])
                    
grades.append('A')
                    
f['Code'][0]                  
dictNames = {}                    
print(result)
dictNames[result] = pd.DataFrame()

A829RC1                   
urls['date_pub'][0]
f['date_pub'][0]

urls['date_pub'].describe
f['date_pub'].describe


result['value'] = 111            
dictNames[result]         
 #           for innerrow in urls:
#                 result['value']=urls.ix[:,-2]

x = "spam"
>>> z = {x: "eggs"}
>>> z["spam"]
'eggs'
                
            
result
            
result=f['Code'].to_string()
        
        for row in urls:
            if([urls['date_pub'] == A191RC1['date_pub']]):
                urls['value'] = test.ix[:,-2]

        
  
print(code_a)
















  elif '101a Qtr' in xls_file.sheet_names:
        p = xls_file.parse(sheetname = '101 Qtr', header=None)
        my_list = p[0].astype(str).tolist()
        matching = [s for s in my_list if "Data published" in s]
        date_pub = matching[0]       
        f = xls_file.parse(sheetname = '101 Qtr', skiprows=7, skip_footer=0)
        f.dropna(inplace=True)
        f['date_pub'] = date_pub
        #f.to_csv('GDP'+str(x)+'.csv')
    





#Create 'f' file which is 1 of 163 files    
xls_file = pd.ExcelFile('histData146.xls')
p = xls_file.parse(sheetname = '10105 Qtr', header=None)
my_list = p[0].astype(str)
matching = [s for s in my_list if "Data published" in s]
matching = [matching.replace("Data published ","") for matching in matching]
date_pub = datetime.datetime.strptime(matching[0] , '%B %d, %Y ').date()

f = xls_file.parse(sheetname = '10105 Qtr', skiprows=7, header=None)
fb = f[:2].transpose()

fb["period"] = fb[0].apply(str).str[:4] + '_Q' + fb[1].apply(str).str[:1]

col_names = fb['period'].tolist()

col_names[0] = 'Line'
col_names[1] = 'Description'
col_names[2] = 'Code'

f.columns = col_names
f.dropna(inplace=True)
f['date_pub'] = date_pub

f.to_csv('GDP'+str(x)+'.csv')







#merge urls with f files 

g = f.loc[f['Code'] == 'A191RC1']
for row in urls:
    if([urls['date_pub'] == A191RC1['date_pub']]):
        urls['value'] = test.ix[:,-2]
