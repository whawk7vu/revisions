# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 13:34:41 2016

@author: Swan
"""

#import a bunch of stuff
import pandas as pd
import requests
import datetime

# table with basic information https://research.stlouisfed.org/fred2/release/tables?rid=53&eid=13562

#percent_change_list
#GDP: A191RL1Q225SBEA
    #Goods: https://research.stlouisfed.org/fred2/series/A353RY2Q224SBEA
    #Services: https://research.stlouisfed.org/fred2/series/DSERRY2Q224SBEA
#Investment: https://research.stlouisfed.org/fred2/series/A006RY2Q224SBEA
    #Nonresidential: https://research.stlouisfed.org/fred2/series/A008RY2Q224SBEA
    #Residential: https://research.stlouisfed.org/fred2/series/A011RY2Q224SBEA
    #Inventories: https://research.stlouisfed.org/fred2/series/A014RY2Q224SBEA
#Net exports: https://research.stlouisfed.org/fred2/series/A019RY2Q224SBEA
    #Exports: https://research.stlouisfed.org/fred2/series/A020RY2Q224SBEA
        #Goods: https://research.stlouisfed.org/fred2/series/A253RY2Q224SBEA
        #Services: https://research.stlouisfed.org/fred2/series/A646RY2Q224SBEA
    #Imports: https://research.stlouisfed.org/fred2/series/A021RY2Q224SBEA
        #Goods: https://research.stlouisfed.org/fred2/series/A255RY2Q224SBEA
        #Services: https://research.stlouisfed.org/fred2/series/A656RY2Q224SBEA
#Government: https://research.stlouisfed.org/fred2/series/A822RY2Q224SBEA
    #Federal: https://research.stlouisfed.org/fred2/series/A823RY2Q224SBEA
        #Defense: https://research.stlouisfed.org/fred2/series/A824RY2Q224SBEA
        #Nondefense: https://research.stlouisfed.org/fred2/series/A825RY2Q224SBEA
    #State and local: https://research.stlouisfed.org/fred2/series/A829RY2Q224SBEA



with open('api.txt', 'r') as api:
    api=api.read()

percent_change_list = ["A353RY2Q224SBEA", "DSERRY2Q224SBEA", "A006RY2Q224SBEA", "A008RY2Q224SBEA",	"A011RY2Q224SBEA",	"A014RY2Q224SBEA",	"A019RY2Q224SBEA",	"A020RY2Q224SBEA",	"A253RY2Q224SBEA",	"A646RY2Q224SBEA",	"A021RY2Q224SBEA",	"A255RY2Q224SBEA",	"A656RY2Q224SBEA",	"A822RY2Q224SBEA",	"A823RY2Q224SBEA",	"A824RY2Q224SBEA",	"A825RY2Q224SBEA",	"A829RY2Q224SBEA"]
#series_list = ['GDPC1', 'PCECC96', 'GPDIC1', 'NETEXC', 'GCEC96']
series_id = 'A191RL1Q225SBEA'

r = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=' + series_id + '&realtime_start=1776-07-04&api_key=' + api + '&file_type=json')

series = r.json()

obs = series['observations']



for obj in obs:
    obj['new_date'] = datetime.datetime.strptime(obj['date'],'%Y-%m-%d').date()
    obj['start'] = datetime.datetime.strptime(obj['realtime_start'],'%Y-%m-%d').date()
    obj['end'] = datetime.datetime.strptime(obj['realtime_end'],'%Y-%m-%d').date()
    ###I think this should be the function, but I am having some trouble
    if obj['realtime_end'] == '9999-12-31':
        obj['current_est'] = obj['value']
    else:
        obj['current_est'] = 'NaN'
        
    if (obj['new_date'] + datetime.timedelta(days=91) < obj['start'] and
        obj['new_date'] + datetime.timedelta(days=121) > obj['start']):
            obj['label'] = 'Advanced'
    elif (obj['new_date'] + datetime.timedelta(days=121) < obj['start'] and
          obj['new_date'] + datetime.timedelta(days=152) > obj['start']):
              obj['label'] = 'Second'
    elif (obj['new_date'] + datetime.timedelta(days=152) < obj['start'] and
          obj['new_date'] + datetime.timedelta(days=182) > obj['start']):
              obj['label'] = 'Third'
    else: obj['label'] = 'NaN'
        


obs[-10:]


vals_by_date={}
series_change={}

#remove if value == '.'
#change data to int?
#remove if date < 2000-01-01

# read in observations
for item in series['observations']:
    # akr: make datetime objects, do date math to find difference
    # set label based on difference
    # item['label'] = 'advance'
    if not item['date'] in vals_by_date:
        vals_by_date[item['date']] = munge_item(item) # { item['label']: item['value'], item['label'] + '_realtime_start': item['realtiem_start']}
    else:
        vals_by_date[item['date']].merge/update(munge_item(item))


for date,value in vals_by_date.items():
    series_change[date] = round(abs(float(value[0])-float(value[-1])),2)
    #series_change[date] = float(value)

vals_by_date
series_change

series_change_data = pd.Series(series_change, name='DateValue')

series_change_data.index.name = 'Date'

series_change_data.reset_index()

vals_by_date
series_change_data
