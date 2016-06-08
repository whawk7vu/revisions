# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:34:35 2016

@author: WHawk
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
from bokeh.charts import Bar, defaults

defaults.width = 600
defaults.height = 300

urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd.read_pickle('main_table')


temp_graph = pivot[(pivot['code']=='DPCERY2')] 
    
output_file('test.html')

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

# create another one
#p2 = figure(width=600, height=300, title=temp_graph['description'].iloc[0], outline_line_color = None)
#p2.quad(top=temp_bar['values'], bottom=0, left)

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
        TableColumn(field='ADVANCE', title = "Advanced Est", width = 5),
        TableColumn(field='SECOND', title = "Second Est", width = 5),
        TableColumn(field='THIRD', title = "Third Est", width = 5),
        TableColumn(field='adv_less_third', title = "Revision (advance est less third est)", width = 10),
        TableColumn(field='abs_two_year', title = "Revision (absolute avg(2-year))", width = 10)
    ]
data_table = DataTable(source=source, columns=columns, width=1000, height=1000)


layout = vform(p, data_table)

#show(layout)
save(layout)