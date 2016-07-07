# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 12:47:54 2016

@author: whawk
"""
import pandas as pd
from bokeh.plotting import figure, output_file, show, save
from bokeh.charts import Bar
import numpy as np

final_gdp_data = pd.read_pickle('final_gdp_data')

test = final_gdp_data 


test['after12'] = np.where(test['date']>='2012_Q1', 'After', 'Before')


test = test.groupby(['category', 'after12']).mean().reset_index()

test.to_excel('Retail_sales2.xlsx')


temp_graph = final_gdp_data[(final_gdp_data['bea_code']=='DFSARY2')]        
temp_bar = temp_graph[['THIRD', 'abs_third_simple', 'abs_third']].mean()
temp_bar = temp_bar.reset_index()
temp_bar = temp_bar.rename(columns = {0:'values'})
p2 = figure(x_range=temp_bar['est'].values.tolist())
p2.quad(top=temp_bar['values'], bottom=0, left=temp_bar['est'].values.tolist(), right=temp_bar['est'].values.tolist(), line_width=100, color=["blue","yellow","red"]) 
#p2.text([.5, 2.5], [.5, .5], text=['Yes', 'No'], text_font_size="20pt", text_align='center')

#p2.xgrid.grid_line_color = None
#p2.ygrid.grid_line_color = None
p2.yaxis.minor_tick_line_color = None
p2.xaxis.minor_tick_line_color = None
#added these two lines
p2.y_range.start = 0
p2.y_range.end = temp_bar['values'].max()*1.1

p3 = figure(width=600, height=300, title=temp_graph['category'].iloc[0], x_axis_type="datetime", outline_line_color = None)
p3.xgrid.grid_line_color = None
p3.ygrid.grid_line_color = None
p3.yaxis.minor_tick_line_color = None
p3.xaxis.minor_tick_line_color = None
p3.line(temp_graph['date_t'], temp_graph['abs_third_less_adv'], color='red', line_width=3, legend="Total absolute revision")

p3.legend.location = "bottom_left"

output_file("p3.html")
show(p3)


p1.quad(top=temp_graph['THIRD'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10), legend="Third estimate") 


plot.quad(top=[2, 3, 4], bottom=[1, 2, 3], left=[1, 2, 3],
    right=[1.2, 2.5, 3.7], color=["green","red","blue"])






p4 = figure(width=600, height=300, title=temp_graph['category'].iloc[0], x_axis_type="datetime", outline_line_color = None)
p4.xgrid.grid_line_color = None
p4.ygrid.grid_line_color = None
p4.yaxis.minor_tick_line_color = None
p4.xaxis.minor_tick_line_color = None
p4.line(temp_graph['date_t'], temp_graph['third_less_adv'], color='red', line_width=3, legend="Third less advanced")

p4.legend.location = "bottom_left"

show(p4)

from bokeh.plotting import figure, output_file, show

plot = figure(width=300, height=300)
plot.annulus(x=[1, 2, 3], y=[1, 2, 3], color="#7FC97F",
             inner_radius=0.2, outer_radius=0.5)

show(plot)


plot = figure(width=300, height=300)
plot.quad(top=[2, 3, 4], bottom=[1, 2, 3], left=[1, 2, 3],
    right=[1.2, 2.5, 3.7], color=["green","red","blue"])

show(plot)


plot = figure(toolbar_location=None,
                      plot_width=800,
                      plot_height=400,
                      x_range=(0, 3),
                      y_range=(0, 10),
                      title='mytitle',
                      min_border=10,
                      min_border_left=50,
                      title_text_font_size='12pt')
plot.quad(bottom=0, left=[0, 1, 2], right=[1, 2, 3],
          top=[0, 0, 0], color="green", name='mytitle')
plot.text([.5, 2.5], [.5, .5], text=['Yes', 'No'],
           text_font_size="20pt", text_align='center')
plot.xaxis.visible = None
plot.xgrid.grid_line_color = None

output_file("p2.html")
show(plot)

datastore = plot.select_one(dict(name=question)).data_source



from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d
import pandas as pd

output_file("bars.html")

df = pd.DataFrame()
df['y_att1'] = [0.70,0.68,0.50,0.48,0.30,0.28]
df['x_att1'] = ['b','d','a','h','f','e']

p = figure(title="twin y-axis bar example", x_range=df['x_att1'].values.tolist())

p.quad(bottom=0, top=df['y_att1'], left=df['x_att1'].values.tolist()
    , right=df['x_att1'].values.tolist(), line_width=7, line_color='red')

p.yaxis.axis_label = 'left y axis'
p.yaxis.axis_label_text_color = 'red'

#added these two lines
p.y_range.start = 0
p.y_range.end = df['y_att1'].max()*1.1

p.xaxis.axis_label = 'x axis'
p.xaxis.axis_label_standoff = -5

show(p)

