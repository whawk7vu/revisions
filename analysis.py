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
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.charts import Bar


urls = pd.read_pickle('urls')
final_data = pd.read_pickle('final_data')
pivot = pd.read_pickle('pivot')
abs_revision_t = pd.read_pickle('abs_revision_t')
abs_revision_index = pd.read_pickle('abs_revision_index')
main_table = pd. read_pickle('main_table')


comp_list = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2", 	"DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2", 	"DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2", 	"DNPIRY2", 	"A009RY2", 	"B935RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2", 	"B985RY2", 	"Y006RY2", 	"Y020RY2", 	"A011RY2", 	"B018RY2", 	"A015RY2", 	"A253RY2", 	"A646RY2", 	"A255RY2", 	"A656RY2", 	"A997RY2", 	"A788RY2", 	"A542RY2", 	"A798RY2", 	"A991RY2", 	"A799RY2"] 
durgoods_list = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2"]
nondurgoods_list = ["DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2"]
serv_list = ["DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2", 	"DNPIRY2"]
nonresinv_list = ["A009RY2", 	"B935RY2", 	"A937RY2", 	"A680RY2", 	"A681RY2", 	"A862RY2", 	"B985RY2", 	"Y006RY2", 	"Y020RY2"]
resinv_list = ["A011RY2"]
inventory_list = ["B018RY2", 	"A015RY2"]
export_list = ["A253RY2", 	"A646RY2"]
import_list = ["A255RY2", 	"A656RY2"]
fedgovdef_list = ["A997RY2", 	"A788RY2"]
fedgovnondef_list =["A542RY2", 	"A798RY2"]
sandlgov_list = ["A991RY2", 	"A799RY2"]

comp_gdp = pivot[pivot['code'].isin(comp_list)]
comp_gdp['category'] = ""

comp_gdp['category'][comp_gdp['code'].isin(durgoods_list)] = "Durable goods"
comp_gdp['category'][comp_gdp['code'].isin(nondurgoods_list)] = "Nondurable goods"
comp_gdp['category'][comp_gdp['code'].isin(serv_list)] = "Services"
comp_gdp['category'][comp_gdp['code'].isin(nonresinv_list)] = "Nonresidential investment"
comp_gdp['category'][comp_gdp['code'].isin(resinv_list)] = "Residential investment"
comp_gdp['category'][comp_gdp['code'].isin(inventory_list)] = "Change in private inventories"
comp_gdp['category'][comp_gdp['code'].isin(export_list)] = "Exports"
comp_gdp['category'][comp_gdp['code'].isin(import_list)] = "Imports"
comp_gdp['category'][comp_gdp['code'].isin(fedgovdef_list)] = "Federal government - defense"
comp_gdp['category'][comp_gdp['code'].isin(fedgovnondef_list)] = "Federal government - nondefense"
comp_gdp['category'][comp_gdp['code'].isin(sandlgov_list)] = "State and local government"


comp_gdp = comp_gdp[comp_gdp['date_t'] >= pd.datetime(2013, 4, 1).date()]

comp_gdp["id"] = comp_gdp["code"] + " - " + comp_gdp["category"] + " - " + comp_gdp["description"]

#comp_gdp.set_index(['id'], inplace=True)
test = comp_gdp.groupby('id').mean()

test.sort_values("abs_third_less_adv", inplace=True, ascending=False)

test['abs_third_revision'] = test['abs_third'] / test['abs_third_less_adv']

test.sort_values("abs_third_revision", inplace=True, ascending=False)

test.to_csv('data.csv')


test3 = test.append(test.sum(numeric_only=True), ignore_index=True)

test['Total'] = test.sum(axis=1)

test2 = test.reset_index()

new = {'code' }


