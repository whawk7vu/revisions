# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 09:54:02 2016

@author: whawk
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import datetime

from bokeh.plotting import figure, output_file, show, save
from bokeh.io import gridplot, output_file, show, vform
from bokeh.plotting import figure
import random
from jinja2 import Template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
import os, sys
from bokeh.charts import Bar

urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd.read_pickle('main_table')

something = 'A011RY2' 

temp_graph = pivot[(pivot['code']==something)]

newpath = (r'C:\Users\whawk\revisions\%s'%something)
if not os.path.exists(newpath): 
    os.makedirs(newpath)

pivot[(pivot['code']==something)].to_csv(str(newpath) + '\%s.csv'%something)  
    

    
temp_graph = pivot[(pivot['code']==something)]

temp_path = '<p><a href="' + temp_graph['code'] + '\\' + temp_graph['code'] + '">Download datafile (csv)</a></p>'

#output_file(str(newpath) + '\%s.html'%something)

p1 = figure(width=600, height=300, title=temp_graph['description'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['CURRENT'].min() - abs(temp_graph['CURRENT'].min()*.1), temp_graph['CURRENT'].max() + abs(temp_graph['CURRENT'].max()*.1)), outline_line_color = None)
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p1.yaxis.minor_tick_line_color = None
p1.xaxis.minor_tick_line_color = None
p1.quad(top=temp_graph['CURRENT'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10)) 

p1.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")

p1.legend.location = "bottom_left"

temp_bar = temp_graph[['abs_current', 'abs_adv_less_third']].mean()
temp_bar = temp_bar.reset_index()
temp_bar = temp_bar.rename(columns = {0:'values'})    
p2 = Bar(temp_bar, 'est', values='values', title=temp_graph['description'].iloc[0], plot_width=400, plot_height=600, outline_line_color = None)
#p2.xgrid.grid_line_color = None
#p2.ygrid.grid_line_color = None
#p2.yaxis.minor_tick_line_color = None
#p2.xaxis.minor_tick_line_color = None

# create another one
p3 = figure(width=600, height=300, title=temp_graph['description'].iloc[0], x_axis_type="datetime", outline_line_color = None)
p3.xgrid.grid_line_color = None
p3.ygrid.grid_line_color = None
p3.yaxis.minor_tick_line_color = None
p3.xaxis.minor_tick_line_color = None
p3.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")

p3.legend.location = "bottom_left"

p4 = figure(width=600, height=300, title=temp_graph['description'].iloc[0], x_axis_type="datetime", outline_line_color = None)
p4.xgrid.grid_line_color = None
p4.ygrid.grid_line_color = None
p4.yaxis.minor_tick_line_color = None
p4.xaxis.minor_tick_line_color = None
p4.line(temp_graph['date_t'], temp_graph['adv_less_current'], color='red', line_width=3, legend="Advance less current")

p4.legend.location = "bottom_left"

# put all the plots in a grid layout
p = gridplot([[p1, p2], [p3, p4]])

# show the results
#show(p)


########## BUILD FIGURES ################

source = ColumnDataSource(temp_graph)
columns = [
        TableColumn(field='code', title = "BEA - Code", width = temp_graph['code'].map(len).max()),
        TableColumn(field='description', title = "Description", width = temp_graph['description'].map(len).max()),
        TableColumn(field='date', title = "Date", width = temp_graph['date'].map(len).max()),
        TableColumn(field='ADVANCE', title = "Advanced Est", width = 5),
        TableColumn(field='SECOND', title = "Second Est", width = 5),
        TableColumn(field='THIRD', title = "Third Est", width = 5),
        TableColumn(field='adv_less_third', title = "Revision (advance est less third est)", width = 10),
        TableColumn(field='abs_two_year', title = "Revision (absolute avg(2-year))", width = 10)
    ]
data_table = DataTable(source=source, columns=columns, width=1000, height=1000)


########## RENDER PLOTS ################

# Define our html template for out plots
template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
          <link rel="stylesheet" href="C:\\Users\\whawk\\revisions\\html_page\\styles\\main.css">
          <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
          <script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
        <title>GDP Revisions</title>
        {{ js_resources }}
        {{ css_resources }}
    </head>
    <body>
        <header>
            <div class="intro">
              <h1>GDP Revisions</h1>
              <p>GDP Revisions: <a href="C://Users//whawk//revisions//GDP_index.html">Home</a></p>
              <p>More information on from the Bureau of Economic Analysis: <a href="http://www.bea.gov/newsreleases/national/gdp/gdpnewsrelease.htm">Gross Domestic Product</a></p>
            </div>
          </header>
    
    <h2>Revisions to %s</h2>
    {{ plot_div.p }}
    
    <h3>%s revisions</h3>
    <p><a href="%s.csv">Download %s revisions csv</a></p>
    {{ plot_div.data_table }}
    {{ plot_script }}
    
    
        <h3>Contributions to GDP revisions</h3>
    <p><a href="A191RL1\A191RL1.html">    Gross domestic product</a></p>
    <p><a href="A006RY2\A006RY2.html">Gross private domestic investment</a></p>
    <p><a href="A007RY2\A007RY2.html">  Fixed investment</a></p>
    <p><a href="A008RY2\A008RY2.html">    Nonresidential</a></p>
    <p><a href="A009RY2\A009RY2.html">      Structures</a></p>
    <p><a href="B935RY2\B935RY2.html">          Computers and peripheral equipment</a></p>
    <p><a href="B985RY2\B985RY2.html">        Software \4\</a></p>
    <p><a href="A937RY2\A937RY2.html">          Other</a></p>
    <p><a href="A680RY2\A680RY2.html">        Industrial equipment</a></p>
    <p><a href="A681RY2\A681RY2.html">        Transportation equipment</a></p>
    <p><a href="A862RY2\A862RY2.html">        Other equipment</a></p>
    <p><a href="A011RY2\A011RY2.html">    Residential</a></p>
    <p><a href="A014RY2\A014RY2.html">  Change in private inventories</a></p>
    <p><a href="B018RY2\B018RY2.html">    Farm</a></p>
    <p><a href="A015RY2\A015RY2.html">    Nonfarm</a></p>
    <p><a href="A019RY2\A019RY2.html">Net exports of goods and services</a></p>
    <p><a href="A020RY2\A020RY2.html">  Exports</a></p>
    <p><a href="A253RY2\A253RY2.html">    Goods</a></p>
    <p><a href="A646RY2\A646RY2.html">    Services</a></p>
    <p><a href="A021RY2\A021RY2.html">  Imports</a></p>
    <p><a href="A255RY2\A255RY2.html">    Goods</a></p>
    <p><a href="A656RY2\A656RY2.html">    Services</a></p>
    <p><a href="A822RY2\A822RY2.html">Government consumption expenditures and gross investment</a></p>
    <p><a href="A823RY2\A823RY2.html">  Federal</a></p>
    <p><a href="A824RY2\A824RY2.html">    National defense</a></p>
    <p><a href="A997RY2\A997RY2.html">      Consumption expenditures</a></p>
    <p><a href="A788RY2\A788RY2.html">      Gross investment</a></p>
    <p><a href="A825RY2\A825RY2.html">    Nondefense</a></p>
    <p><a href="A542RY2\A542RY2.html">      Consumption expenditures</a></p>
    <p><a href="A798RY2\A798RY2.html">      Gross investment</a></p>
    <p><a href="A829RY2\A829RY2.html">  State and local</a></p>
    <p><a href="A991RY2\A991RY2.html">    Consumption expenditures</a></p>
    <p><a href="A799RY2\A799RY2.html">    Gross investment</a></p>
    <p><a href="DPCERY2\DPCERY2.html">Personal consumption expenditures</a></p>
    <p><a href="DGDSRY2\DGDSRY2.html">  Goods</a></p>
    <p><a href="DDURRY2\DDURRY2.html">    Durable goods</a></p>
    <p><a href="DMOTRY2\DMOTRY2.html">      Motor vehicles and parts</a></p>
    <p><a href="DFDHRY2\DFDHRY2.html">      Furnishings and durable household equipment</a></p>
    <p><a href="DREQRY2\DREQRY2.html">      Recreational goods and vehicles</a></p>
    <p><a href="DODGRY2\DODGRY2.html">      Other durable goods</a></p>
    <p><a href="DNDGRY2\DNDGRY2.html">    Nondurable goods</a></p>
    <p><a href="DFXARY2\DFXARY2.html">      Food and beverages purchased for off-premises consumption</a></p>
    <p><a href="DCLORY2\DCLORY2.html">      Clothing and footwear</a></p>
    <p><a href="DGOERY2\DGOERY2.html">      Gasoline and other energy goods</a></p>
    <p><a href="DONGRY2\DONGRY2.html">      Other nondurable goods</a></p>
    <p><a href="DSERRY2\DSERRY2.html">  Services</a></p>
    <p><a href="DHCERY2\DHCERY2.html">    Household consumption expenditures (for services)</a></p>
    <p><a href="DHUTRY2\DHUTRY2.html">      Housing and utilities</a></p>
    <p><a href="DHLCRY2\DHLCRY2.html">      Health care</a></p>
    <p><a href="DTRSRY2\DTRSRY2.html">      Transportation services</a></p>
    <p><a href="DRCARY2\DRCARY2.html">      Recreation services</a></p>
    <p><a href="DFSARY2\DFSARY2.html">      Food services and accommodations</a></p>
    <p><a href="DIFSRY2\DIFSRY2.html">      Financial services and insurance</a></p>
    <p><a href="DOTSRY2\DOTSRY2.html">      Other services</a></p>
    <p><a href="DNPIRY2\DNPIRY2.html">    Final consumption expenditures of nonprofit institutions serving households (NPISHs) \1\</a></p>
    <p><a href="DNPERY2\DNPERY2.html">      Gross output of nonprofit institutions \2\</a></p>
    <p><a href="DNPSRY2\DNPSRY2.html">      Less: Receipts from sales of goods and services by nonprofit institutions \3\</a></p>
    <p><a href="Y033RY2\Y033RY2.html">      Equipment</a></p>
    <p><a href="Y034RY2\Y034RY2.html">        Information processing equipment</a></p>
    <p><a href="Y001RY2\Y001RY2.html">      Intellectual property products</a></p>
    <p><a href="Y006RY2\Y006RY2.html">        Research and development \5\</a></p>
    <p><a href="Y020RY2\Y020RY2.html">        Entertainment, literary, and artistic originals</a></p>
    <footer></footer>
    </body>
</html>
''' % (temp_graph['description'].iloc[0].strip().replace('\\', ''), temp_graph['description'].iloc[0].strip().replace('\\', ''), something, temp_graph['description'].iloc[0].strip().replace('\\', '')))

resources = INLINE

js_resources = resources.render_js()
css_resources = resources.render_css()

script, div = components({'p': p, 'data_table': data_table})

html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       plot_script=script,
                       plot_div=div)

filename = str(newpath) + '\%s.html'%something

with open(filename, 'w') as f:
    f.write(html)