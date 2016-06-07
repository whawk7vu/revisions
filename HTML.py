# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:16:05 2016

@author: whawk
"""

import pandas as pd
import datetime
import gc

from bokeh.plotting import figure, output_file, show, save


urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd. read_pickle('main_table')

main_table_list = ['A191RL1','DPCERY2', 'DGDSRY2', 'DSERRY2', 'A007RY2', 'A008RY2', 'A011RY2', 'A014RY2', 'A019RY2', 'A020RY2', 'A253RY2', 'A646RY2', 'A021RY2', 'A255RY2', 'A656RY2', 'A822RY2', 'A823RY2','A824RY2', 'A825RY2', 'A829RY2']
main_table_short = main_table[main_table['code'].isin(main_table_list)]


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

temp_graph = pivot[(pivot['code']=='A191RL1')]


output_file('' + temp_graph['description'].iloc[0].strip().replace('\\', '') + '.html')

# create a new plot with a datetime axis type
p1 = figure(width=600, height=300, title=temp_graph['description'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['current'].min() - abs(temp_graph['current'].min()*.1), temp_graph['current'].max() + abs(temp_graph['current'].max()*.1)), outline_line_color = None)
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p1.yaxis.minor_tick_line_color = None
p1.xaxis.minor_tick_line_color = None
p1.quad(top=temp_graph['current'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10)) 

p1.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")

p1.legend.location = "bottom_left"


# create another one
p2 = figure(width=600, height=300, title=temp_graph['description'].iloc[0], x_axis_type="datetime", outline_line_color = None)
p2.xgrid.grid_line_color = None
p2.ygrid.grid_line_color = None
p2.yaxis.minor_tick_line_color = None
p2.xaxis.minor_tick_line_color = None
p2.line(temp_graph['date_t'], temp_graph['adv_less_third'], color='red', line_width=3, legend="Advanced less third")

p2.legend.location = "bottom_left"

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

source = ColumnDataSource(main_table_short)
columns = [
        TableColumn(field='code', title = "BEA - Code", width = main_table['code'].map(len).max()),
        TableColumn(field='description', title = "Description", width = main_table['description'].map(len).max()),
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
              <p>More information on from the Bureau of Economic Analysis:</p>
              <a href="http://www.bea.gov/newsreleases/national/gdp/gdpnewsrelease.htm">Gross Domestic Product</a>
            </div>
          </header>
    
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
    <a href="https://raw.githubusercontent.com/whawk7vu/revisions/master/A191RL1.csv">Download GDP revisions csv</a>
    {{ plot_div.data_table }}
    {{ plot_script }}
    <h3>Data</h3>
    <a href="http://www.bea.gov/histdata/histChildLevels.cfm?HMI=7">BEA Data Archive - National accounts</a>
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

filename = 'embed_multiple_responsive.html'

with open(filename, 'w') as f:
    f.write(html)

view(filename)

gc.collect()

gc.enable()


###############################


