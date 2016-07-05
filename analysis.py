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

urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
pivot_all = pd.read_pickle('pivot_all')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd. read_pickle('main_table')

comp_gdp = pivot

#Current vintage - lowest level
#gdp_list = ["A191RL1"]
comp_list = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2", 	"DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2", 	"DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2", 	"DNPIRY2", 	"A009RY2", 	"B935RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2", 	"B985RY2", 	"Y006RY2", 	"Y020RY2", 	"A011RY2", 	"B018RY2", 	"A015RY2", 	"A253RY2", 	"A646RY2", 	"A255RY2", 	"A656RY2", 	"A997RY2", 	"A788RY2", 	"A542RY2", 	"A798RY2", 	"A991RY2", 	"A799RY2"] 
durgoods_list = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2"]
nondurgoods_list = ["DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2"]
houseserv_list = ["DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2"]
nonprofserv_list = ["DNPIRY2"]
struct_list = ["A009RY2"]
info_list = ["B935RY2", "A937RY2"]
indust_list = ["A680RY2"]
trans_list = ["A681RY2"]
othequip_list = ["A862RY2"]
intprop_list = ["B985RY2", "Y006RY2", "Y020RY2"]
resinv_list = ["A011RY2"]
inventory_list = ["B018RY2", 	"A015RY2"]
export_list = ["A253RY2", 	"A646RY2"]
import_list = ["A255RY2", 	"A656RY2"]
fedgovdef_list = ["A997RY2", 	"A788RY2"]
fedgovnondef_list =["A542RY2", 	"A798RY2"]
sandlgov_list = ["A991RY2", 	"A799RY2"]

#comp_gdp = comp_gdp[comp_gdp['date_t'] >= pd.datetime(2013, 4, 1).date()]

comp_gdp['category'] = ""

#lowest Level
comp_gdp['category'][comp_gdp['code'].isin(durgoods_list)] = "Durable goods"
comp_gdp['category'][comp_gdp['code'].isin(nondurgoods_list)] = "Nondurable goods"
comp_gdp['category'][comp_gdp['code'].isin(houseserv_list)] = "Household consumption for services"
comp_gdp['category'][comp_gdp['code'].isin(nonprofserv_list)] = "Nonprofit consumption for services"
comp_gdp['category'][comp_gdp['code'].isin(struct_list)] = "Structures"
comp_gdp['category'][comp_gdp['code'].isin(info_list)] = "Information processing"
comp_gdp['category'][comp_gdp['code'].isin(indust_list)] = "Industrial equipment"
comp_gdp['category'][comp_gdp['code'].isin(trans_list)] = "Transportation equipment"
comp_gdp['category'][comp_gdp['code'].isin(othequip_list)] = "Other equipment"
comp_gdp['category'][comp_gdp['code'].isin(intprop_list)] = "Intellectual property"
comp_gdp['category'][comp_gdp['code'].isin(resinv_list)] = "Residential investment"
comp_gdp['category'][comp_gdp['code'].isin(inventory_list)] = "Change in private inventories"
comp_gdp['category'][comp_gdp['code'].isin(export_list)] = "Exports"
comp_gdp['category'][comp_gdp['code'].isin(import_list)] = "Imports"
comp_gdp['category'][comp_gdp['code'].isin(fedgovdef_list)] = "Federal government - defense"
comp_gdp['category'][comp_gdp['code'].isin(fedgovnondef_list)] = "Federal government - nondefense"
comp_gdp['category'][comp_gdp['code'].isin(sandlgov_list)] = "State and local government"

cat1 = comp_gdp[comp_gdp['code'].isin(comp_list)]
cat1 = cat1.groupby([cat1['category'], cat1['date']]).sum()

#next level
goods_list = durgoods_list + nondurgoods_list
serv_list = houseserv_list + nonprofserv_list
equip_list = info_list + indust_list + trans_list + othequip_list
netexport_list = export_list + import_list
fed_list = fedgovdef_list + fedgovnondef_list


comp_gdp['category2'] = ""
comp_gdp['category2'][comp_gdp['code'].isin(goods_list)] = "Goods"
comp_gdp['category2'][comp_gdp['code'].isin(serv_list)] = "Services"
comp_gdp['category2'][comp_gdp['code'].isin(equip_list)] = "Equipment"
comp_gdp['category2'][comp_gdp['code'].isin(netexport_list)] = "Net exports"
comp_gdp['category2'][comp_gdp['code'].isin(fed_list)] = "Federal government"

comp_list2 = goods_list + serv_list + equip_list + netexport_list + fed_list

cat2 = comp_gdp[comp_gdp['code'].isin(comp_list2)]
cat2 = cat2.groupby([cat2['category2'], cat2['date']]).sum()

#next level
pce_list = goods_list + serv_list
nonres_list = struct_list + equip_list + intprop_list 
gov_list = fed_list + sandlgov_list

comp_gdp['category3'] = ""
comp_gdp['category3'][comp_gdp['code'].isin(pce_list)] = "Personal consumption expenditures"
comp_gdp['category3'][comp_gdp['code'].isin(nonres_list)] = "Nonresidential investment"
comp_gdp['category3'][comp_gdp['code'].isin(gov_list)] = "Government"

comp_list3 = pce_list + nonres_list + gov_list

cat3 = comp_gdp[comp_gdp['code'].isin(comp_list3)]
cat3 = cat3.groupby([cat3['category3'], cat3['date']]).sum()

#next level
fixedinv_list = nonres_list + resinv_list

comp_gdp['category4'] = ""
comp_gdp['category4'][comp_gdp['code'].isin(fixedinv_list)] = "Fixed investment"

comp_list4 = fixedinv_list

cat4 = comp_gdp[comp_gdp['code'].isin(comp_list4)]
cat4 = cat4.groupby([cat4['category4'], cat4['date']]).sum()


#next level
inv_list = fixedinv_list + inventory_list

comp_gdp['category5'] = ""
comp_gdp['category5'][comp_gdp['code'].isin(inv_list)] = "Investment"

comp_list5 = inv_list

cat5 = comp_gdp[comp_gdp['code'].isin(comp_list5)]
cat5 = cat5.groupby([cat5['category5'], cat5['date']]).sum()

#next level
gdp_list = pce_list + inv_list + netexport_list + gov_list

comp_gdp['category6'] = ""
comp_gdp['category6'][comp_gdp['code'].isin(gdp_list)] = "Gross domestic product"

comp_list6 = gdp_list

cat6 = comp_gdp[comp_gdp['code'].isin(comp_list6)]
cat6 = cat6.groupby([cat6['category6'], cat6['date']]).sum()

frames = [cat1, cat2, cat3, cat4, cat5, cat6]

gdp_data = pd.concat(frames)

gdp_data = gdp_data.reset_index(level=[]).reset_index().sort_values(by=['category', 'date'])

final_gdp_data = gdp_data[['category', 'date', 'ADVANCE', 'THIRD', 'abs_third', 'third_less_adv', 'abs_third_less_adv']]
#comp_gdp["id"] = comp_gdp["code"] + " - " + comp_gdp["category"] + " - " + comp_gdp["description"]


''' Leftover code
abs_rev = abs_rev['abs_third_less_adv'].groupby([abs_rev['id'], abs_rev['date']]).mean().unstack().sum()

comp_gdp_childs = comp_gdp[comp_gdp['code'].isin(comp_list)]
abs_rev = comp_gdp[comp_gdp['code'].isin(gdp_list)]
abs_rev = abs_rev['abs_third_less_adv'].groupby([abs_rev['id'], abs_rev['date']]).mean().unstack().sum()
tot_abs_rev = comp_gdp_childs['abs_third_less_adv'].groupby([comp_gdp_childs['id'], comp_gdp_childs['date']]).mean().unstack().sum()

#gdp revisions
gdp = pd.concat([tot_abs_rev , abs_rev], axis=1)
gdp.columns = ['tot_abs_rev', 'abs_rev']
gdp.reset_index(level=0, inplace=True)

#second vintage

gdp_list = ["A191RL1"]
comp_list = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2", 	"DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2", 	"DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2", 	"DNPERY2", 	"DNPSRY2", 	"A009RY2", 	"B935RY2", 	"B985RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2", 	"A011RY2", 	"B018RY2", 	"A015RY2", 	"A253RY2", 	"A646RY2", 	"A255RY2", 	"A656RY2", 	"A997RY2", 	"A788RY2", 	"A542RY2", 	"A798RY2", 	"A991RY2", 	"A799RY2"] 
durgoods_list = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2"]
nondurgoods_list = ["DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2"]
serv_list = ["DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2", 	"DNPERY2", 	"DNPSRY2"]
nonresinv_list = ["A009RY2", 	"B935RY2", 	"B985RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2"]
resinv_list = ["A011RY2"]
inventory_list = ["B018RY2", 	"A015RY2"]
export_list = ["A253RY2", 	"A646RY2"]
import_list = ["A255RY2", 	"A656RY2"]
fedgovdef_list = ["A997RY2", 	"A788RY2"]
fedgovnondef_list =["A542RY2", 	"A798RY2"]
sandlgov_list = ["A991RY2", 	"A799RY2"]


#old vintage
gdp_list = ["A191RL1"]
comp_list = ["A165RY2", 	"A166RY2", 	"A167RY2", 	"A168RY2", 	"A169RY2", 	"A173RY2", 	"A172RY2", 	"A174RY2", 	"A175RY2", 	"A176RY2", 	"A494RY2", 	"A490RY2", 	"A178RY2", 	"A009RY2", 	"B935RY2", 	"B985RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2", 	"A011RY2", 	"A014RY2", 	"A253RY2", 	"A646RY2", 	"A255RY2", 	"A656RY2", 	"A997RY2", 	"A788RY2", 	"A542RY2", 	"A798RY2", 	"A991RY2", 	"A799RY2"] 
durgoods_list = ["A165RY2", 	"A166RY2", 	"A167RY2"]
nondurgoods_list = ["A168RY2", 	"A169RY2", 	"A173RY2", 	"A172RY2"]
serv_list = ["A174RY2", 	"A175RY2", 	"A176RY2", 	"A494RY2", 	"A490RY2", 	"A178RY2"]
nonresinv_list = ["A009RY2", 	"B935RY2", 	"B985RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2"]
resinv_list = ["A011RY2"]
inventory_list = ["B018RY2", "A015RY2"]
export_list = ["A253RY2", 	"A646RY2"]
import_list = ["A255RY2", 	"A656RY2"]
fedgovdef_list = ["A997RY2", 	"A788RY2"]
fedgovnondef_list =["A542RY2", 	"A798RY2"]
sandlgov_list = ["A991RY2", 	"A799RY2"]
'''

gdp_test = pivot[pivot['code'].isin(gdp_list)]

plt.xkcd()



pp = PdfPages('multipage.pdf')
for i, group in pivot.groupby('description'):
    #plt.figure()
    group.plot(x='date', y='third_less_adv', title= "Revision of " + str(i).strip())
    pp.savefig()
pp.close()
abs_rev = PdfPages('abs_rev.pdf')
for i, group in pivot.groupby('description'):
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
