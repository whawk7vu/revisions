# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:16:05 2016

@author: whawk
"""

import pandas as pd
import datetime

from bokeh.plotting import figure, output_file, show, save


urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd. read_pickle('main_table')

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

PLOT_OPTIONS = dict(plot_width=800, plot_height=300)
SCATTER_OPTIONS = dict(size=12, alpha=0.5)

data = lambda: [random.choice([i for i in range(100)]) for r in range(10)]

source = ColumnDataSource(temp_graph)
columns = [
        TableColumn(field=c, title=c) for c in temp_graph.columns 
    ]
data_table = DataTable(source=source, columns=columns, width=2000, height=1000)

green = data_table


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
    {{ plot_div.green }}
    <h3>Blue - pan tool, not responsive</h3>
    {{ plot_div.blue }}
    {{ plot_script }}
    
    <footer></footer>
    </body>
</html>
''')

resources = INLINE

js_resources = resources.render_js()
css_resources = resources.render_css()

script, div = components({'p': p, 'green': green})

html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       plot_script=script,
                       plot_div=div)

filename = 'embed_multiple_responsive.html'

with open(filename, 'w') as f:
    f.write(html)

view(filename)


###############################













temp_graph = pivot[(pivot['code']=='A191RL1')]
output_file('' + temp_graph['description'].iloc[0].strip().replace('\\', '') + '.html')

# create a new plot with a datetime axis type
p1 = figure(width=800, height=400, title=temp_graph['description'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['current'].min() - abs(temp_graph['current'].min()*.1), temp_graph['current'].max() + abs(temp_graph['current'].max()*.1)), outline_line_color = None)
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p1.yaxis.minor_tick_line_color = None
p1.xaxis.minor_tick_line_color = None
p1.quad(top=temp_graph['current'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10)) 

p1.line(temp_graph['date_t'], temp_graph['abs_two_year'], color='red', line_width=3, legend="Two-year absolute revision")

p1.legend.location = "bottom_left"

show(p1)
#save(p)






















from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn


#data table
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

script, div = components({'red': red, 'green': green})

html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       plot_script=script,
                       plot_div=div)

filename = 'embed_multiple_responsive.html'

with open(filename, 'w') as f:
    f.write(html)

view(filename)


###############################

