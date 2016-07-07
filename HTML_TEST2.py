# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 17:18:11 2016

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
from bokeh.charts import Bar

final_gdp_data = pd.read_pickle('final_gdp_data')


for something in test['bea_code'].unique():
    temp_graph = final_gdp_data[(final_gdp_data['bea_code']==something)]

#    newpath = (r'C:\Users\whawk\revisions\%s'%something)
#    if not os.path.exists(newpath): 
#        os.makedirs(newpath)
#   temp_graph.to_csv(str(newpath) + '\%s.csv'%something)          
    temp_graph.to_csv('%s.csv'%something)      
    temp_path = '<p><a href="'+ temp_graph['bea_code'] + '">Download datafile (csv)</a></p>'
    
    #output_file(str(newpath) + '\%s.html'%something)
    
    p1 = figure(width=1000, height=500, title=temp_graph['category'].iloc[0], x_axis_type="datetime", y_range=(temp_graph['THIRD'].min() - abs(temp_graph['THIRD'].min()*.1), temp_graph['THIRD'].max() + abs(temp_graph['THIRD'].max()*.1)), outline_line_color = None)
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None
    p1.yaxis.minor_tick_line_color = None
    p1.xaxis.minor_tick_line_color = None
    p1.quad(top=temp_graph['THIRD'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10), legend="Third estimate") 
    
    p1.line(temp_graph['date_t'], temp_graph['third_less_adv'], color='red', line_width=3, legend="Third est less advanced est")
    
    p1.legend.location = "bottom_left"


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
    
    p3 = figure(width=1000, height=500, title=temp_graph['category'].iloc[0], x_axis_type="datetime", outline_line_color = None)
    p3.xgrid.grid_line_color = None
    p3.ygrid.grid_line_color = None
    p3.yaxis.minor_tick_line_color = None
    p3.xaxis.minor_tick_line_color = None
    p3.line(temp_graph['date_t'], temp_graph['abs_third_less_adv'], color='red', line_width=3, legend="Total abs third less advanced")
    
    p3.legend.location = "bottom_left"

        # create another one
    p4 = figure(width=1000, height=500, title=temp_graph['category'].iloc[0], x_axis_type="datetime",  outline_line_color = None)
    p4.xgrid.grid_line_color = None
    p4.ygrid.grid_line_color = None
    p4.yaxis.minor_tick_line_color = None
    p4.xaxis.minor_tick_line_color = None
    p4.quad(top=temp_graph['abs_third'], bottom=0, left=temp_graph['date_t'][:-1] + pd.DateOffset(10) , right=temp_graph['date_t'][1:] - pd.DateOffset(10), legend="Absolute change in third estimate") 
    
    p4.line(temp_graph['date_t'], temp_graph['abs_third_less_adv'], color='red', line_width=3, legend="Total abs third less advanced")
    
    p4.legend.location = "bottom_left"
       

    
    # put all the plots in a grid layout
    
    # show the results
    #show(p)
    
    
    ########## BUILD FIGURES ################
    
    source = ColumnDataSource(temp_graph)
    columns = [
            TableColumn(field='bea_code', title = "BEA - bea_code", width = temp_graph['bea_code'].map(len).max()),
            TableColumn(field='category', title = "category", width = temp_graph['category'].map(len).max()),
            TableColumn(field='date', title = "Date", width = temp_graph['date'].map(len).max()),
            TableColumn(field='ADVANCE', title = "Advanced Est", width = 5),
            TableColumn(field='THIRD', title = "Third Est", width = 5),
            TableColumn(field='third_less_adv', title = "Revision (third est less advance est)", width = 10),
            TableColumn(field='abs_third_less_adv', title = "Revision (absolute avg(2-year))", width = 10)
        ]
    data_table = DataTable(source=source, columns=columns, width=1000, height=1000)
    
    
    ########## RENDER PLOTS ################
    
    # Define our html template for out plots
    template = Template('''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="html_page/styles/main.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
    <title>GDP Revisions</title>
    {{ js_resources }} {{ css_resources }}
    <style type="text/css">
        ul {
            list-style: none;
            padding: 0px;
            margin: 0px;
        }
        
        ul li {
            display: block;
            position: relative;
            float: left;
            border: 1px solid #000
        }
        
        li ul {
            display: none;
        }
        
        ul li a {
            display: block;
            background: #000;
            padding: 5px 10px 5px 10px;
            text-decoration: none;
            white-space: nowrap;
            color: #fff;
        }
        
        ul li a:hover {
            background: #f00;
        }
        
        li:hover ul {
            display: block;
            position: absolute;
        }
        
        li:hover li {
            float: none;
        }
        
        li:hover a {
            background: #f00;
        }
        
        li:hover li a:hover {
            background: #000;
        }
        
        #drop-nav li ul li {
            border-top: 0px;
        }
    </style>
</head>

<body>
    <header>
        <div class="intro">
            <h1>GDP Revisions</h1>
            <p>GDP Revisions: <a href="C://Users//whawk//revisions//GDP_index.html">Home</a></p>
            <p>More information on from the Bureau of Economic Analysis: <a href="http://www.bea.gov/newsreleases/national/gdp/gdpnewsrelease.htm">Gross Domestic Product</a></p>
        </div>
    </header>
    <main>
        <div class="next">
            <ul id="drop-nav">
                <li><a href="A191RL1.html">GDP</a>
                    <ul>
                        <li><a href="DPCERY2.html">Personal consumption expenditures</a></li>
                        <li><a href="A006RY2.html">Gross private domestic investment</a></li>
                        <li><a href="A019RY2.html">Net exports of goods and services</a></li>
                        <li><a href="A822RY2.html">Government consumption expenditures and gross investment</a></li>
                    </ul>
                </li>
                <li><a href="DGDSRY2.html">Goods (PCE)</a>
                    <ul>
                        <li><a href="DDURRY2.html">    Durable goods</a></li>
                        <li><a href="DMOTRY2.html">      Motor vehicles and parts</a></li>
                        <li><a href="DFDHRY2.html">      Furnishings and durable household equipment</a></li>
                        <li><a href="DREQRY2.html">      Recreational goods and vehicles</a></li>
                        <li><a href="DODGRY2.html">      Other durable goods</a></li>
                        <li><a href="DNDGRY2.html">    Nondurable goods</a></li>
                        <li><a href="DFXARY2.html">      Food and beverages purchased for off-premises consumption</a></li>
                        <li><a href="DCLORY2.html">      Clothing and footwear</a></li>
                        <li><a href="DGOERY2.html">      Gasoline and other energy goods</a></li>
                        <li><a href="DONGRY2.html">      Other nondurable goods</a></li>
                    </ul>
                </li>
                <li><a href="DSERRY2.html">  Services (PCE)</a>
                    <ul>
                        <li><a href="DHCERY2.html">    Household consumption expenditures (for services)</a></li>
                        <li><a href="DHUTRY2.html">      Housing and utilities</a></li>
                        <li><a href="DHLCRY2.html">      Health care</a></li>
                        <li><a href="DTRSRY2.html">      Transportation servies</a></li>
                        <li><a href="DRCARY2.html">      Recreation services</a></li>
                        <li><a href="DFSARY2.html">      Food services and accommodations</a></li>
                        <li><a href="DIFSRY2.html">      Financial services and insurance</a></li>
                        <li><a href="DOTSRY2.html">      Other services</a></li>
                        <li><a href="DNPIRY2.html">    Final consumption expenditures of nonprofit institutions serving households (NPISHs) \1\</a></li>
                        <li><a href="Y033RY2.html">      Equipment</a></li>
                        <li><a href="Y034RY2.html">        Information processing equipment</a></li>
                        <li><a href="Y001RY2.html">      Intellectual property products</a></li>
                        <li><a href="Y006RY2.html">        Research and development \5\</a></li>
                        <li><a href="Y020RY2.html">        Entertainment, literary, and artistic originals</a></li>
                    </ul>
                </li>
                <li><a href="A006RY2.html">Investment</a>
                    <ul>
                        <li><a href="A007RY2.html">  Fixed investment</a></li>
                        <li><a href="A008RY2.html">    Nonresidential</a></li>
                        <li><a href="A009RY2.html">      Structures</a></li>
                        <li><a href="B935RY2.html">          Computers and peripheral equipment</a></li>
                        <li><a href="B985RY2.html">        Software \4\</a></li>
                        <li><a href="A937RY2.html">          Other</a></li>
                        <li><a href="A680RY2.html">        Industrial equipment</a></li>
                        <li><a href="A681RY2.html">        Transportation equipment</a></li>
                        <li><a href="A862RY2.html">        Other equipment</a></li>
                        <li><a href="A011RY2.html">    Residential</a></li>
                        <li><a href="A014RY2.html">  Change in private inventories</a></li>
                        <li><a href="B018RY2.html">    Farm</a></li>
                        <li><a href="A015RY2.html">    Nonfarm</a></li>
                    </ul>
                </li>
                <li><a href="A019RY2.html">Net exports</a>
                    <ul>
                        <li><a href="A020RY2.html">  Exports</a></li>
                        <li><a href="A253RY2.html">    Goods</a></li>
                        <li><a href="A646RY2.html">    Services</a></li>
                        <li><a href="A021RY2.html">  Imports</a></li>
                        <li><a href="A255RY2.html">    Goods</a></li>
                        <li><a href="A656RY2.html">    Services</a></li>
                    </ul>
                </li>
                <li><a href="A822RY2.html">Government</a>
                    <ul>
                        <li><a href="A823RY2.html">  Federal</a></li>
                        <li><a href="A824RY2.html">    National defense</a></li>
                        <li><a href="A997RY2.html">      Consumption expenditures</a></li>
                        <li><a href="A788RY2.html">      Gross investment</a></li>
                        <li><a href="A825RY2.html">    Nondefense</a></li>
                        <li><a href="A542RY2.html">      Consumption expenditures</a></li>
                        <li><a href="A798RY2.html">      Gross investment</a></li>
                        <li><a href="A829RY2.html">  State and local</a></li>
                        <li><a href="A991RY2.html">    Consumption expenditures</a></li>
                        <li><a href="A799RY2.html">    Gross investment</a></li>
                    </ul>
                </li>
            </ul>
        </div>

        <h2>Revisions to %s</h2> {{ plot_div.p1 }}
        <h2>Revisions to </h2> {{ plot_div.p2 }}
        <h2>Revisions to </h2> {{ plot_div.p3 }}
        <h2>Revisions to </h2> {{ plot_div.p4 }}

        <h3>%s revisions</h3>
        <p><a href="%s.csv">Download %s revisions csv</a></p>
        {{ plot_div.data_table }} {{ plot_script }}

    </main>
    <footer></footer>
</body>

</html>
    ''' % (temp_graph['category'].iloc[0].strip().replace('\\', ''), temp_graph['category'].iloc[0].strip().replace('\\', ''), something, temp_graph['category'].iloc[0].strip().replace('\\', '')))
    
    resources = INLINE
    
    js_resources = resources.render_js()
    css_resources = resources.render_css()
    
    script, div = components({'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4,'data_table': data_table})
    
    html = template.render(js_resources=js_resources,
                           css_resources=css_resources,
                           plot_script=script,
                           plot_div=div)
    
    filename = '%s.html'%something
    
    with open(filename, 'w') as f:
        f.write(html)
        f.close()
        






