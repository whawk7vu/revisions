# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 10:00:11 2016

@author: WHawk
"""

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
