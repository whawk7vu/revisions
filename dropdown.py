# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 13:43:28 2016

@author: whawk
"""

from bokeh.models import  Callback, ColumnDataSource, Rect, Select,CustomJS
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets.layouts import VBox,HBox
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
import numpy as np
from bokeh.io import vform, gridplot
import pandas as pd

urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd. read_pickle('main_table')

pivot.to_csv('GDP.csv')

output_file('Dropdown.html')


temp_graph = pivot[(pivot['code']=='DPCERY2')] 

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

#Figure for Stacked bar chart

for something in pivot['code'].unique():
    str('source%s'%something) =  ColumnDataSource(data=dict(x=country_both, y = yUnder5, y_full = yUnder5, height = heightUnder5, height_full = heightUnder5 ,height_zeros = zeros, y_zeros = heightUnder5 / 2.0))
    print(test)
    
    newpath) + '\%s.csv'%something

#source for callback
source1 = ColumnDataSource(data=dict(x=country_both, y = yUnder5, y_full = yUnder5, height = heightUnder5, height_full = heightUnder5 ,height_zeros = zeros, y_zeros = heightUnder5 / 2.0))
source2 = ColumnDataSource(data=dict(x=country_both, y = y15to49, y_full = y15to49, height = height15to49, height_full = height15to49,height_zeros = zeros, y_zeros = height15to49 / 2.0))
source3 = ColumnDataSource(data=dict(x=country_both, y = y50to69, y_full = y50to69, height = height50to69, height_full = height50to69,height_zeros = zeros , y_zeros = height50to69 / 2.0))
source4 = ColumnDataSource(data=dict(x=country_both, y = y70yr, y_full = y70yr, height = height70yr, height_full = height70yr,height_zeros = zeros, y_zeros =  height70yr / 2.0))

#Use rect glyphs for stached bars
p1.rect(x ='x', y ='y', width =.8, height = 'height', source = source1, color=redcolor5['Under 5 years'], alpha=0.8, name = "Under 5")
p1.rect(x = 'x', y ='y', width = .8, height ='height', source = source2, color=redcolor5['15-49 years'], alpha=0.8, name = "15 to 49")
p1.rect(x = 'x', y ='y', width = .8, height ='height', source = source3, color=redcolor5['50-69 years'], alpha = .8, name = "50 to 69")
p1.rect(x = 'x', y ='y', width = .8, height ='height', source = source4, color=redcolor5['70+ years'], alpha = .8, name = "70+ yrs")

#Java script Callbacks for age  
#I want this to recognize the 70+ year old drop down selection 
#and change the plot so that the height of the glyph is the same as the y value and the 70 year old glyph is the only one that displays
Callback_Age = CustomJS(args={'source1': source1,'source2': source2,'source3': source3,'source4': source4}, code="""
        var f = cb_obj.get('value');
        var data1 = source1.get('data');
        var data2 = source2.get('data');
        var data3 = source3.get('data');
        var data4 = source4.get('data');
        if (f == 'Under 5 years') {
            data3['height'] = data3['height_zeros'];
            data2['height'] = data2['height_zeros'];
            data4['height'] = data4['height_zeros'];
            data1['y'] = data1['y_zeros'];
            data1['height'] = data1['height_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }
        if (f == '15-49 years') {
            data1['height'] = data1['height_zeros'];
            data3['height'] = data3['height_zeros'];
            data4['height'] = data4['height_zeros'];
            data2['y'] = data2['y_zeros'];
            data2['height'] = data2['height_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }

        if (f == '50-69 years') {
            data1['height'] = data1['height_zeros'];
            data2['height'] = data2['height_zeros'];
            data4['height'] = data4['height_zeros'];
            data3['y'] = data3['y_zeros'];
            data3['height'] = data3['height_full'];
            console.log('data3',data3)
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }
        if (f == '70+ years') {
            data1['height'] = data1['height_zeros'];
            data2['height'] = data2['height_zeros'];
            data3['height'] = data3['height_zeros'];
            data4['y'] = data4['y_zeros'];
            data4['height'] = data4['height_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }
        if (f == 'All ages') {
            data1['height'] = data1['height_full'];
            data1['y'] = data1['y_full'];
            data2['height'] = data2['height_full'];
            data2['y'] = data2['y_full'];
            data3['height'] = data3['height_full'];
            data3['y'] = data3['y_full'];
            data4['height'] = data4['height_full'];
            data4['y'] = data4['y_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }



    """)
#Use the Select widget
dropdown_age = Select(title="Ages:", value=ages_gen[4], options= ages_gen,  callback = Callback_Age)

#Display data
filters = VBox(dropdown_age)
tot =  HBox(filters, gridplot([[p1]]))
show(tot)