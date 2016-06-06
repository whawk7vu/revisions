# -*- coding: utf-8 -*-
"""
Created on Thu May  5 09:23:34 2016

@author: Swan
"""

import bokeh
import pandas as pd
import datetime

from bokeh.plotting import figure, output_file, show, save

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


#get list for final data:
final_dates = list(set(urls['date'].values.tolist()))
final_dates.sort()


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
        
        #Create current values spreadsheet
        if x == 1:
            #Get the actual data values by parsing each xls file
            hist_file_current = xls_file.parse(sheetname = '10502 Qtr', skiprows=7, header=None)
            
            #Change rows into column names
            hist_col = hist_file_current[:2].transpose()
            hist_col["period"] = hist_col[0].apply(str).str[:4] + '_Q' + hist_col[1].apply(str).str[:1]
            col_names = hist_col['period'].tolist()
            col_names[0] = 'line'
            col_names[1] = 'description'
            col_names[2] = 'code'
            #col_names[-1] = 'value'
            hist_file_current.columns = col_names
            
            #drop NAs
            hist_file_current.dropna(inplace=True)
            
            #add date_pub to the files
            #hist_file_current['date_pub'] = date_pub
            #test = hist_file[list(hist_file.columns[:2]) + list(hist_file.columns[:-2])].copy()
            
            hist_file_current = pd.melt(hist_file_current, id_vars=["line", "description", "code"], 
                              var_name="date", value_name="current")
            hist_file_current = hist_file_current[(hist_file_current.date >= '2004_Q1')][['code','date','current']]        

        
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
            codes = hist_file['code']
            descrip = hist_file[['code','description']]
            line = hist_file[['line','code']]
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

final_data.dropna(inplace=True)

final_data.to_csv('final_data.csv')


#final_data.to_pickle('final_GDP_cont')
#final_data.to_excel('final_GDP_cont.xlsx')

pivot = final_data.pivot_table('value', ['line', 'code', 'description', 'date'], 'est')

pivot.reset_index(inplace=True)

pivot = pd.merge(pivot, hist_file_current, how='left', on=['code', 'date'])

pivot['adv_less_second'] = (pivot['ADVANCE'] - pivot['SECOND']).round(2)
pivot['adv_less_third'] = (pivot['ADVANCE'] - pivot['THIRD']).round(2)
pivot['second_less_third'] = (pivot['SECOND'] - pivot['THIRD']).round(2)

pivot['abs_adv_less_second'] = abs(pivot['ADVANCE'] - pivot['SECOND']).round(2)
pivot['abs_adv_less_third'] = abs(pivot['ADVANCE'] - pivot['THIRD']).round(2)
pivot['abs_second_less_third'] = abs(pivot['SECOND'] - pivot['THIRD']).round(2)


#rolling_mean is deprecated and needs to be replaced with Series.rolling(min_periods=1,center=False,window=8).mean()
pivot['abs_two_year'] = pivot.groupby('code')['abs_adv_less_third'].apply(pd.rolling_mean, 8, min_periods=1).round(2)

pivot.sort_values(['date','line'],inplace=True)


pivot['abs_adv_less_current'] = abs(pivot['ADVANCE'] - pivot['current']).round(2)
pivot['abs_third_less_current'] = abs(pivot['THIRD'] - pivot['current']).round(2)


pivot['year'] = pivot['date'].str[:4]
pivot['month'] = pivot['date'].str[-1:]

pivot['month'][pivot['month']=='4'] = '10'
pivot['month'][pivot['month']=='3'] = '7'
pivot['month'][pivot['month']=='2'] = '4'

pivot['date_t'] = pd.to_datetime(pivot['year']+pivot['month'],format='%Y%m')

main_table = pivot.drop(['line', 'year', 'month', 'date_t'], axis=1)

test_table = pivot.drop(['line', 'year', 'month'], axis=1)

test_table.to_csv('test_table.csv')

main_table = main_table[(main_table['date'] == main_table['date'].iloc[-1])]

main_table.to_csv('gdp_revisions.csv')
main_table.to_json('gdp_revisions.json')

main_table.to_html('main_table.html', classes = 'my_class" id = "gdp_main')

main_table_indexed = main_table.set_index(['code', 'description', 'date'])
main_table_indexed = main_table_indexed.stack()
main_table_indexed = main_table_indexed.reset_index()
main_table_indexed = main_table_indexed.rename(columns = {0:'value'})

main_table_indexed.to_csv('gdp_revisions.csv')


#if I use line as an index then the codes don't combine, if I don't i get out of order
abs_revision_index = pivot.pivot_table('abs_two_year', ['code', 'description'], 'date')
abs_revision_t = abs_revision_index.reset_index()
abs_revision_t = pd.merge(line, abs_revision_t, how='left', on=['code'])

abs_revision_t.to_csv('Two_year_abs_revision.csv')



for something in pivot['code'].unique():
    pivot[(pivot['code']==something)].to_csv('%s.csv'%something)
    
    temp_graph = pivot[(pivot['code']==something)]
    
    output_file('' + temp_graph['description'].iloc[0].strip().replace('\\', '') + '.html')
    
    # create a new plot with a datetime axis type
    p = figure(width=800, height=400, title=temp_graph['description'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['current'].min() - abs(temp_graph['current'].min()*.1), temp_graph['current'].max() + abs(temp_graph['current'].max()*.1)), outline_line_color = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.quad(top=temp_graph['current'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10)) 
    
    p.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")
    
    p.legend.location = "bottom_left"
    
    #show(p)
    save(p)
    


temp_graph = pivot[(pivot['code']=='A191RL1')]

output_file("line.html")

p = figure(plot_width=800, plot_height=400, title=temp_graph['description'].iloc[0], x_axis_type="datetime", outline_line_color = None )


p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.minor_tick_line_color = None

# add a line renderer
p.line(temp_graph['date_t'], temp_graph['adv_less_third'], color='red', line_width=3, legend="Revision")

p.legend.location = "bottom_left"

show(p)    


from bokeh.charts import Bar, output_file, show
from bokeh.sampledata.autompg import autompg as df

p = Bar(temp_graph, values='adv_less_third', title="Total MPG by CYL")

output_file("bar.html")

show(p)


    


output_file('' + temp_graph['description'].iloc[0].strip().replace('\\', '') + '.html')

# create a new plot with a datetime axis type
p = figure(width=800, height=400, title=temp_graph['description'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['current'].min() - abs(temp_graph['current'].min()*.1), temp_graph['current'].max() + abs(temp_graph['current'].max()*.1)), outline_line_color = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.minor_tick_line_color = None
p.quad(top=temp_graph['current'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10)) 

p.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")

p.legend.location = "bottom_left"

#show(p)
save(p)





from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform

output_file("data_table.html")

data_table = DataTable(source=main_table, width=400, height=280)

show(vform(data_table))
save(data_table)

from datetime import date
from random import randint

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform

output_file("data_table.html")

source = ColumnDataSource(main_table)

columns = [
        TableColumn(field=c, title=c) for c in main_table.columns 
    ]
data_table = DataTable(source=source, columns=columns, width=2000, height=1000)

show(vform(data_table))





#########################################################################################################



import random

from jinja2 import Template

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view

########## BUILD FIGURES ################

PLOT_OPTIONS = dict(plot_width=800, plot_height=300)
SCATTER_OPTIONS = dict(size=12, alpha=0.5)

data = lambda: [random.choice([i for i in range(100)]) for r in range(10)]

source = ColumnDataSource(main_table)
columns = [
        TableColumn(field=c, title=c) for c in main_table.columns 
    ]
data_table = DataTable(source=source, columns=columns, width=2000, height=1000)


red = figure(width=800, height=400, title=temp_graph['description'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['current'].min() - abs(temp_graph['current'].min()*.1), temp_graph['current'].max() + abs(temp_graph['current'].max()*.1)), outline_line_color = None)
red.xgrid.grid_line_color = None
red.ygrid.grid_line_color = None
red.yaxis.minor_tick_line_color = None
red.xaxis.minor_tick_line_color = None
red.quad(top=temp_graph['current'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10)) 
red.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")
red.legend.location = "bottom_left"


green = data_table


########## RENDER PLOTS ################

# Define our html template for out plots
template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Responsive plots</title>
        {{ js_resources }}
        {{ css_resources }}
    </head>
    <body>
    <h2>Resize the window to see some plots resizing</h2>
    <h3>Red - pan tool, responsive</h3>
    {{ plot_div.red }}
    <h3>Green - pan and resize tools, responsive (maintains new aspect ratio)</h3>
    {{ plot_div.green }}
    <h3>Blue - pan tool, not responsive</h3>
    {{ plot_div.blue }}
    {{ plot_script }}
    </body>
</html>
''')

resources = INLINE

js_resources = resources.render_js()
css_resources = resources.render_css()

script, div = components({'red': red, 'blue': blue, 'green': green})

html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       plot_script=script,
                       plot_div=div)

filename = 'embed_multiple_responsive.html'

with open(filename, 'w') as f:
    f.write(html)

view(filename)


###############################





           