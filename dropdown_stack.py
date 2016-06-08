# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:36:44 2016

@author: whawk
"""

from bokeh.io import gridplot, output_file, show, vform
from bokeh.plotting import figure
import random
from jinja2 import Template
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show,  gridplot, save
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.models import Callback, ColumnDataSource, Rect, Select, CustomJS
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

output_file("dropdown_%s.html")

pivot = pd.read_pickle('pivot')

GDP = pivot

#Plot for one code
GDP_temp = GDP[(GDP['code']=='A006RY2')]

p1 = figure(width=600, height=300, title=GDP_temp['code'].iloc[0], x_axis_type="datetime")
p1.line(GDP_temp['date_t'], GDP_temp['abs_adv_less_current'])
#show(p1)

source = ColumnDataSource(GDP_temp)

columns = [
    TableColumn(field='code', title = "BEA - Code", width = GDP_temp['code'].map(len).max()),
    TableColumn(field='description', title = "Description", width = GDP_temp['description'].map(len).max()),
    TableColumn(field='ADVANCE', title = "Advanced Est", width = 5),
    TableColumn(field='SECOND', title = "Second Est", width = 5),
    TableColumn(field='THIRD', title = "Third Est", width = 5),
    TableColumn(field='adv_less_third', title = "Revision (advance est less third est)", width = 10),
    TableColumn(field='abs_two_year', title = "Revision (absolute avg(2-year))", width = 10)
    ]

data_table = DataTable(source=source, columns=columns, width=1000, height=1000)

layout = vform(p1, data_table)

show(layout)
save(layout)

save('layout%s'%something)

print('layout%s'%something)

something = 'A006RY2'

str(newpath + '\%s.csv'%something) = 4

(str(newpath) + '\%s.csv'%something)

'%s.csv'%something = 4




d ={}
#Plot for each code
for something in GDP['code'].unique():
    temp_GDP = GDP[(GDP['code']==something)]
    p1 = figure(width=600, height=300, title=temp_GDP['code'].iloc[0], x_axis_type="datetime")
    p1.line(temp_GDP['date'], temp_GDP['value'])
#    show(p1)
        
    
    
    
    
    
    source = ColumnDataSource(temp_GDP)

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


layout = vform(p, data_table)

show(layout)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

Callback_code = CustomJS()

#Use the Select widget
dropdown_code = Select(title="Code", value=GDP['value'], callback = Callback_code)

#Display data
filters = VBox(dropdown_code)
tot =  HBox(filters, gridplot([[p1]]))
show(tot)