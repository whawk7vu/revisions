# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:16:05 2016

@author: whawk
"""

import pandas as pd
import datetime
import gc
from bokeh.io import gridplot, output_file, show, vform
from bokeh.plotting import figure, output_file, show, save
import random
from jinja2 import Template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.charts import Bar


urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd. read_pickle('main_table')



#html_str = pivot[['code', 'description']].drop_duplicates(keep='first')
#<p><a href="A191RL1\A191RL1.html">A191RL1</a></p> 
#html_str['html_code'] = '<p><a href="' + html_str['code'] + '\\' + html_str['code'] + '.html">' + html_str['description'] + '</a></p>'
#html_str['html_code'].to_csv('html_code.csv')

html_str = pivot[['code', 'description']].drop_duplicates(keep='first')
#<p><a href="A191RL1\A191RL1.html">A191RL1</a></p> 
html_str['html_code'] = '<p><a href="' + html_str['code'] + '.html">' + html_str['description'] + '</a></p>'
html_str['html_code'].to_csv('html_code.csv')



main_table_list = ['A191RL1','DPCERY2', 'DGDSRY2', 'DSERRY2', 'A007RY2', 'A008RY2', 'A011RY2', 'A014RY2', 'A019RY2', 'A020RY2', 'A253RY2', 'A646RY2', 'A021RY2', 'A255RY2', 'A656RY2', 'A822RY2', 'A823RY2','A824RY2', 'A825RY2', 'A829RY2']
main_table_short = main_table[main_table['code'].isin(main_table_list)]


temp_graph = pivot[(pivot['code']=='A191RL1')]


#output_file('' + temp_graph['description'].iloc[0].strip().replace('\\', '') + '.html')

# create a new plot with a datetime axis type
p1 = figure(width=600, height=300, title=temp_graph['description'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['CURRENT'].min() - abs(temp_graph['CURRENT'].min()*.1), temp_graph['CURRENT'].max() + abs(temp_graph['CURRENT'].max()*.1)), outline_line_color = None)
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p1.yaxis.minor_tick_line_color = None
p1.xaxis.minor_tick_line_color = None
p1.quad(top=temp_graph['CURRENT'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10)) 

p1.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")

p1.legend.location = "bottom_left"


# create another one
temp_bar = temp_graph[['abs_current', 'abs_third_less_adv']].mean()
temp_bar = temp_bar.reset_index()
temp_bar = temp_bar.rename(columns = {0:'values'})    
p2 = Bar(temp_bar, 'est', values='values', title=temp_graph['description'].iloc[0], plot_width=400, plot_height=600, outline_line_color = None)
 

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
p4.line(temp_graph['date_t'], temp_graph['third_less_adv'], color='red', line_width=3, legend="Third less advanced")

p4.legend.location = "bottom_left"

# put all the plots in a grid layout
p = gridplot([[p1, p2], [p3, p4]])

# show the results
#show(p)


########## BUILD FIGURES ################

source = ColumnDataSource(main_table_short)
columns = [
        TableColumn(field='code', title = "BEA - Code", width = main_table['code'].map(len).max()),
        TableColumn(field='description', title = "Description", width = main_table['description'].map(len).max()),
        TableColumn(field='ADVANCE', title = "Advanced Est", width = 5),
        TableColumn(field='SECOND', title = "Second Est", width = 5),
        TableColumn(field='THIRD', title = "Third Est", width = 5),
        TableColumn(field='third_less_adv', title = "Revision (advance est less third est)", width = 10),
        TableColumn(field='abs_two_year', title = "Revision (absolute avg(2-year))", width = 10)
    ]
data_table = DataTable(source=source, columns=columns, width=1000, height=600)


########## RENDER PLOTS ################

# Define our html template for out plots
template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
          <link rel="stylesheet" href="html_page/styles/main.css">
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
              <p>GDP Revisions: <a href="GDP_index.html">Home</a></p>
              <p>More information on from the Bureau of Economic Analysis: <a href="http://www.bea.gov/newsreleases/national/gdp/gdpnewsrelease.htm">Gross Domestic Product</a></p>
            </div>
          </header>
          <main>
    <h2>Revisions to Gross Domestic Product</h2>
    <p>
      Gross domestic product (GDP), measures the value of the goods and services produced by
      the U.S. economy in a given time period. GDP is one of the most comprehensive and closely
      watched economic statistics.
    </p>
    <h3>What do we mean by "revision?"</h3>        
        <ul>
          <li>The change from initial release to "final" release</li>
            <ul>
            <li>These revisions are most noticed by policymakers and the business community: Yellen, POTUS, Wall Street,...</li>
            <li>Naming conventions vary across indicators</li>
            <li>Initial release may be called advance, preliminary, etc.</li>
            </ul>
          </li>
        </ul>
    <h3>Why does GDP revise?</h3>        
        <ul>
          <li>Revisions to economic indicator inputs due to:</li>
            <ul>
            <li>Late and corrected sample responses</li>
            <li>Concurrent seasonal adjustment</li>
            <li>Error corrections</li>
            </ul>
          </li>
          <li>Best source data not initially available</li>
            <ul>
            <li>Some key economic indicators are not available for use in the advance GDP estimates</li>
            <li>BEA imputes for them or uses alternative data sources, for example aggregate payroll hours data for health care industries from BLS instead of health care expenditures</li>
            </ul>
          </li>
        </ul>
    {{ plot_div.p }}
    
    <h3>Contributions to GDP revisions</h3>
    <p><a href="A191RL1\A191RL1.csv">Download GDP revisions csv</a></p>
    {{ plot_div.data_table }}
    {{ plot_script }}
    
    <div class = "data">
        <h3>Contributions to GDP revisions</h3>
    <p><a href="A191RL1.html">    Gross domestic product</a></p>
    <p><a href="A006RY2.html">Gross private domestic investment</a></p>
    <p><a href="A007RY2.html">  Fixed investment</a></p>
    <p><a href="A008RY2.html">    Nonresidential</a></p>
    <p><a href="A009RY2.html">      Structures</a></p>
    <p><a href="B935RY2.html">          Computers and peripheral equipment</a></p>
    <p><a href="B985RY2.html">        Software \4\</a></p>
    <p><a href="A937RY2.html">          Other</a></p>
    <p><a href="A680RY2.html">        Industrial equipment</a></p>
    <p><a href="A681RY2.html">        Transportation equipment</a></p>
    <p><a href="A862RY2.html">        Other equipment</a></p>
    <p><a href="A011RY2.html">    Residential</a></p>
    <p><a href="A014RY2.html">  Change in private inventories</a></p>
    <p><a href="B018RY2.html">    Farm</a></p>
    <p><a href="A015RY2.html">    Nonfarm</a></p>
    <p><a href="A019RY2.html">Net exports of goods and services</a></p>
    <p><a href="A020RY2.html">  Exports</a></p>
    <p><a href="A253RY2.html">    Goods</a></p>
    <p><a href="A646RY2.html">    Services</a></p>
    <p><a href="A021RY2.html">  Imports</a></p>
    <p><a href="A255RY2.html">    Goods</a></p>
    <p><a href="A656RY2.html">    Services</a></p>
    <p><a href="A822RY2.html">Government consumption expenditures and gross investment</a></p>
    <p><a href="A823RY2.html">  Federal</a></p>
    <p><a href="A824RY2.html">    National defense</a></p>
    <p><a href="A997RY2.html">      Consumption expenditures</a></p>
    <p><a href="A788RY2.html">      Gross investment</a></p>
    <p><a href="A825RY2.html">    Nondefense</a></p>
    <p><a href="A542RY2.html">      Consumption expenditures</a></p>
    <p><a href="A798RY2.html">      Gross investment</a></p>
    <p><a href="A829RY2.html">  State and local</a></p>
    <p><a href="A991RY2.html">    Consumption expenditures</a></p>
    <p><a href="A799RY2.html">    Gross investment</a></p>
    <p><a href="DPCERY2.html">Personal consumption expenditures</a></p>
    <p><a href="DGDSRY2.html">  Goods</a></p>
    <p><a href="DDURRY2.html">    Durable goods</a></p>
    <p><a href="DMOTRY2.html">      Motor vehicles and parts</a></p>
    <p><a href="DFDHRY2.html">      Furnishings and durable household equipment</a></p>
    <p><a href="DREQRY2.html">      Recreational goods and vehicles</a></p>
    <p><a href="DODGRY2.html">      Other durable goods</a></p>
    <p><a href="DNDGRY2.html">    Nondurable goods</a></p>
    <p><a href="DFXARY2.html">      Food and beverages purchased for off-premises consumption</a></p>
    <p><a href="DCLORY2.html">      Clothing and footwear</a></p>
    <p><a href="DGOERY2.html">      Gasoline and other energy goods</a></p>
    <p><a href="DONGRY2.html">      Other nondurable goods</a></p>
    <p><a href="DSERRY2.html">  Services</a></p>
    <p><a href="DHCERY2.html">    Household consumption expenditures (for services)</a></p>
    <p><a href="DHUTRY2.html">      Housing and utilities</a></p>
    <p><a href="DHLCRY2.html">      Health care</a></p>
    <p><a href="DTRSRY2.html">      Transportation services</a></p>
    <p><a href="DRCARY2.html">      Recreation services</a></p>
    <p><a href="DFSARY2.html">      Food services and accommodations</a></p>
    <p><a href="DIFSRY2.html">      Financial services and insurance</a></p>
    <p><a href="DOTSRY2.html">      Other services</a></p>
    <p><a href="DNPIRY2.html">    Final consumption expenditures of nonprofit institutions serving households (NPISHs) \1\</a></p>
    <p><a href="DNPERY2.html">      Gross output of nonprofit institutions \2\</a></p>
    <p><a href="DNPSRY2.html">      Less: Receipts from sales of goods and services by nonprofit institutions \3\</a></p>
    <p><a href="Y033RY2.html">      Equipment</a></p>
    <p><a href="Y034RY2.html">        Information processing equipment</a></p>
    <p><a href="Y001RY2.html">      Intellectual property products</a></p>
    <p><a href="Y006RY2.html">        Research and development \5\</a></p>
    <p><a href="Y020RY2.html">        Entertainment, literary, and artistic originals</a></p>


    </div>
    
    <h3>Data</h3>
    <a href="http://www.bea.gov/histdata/histChildLevels.cfm?HMI=7">BEA Data Archive - National accounts</a>
    </main>
    <footer></footer>
    </body>
</html>
''')

resources = INLINE

js_resources = resources.render_js()
css_resources = resources.render_css()

script, div = components({'p': p, 'data_table': data_table})

html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       plot_script=script,
                       plot_div=div)

filename = 'GDP_index.html'

with open(filename, 'w') as f:
    f.write(html)

#view(filename)

gc.collect()

gc.enable()


###############################


