# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 08:59:30 2016

@author: whawk
"""
import pandas as pd
import datetime
import gc
from bokeh.io import gridplot, output_file, show, vform
from bokeh.plotting import figure, output_file, show, save
import random
from jinja2 import Template
import numpy as np
from matplotlib import pyplot as plt
from pylab import figure, axes, pie, title, show
from matplotlib.backends.backend_pdf import PdfPages

final_gdp_data = pd.read_pickle('final_gdp_data')


plt.xkcd()

pp = PdfPages('multipage.pdf')
for i, group in final_gdp_data.groupby('category'):
    #plt.figure()
    group.plot(x='date', y='third_less_adv', title= "Revision of " + str(i).strip())
    pp.savefig()
pp.close()
abs_rev = PdfPages('abs_rev.pdf')
for i, group in final_gdp_data.groupby('category'):
    plt.figure()
    group.plot(x='date', y='abs_third_less_adv', title= "Absolute revision of " + str(i).strip())
    abs_rev.savefig()
abs_rev.close()



# Setting the positions and width for the bars
pos = list(range(len(test['abs_rev'])))
width = 0.25

# Plotting the bars
fig, ax = plt.subplots(figsize=(10,5))

# Create a bar with pre_score data,
# in position pos,
plt.bar(pos,
        #using df['pre_score'] data,
        test['tot_abs_rev'],
        # of width
        width,
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#EE3224',
        # with label the first value in first_name
        label=gdp_test['description'][0])

# Create a bar with mid_score data,
# in position pos + some width buffer,
plt.bar([p + width for p in pos],
        #using df['mid_score'] data,
        test['abs_rev'],
        # of width
        width,
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#F78F1E',
        # with label the second value in first_name
        label=gdp_test['description'][1])

# Set the y axis label
ax.set_ylabel('Absolute change')

# Set the chart's title
ax.set_title('Absolute Revision')

# Set the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

# Set the labels for the x ticks
ax.set_xticklabels(test['date'])

# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*4)
plt.ylim([0, max(test['tot_abs_rev'] + test['abs_rev'])] )

# Adding the legend and showing the plot
plt.legend(['Total absolute revision', 'Abosulte revision'], loc='upper left')
plt.grid()
plt.show()
