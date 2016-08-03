# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 08:59:30 2016

@author: whawk
"""
import pandas as pd
#from bokeh.io import gridplot, output_file, show, vform
#from bokeh.plotting import figure, output_file, show, save
from bokeh.charts import Bar, Scatter, output_file, show
from bokeh.models import HoverTool, Range1d
from bokeh.plotting import figure, ColumnDataSource
from bokeh.charts.attributes import ColorAttr, CatAttr
from bokeh.charts.builders.bar_builder import BarBuilder
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn




final_gdp_data = pd.read_pickle('final_gdp_data')

gdp_data = pd.read_pickle('gdp_data')

gdp_data.to_excel('gdp_revisions_data.xlsx')

comp_list_cur = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2", 	"DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2", 	"DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2", 	"DNPIRY2", 	"A009RY2", 	"B935RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2", 	"B985RY2", 	"Y006RY2", 	"Y020RY2", 	"A011RY2", 	"B018RY2", 	"A015RY2", 	"A253RY2", 	"A646RY2", 	"A255RY2", 	"A656RY2", 	"A997RY2", 	"A788RY2", 	"A542RY2", 	"A798RY2", 	"A991RY2", 	"A799RY2"]

comp_list_ext = comp_list_cur + ["A165RY2", "A166RY2", "A167RY2", "A168RY2", "A169RY2", "A173RY2", "A172RY2", "A174RY2", "A175RY2", "A176RY2", "A177RY2", "A494RY2", "A490RY2", "A178RY2"]


test = gdp_data[(gdp_data['bea_code'].isin(comp_list_cur)) & (gdp_data['date'] == "2013_Q1")]

test.sort_values('abs_third_less_adv_simple', ascending=False, inplace=True)
test = test.head(10)
test.sort_values('line', inplace=True)

source = ColumnDataSource(test)
p1 = Bar(test, values='third_less_adv', title="GDP revisions for 2013_Q1", label=CatAttr(columns=['description'], sort=False), ylabel='Revision', xlabel='GDP Component', plot_width=1000, plot_height=1000)
#p1.x_range = FactorRange(factors=test['description'].tolist())
output_file('2013_Q1.html')
show(p1)


test2 = gdp_data[(gdp_data['bea_code'].isin(comp_list_cur)) & (gdp_data['date'] >= "2011_Q1")]

test3 = test2.groupby(test2['category']).mean().round(2)
test3.sort_values('line', inplace=True, ascending=True)
test3.reset_index(inplace=True)

test3[['category','third_less_adv']].to_excel('simple_revision.xlsx')
test3[['category', 'THIRD', 'abs_third_less_adv']].to_excel('abs_revision.xlsx')

source = ColumnDataSource(test3)
columns = [
        TableColumn(field='category', title = "category", width = test3['category'].map(len).max()),
        TableColumn(field='abs_third_less_adv', title = "Revision (third est less advance est)", width = 10)
    ]
data_table = DataTable(source=source, columns=columns, width=500, height=1000)
output_file('data_table.html')
show(data_table)









test3.sort_values('abs_third_less_adv', inplace=True, ascending=False)
test3.reset_index(inplace=True)

source = ColumnDataSource(test3)
p2 = Bar(test3, 'category', values='third_less_adv', title="GDP revisions for 2011 - 2015: Simple", plot_width=1000, plot_height=1000)

output_file('2011_2015_change.html')
show(p2)

p3 = Bar(test3, 'category', values='abs_third_less_adv', title="GDP revisions for 2011 - 2015: absoulte value", plot_width=1000, plot_height=1000)

output_file('2011_2015_abs_change.html')
show(p3)

















test2 = gdp_data[gdp_data['bea_code'] == "A191RL1"]


output_file("scatter.html")

fig = figure(plot_width=500, plot_height=500)
df = test2
x = 'abs_third_less_adv_simple'
y = 'abs_third_less_adv'

def scatter_with_hover(df, x, y,
                       fig=None, cols=None, name=None, marker='x',
                       fig_width=500, fig_height=500, **kwargs):
    """
    Plots an interactive scatter plot of `x` vs `y` using bokeh, with automatic
    tooltips showing columns from `df`.
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data to be plotted
    x : str
        Name of the column to use for the x-axis values
    y : str
        Name of the column to use for the y-axis values
    fig : bokeh.plotting.Figure, optional
        Figure on which to plot (if not given then a new figure will be created)
    cols : list of str
        Columns to show in the hover tooltip (default is to show all)
    name : str
        Bokeh series name to give to the scattered data
    marker : str
        Name of marker to use for scatter plot
    **kwargs
        Any further arguments to be passed to fig.scatter
    Returns
    -------
    bokeh.plotting.Figure
        Figure (the same as given, or the newly created figure)
    Example
    -------
    fig = scatter_with_hover(df, 'A', 'B')
    show(fig)
    fig = scatter_with_hover(df, 'A', 'B', cols=['C', 'D', 'E'], marker='x', color='red')
    show(fig)
    Author
    ------
    Robin Wilson <robin@rtwilson.com>
    with thanks to Max Albert for original code example
    """

    # If we haven't been given a Figure obj then create it with default
    # size etc.
    if fig is None:
        fig = figure(width=fig_width, height=fig_height, tools=['box_zoom', 'reset'])

    # We're getting data from the given dataframe
    source = ColumnDataSource(data=df)

    # We need a name so that we can restrict hover tools to just this
    # particular 'series' on the plot. You can specify it (in case it
    # needs to be something specific for other reasons), otherwise
    # we just use 'main'
    if name is None:
        name = 'main'

    # Actually do the scatter plot - the easy bit
    # (other keyword arguments will be passed to this function)
    fig.scatter(df[x], df[y], source=source, name=name, marker=marker, **kwargs)

    # Now we create the hover tool, and make sure it is only active with
    # the series we plotted in the previous line
    hover = HoverTool(names=[name])

    if cols is None:
        # Display *all* columns in the tooltips
        hover.tooltips = [(c, '@' + c) for c in df.columns]
    else:
        # Display just the given columns in the tooltips
        hover.tooltips = [(c, '@' + c) for c in cols]

    hover.tooltips.append(('index', '$index'))

    # Finally add/enable the tool
    fig.add_tools(hover)
    
    return fig


p2 = scatter_with_hover(test2, 'abs_third_less_adv_simple', 'abs_third_less_adv', marker='circle', fig_width=800, fig_height=800, cols=['bea_code', 'date', 'abs_third_less_adv_simple', 'abs_third_less_adv'], size=20)
p2.title ="Offsetting revisions"
p2.xaxis.axis_label="Absolute (third less adv)"
p2.yaxis.axis_label="Aggregate absolute (third less adv)"
p2.x_range= Range1d(0,test2['abs_third_less_adv_simple'].max()*1.1)
p2.y_range= Range1d(0,test2['abs_third_less_adv'].max()*1.1)

sum_rev = test2['abs_third_less_adv']
simple = test2['abs_third_less_adv_simple']

regression = np.polyfit(simple, sum_rev, 1)
r_x, r_y = zip(*((i, i*regression[0] + regression[1]) for i in range(len(test2['abs_third_less_adv']))))
p2.line(r_x, r_y, color="red", line_width=6)
output_file("regression.html")
show(p2)

























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
