# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:36:44 2016

@author: whawk
"""
import pandas as pd
from bokeh.models import  Callback, ColumnDataSource, Rect, Select,CustomJS
from bokeh.plotting import figure, output_file, show,  gridplot
from bokeh.models.widgets.layouts import VBox,HBox

output_file("dropdown.html")

#Plot for one code
GDP_temp = GDP[(GDP['code']=='A006RY2')]

p1 = figure(width=600, height=300, title=GDP_temp['code'].iloc[0], x_axis_type="datetime")
p1.line(GDP_temp['date'], GDP_temp['value'])
show(p1)

#Plot for each code
for something in GDP['code'].unique():
    temp_GDP = GDP[(GDP['code']==something)]
    p1 = figure(width=600, height=300, title=temp_GDP['code'].iloc[0], x_axis_type="datetime")
    p1.line(temp_GDP['date'], temp_GDP['value'])
    show(p1)
    

Callback_code = CustomJS()

#Use the Select widget
dropdown_code = Select(title="Code", value=GDP['value'], callback = Callback_code)

#Display data
filters = VBox(dropdown_code)
tot =  HBox(filters, gridplot([[p1]]))
show(tot)