# -*- coding: utf-8 -*-
"""
Created on Thu May  5 09:23:34 2016

@author: Swan
"""


import pandas as pd
import datetime
import matplotlib.pyplot as plt
from pylab import figure, axes, pie, title, show
from matplotlib.backends.backend_pdf import PdfPages

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot

from plotly.offline import plot
from plotly.graph_objs import Scatter

plt.style.use('ggplot')

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
for x in range(1, 150):
    #read in xls files
    xls_file = pd.ExcelFile('histData' + str(x) + '.xls')
    
    if '10502 Qtr' in xls_file.sheet_names:
        
        #This section is simply to get the date_pub variable to match with date_pub from urls
        hist_date = xls_file.parse(sheetname = '10502 Qtr', header=None)
        my_list = hist_date[0].astype(str)
        matching = [s for s in my_list if "Data published" in s]
        matching = [matching.replace("Data published","") for matching in matching]
        #change date into datime.date() format
        date_pub = datetime.datetime.strptime(matching[0].strip(' '), '%B %d, %Y').date()
        
        #Get the actual data values by parsing each xls file
        hist_file = xls_file.parse(sheetname = '10502 Qtr', skiprows=7, header=None)
        
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

#sort the file
hist_file_all.sort_values(by=['date_pub', 'line'], inplace=True)

#change two release dates so they match up
hist_file_all.ix[hist_file_all['date_pub']==pd.datetime(2007, 1, 31).date(), 'date_pub'] = pd.datetime(2007, 1, 27).date()
hist_file_all.ix[hist_file_all['date_pub']==pd.datetime(2007, 3, 29).date(), 'date_pub'] = pd.datetime(2007, 3, 30).date()

hist_file_all = pd.merge(hist_file_all, descrip, how='left', on='code')

hist_file_all["description_y"].fillna(hist_file_all["description_x"], inplace=True)
hist_file_all.drop('description_x', axis=1, inplace=True)
hist_file_all.rename(columns = {'description_y':'description'}, inplace = True)

#create final_data
final_data = pd.merge(long_file, hist_file_all, how='left', on=['date_pub', 'code'])

final_data.to_csv('final_data.csv')


#final_data.to_pickle('final_GDP_cont')
#final_data.to_excel('final_GDP_cont.xlsx')

pivot = final_data.pivot_table('value', ['line', 'code', 'description', 'date'], 'est')

#testing ground
test = pivot

test.reset_index(inplace=True)









#End testing ground











pivot['adv_less_second'] = pivot['ADVANCE'] - pivot['SECOND']
pivot['adv_less_third'] = pivot['ADVANCE'] - pivot['THIRD']
pivot['second_less_third'] = pivot['SECOND'] - pivot['THIRD']

pivot['abs_adv_less_second'] = abs(pivot['ADVANCE'] - pivot['SECOND'])
pivot['abs_adv_less_third'] = abs(pivot['ADVANCE'] - pivot['THIRD'])
pivot['abs_second_less_third'] = abs(pivot['SECOND'] - pivot['THIRD'])

pivot.reset_index(inplace=True)

#rolling_mean is deprecated and needs to be replaced with Series.rolling(min_periods=1,center=False,window=8).mean()
pivot['abs_two_year'] = pivot.groupby('code')['abs_adv_less_third'].apply(pd.rolling_mean, 8, min_periods=1)

pivot.sort_values(['date','line'],inplace=True)


abs_rev = PdfPages('abs_rev.pdf')
for i, group in pivot.groupby('description'):
    plt.figure()
    group.plot(x='date', y='abs_two_year', title=str(i))
    abs_rev.savefig()

abs_rev.close()



#if I use line as an index then the codes don't combine, if I don't i get out of order
abs_revision_index = pivot.pivot_table('abs_two_year', ['code', 'description'], 'date')
abs_revision_t = abs_revision_index.reset_index() 
#abs_revision_t.sort_values(['date','line'],inplace=True)  


tree = abs_revision_t[['code','2015_Q4']]
tree_map = pd.merge(descrip, tree, how='left', on='code')

tree_2 = pd.read_csv('tree_map_copy_manual.csv')



pp = PdfPages('multipage.pdf')

for i, group in final_data.groupby('description'):
    plt.figure()
    group.plot(x='date', y='value', title=str(i))
    pp.savefig()

pp.close()






           