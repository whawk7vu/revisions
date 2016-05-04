# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 13:34:41 2016

@author: Swan
"""
import pandas as pd
import requests
import datetime
import pandas_highcharts

writer = pd.ExcelWriter('output2.xlsx')

with open('api.txt', 'r') as api:
    api=api.read()

percent_change_list = ["A353RY2Q224SBEA", "DSERRY2Q224SBEA", "A006RY2Q224SBEA", "A008RY2Q224SBEA",	"A011RY2Q224SBEA",	"A014RY2Q224SBEA",	"A019RY2Q224SBEA",	"A020RY2Q224SBEA",	"A253RY2Q224SBEA",	"A646RY2Q224SBEA",	"A021RY2Q224SBEA",	"A255RY2Q224SBEA",	"A656RY2Q224SBEA",	"A822RY2Q224SBEA",	"A823RY2Q224SBEA",	"A824RY2Q224SBEA",	"A825RY2Q224SBEA",	"A829RY2Q224SBEA"]
nominal_GDP = ["A253RC1Q027SBEA", 	"A255RC1Q027SBEA", 	"A646RC1Q027SBEA", 	"B009RC1Q027SBEA", 	"B656RC1Q027SBEA", 	"CBI", 	"DGDSRC1Q027SBEA", 	"EXPGS", 	"FDEFX", 	"FGCE", 	"FNDEFX", 	"FPI", 	"GCE", 	"GDP", 	"GPDI", 	"IMPGS", 	"NETEXP", 	"PCDG", 	"PCEC", 	"PCESV", 	"PCND", 	"PNFI", 	"PRFI", 	"SLCE", 	"Y001RC1Q027SBEA", 	"Y033RC1Q027SBEA"]
indicator = ['GDP']

mylist = nominal_GDP

for element in mylist:

    r = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=' + element + '&realtime_start=1776-07-04&api_key=' + api + '&file_type=json')
    
    series = r.json()
    
    obs = series['observations']

    obs = [d for d in obs if d.get('value') != '.']
        
    for obj in obs:
        if obj['value'] == '.':
            print(obj)
        obj['new_date'] = datetime.datetime.strptime(obj['date'],'%Y-%m-%d').date()
        obj['start'] = datetime.datetime.strptime(obj['realtime_start'],'%Y-%m-%d').date()
        obj['end'] = datetime.datetime.strptime(obj['realtime_end'],'%Y-%m-%d').date()
        if obj['new_date'].month == 1:
            obj['date_label'] = str(obj['new_date'].year) + ' Q1'
        elif  obj['new_date'].month == 4:
            obj['date_label'] = str(obj['new_date'].year) + ' Q2'
        elif  obj['new_date'].month == 7:
            obj['date_label'] = str(obj['new_date'].year) + ' Q3'
        elif  obj['new_date'].month == 10:
            obj['date_label'] = str(obj['new_date'].year) + ' Q4'
        else:
            obj['date_label'] = 'NaN'
         
        ###I think this should be the function, but I am having some trouble        
        if (obj['new_date'] + datetime.timedelta(days=85) < obj['start'] and
            obj['new_date'] + datetime.timedelta(days=130) > obj['start']):
                obj['label'] = 'First'
        elif (obj['new_date'] + datetime.timedelta(days=130) < obj['start'] and
              obj['new_date'] + datetime.timedelta(days=152) > obj['start']):
                  obj['label'] = 'Second'
        elif (obj['new_date'] + datetime.timedelta(days=152) < obj['start'] and
              obj['new_date'] + datetime.timedelta(days=182) > obj['start']):
                  obj['label'] = 'Third'
        else: obj['label'] = 'NaN'
               
        
          
    vals_by_date={}
    series_change={}
    
    # read in observations
    for item in obs:        
        if not item['date_label'] in vals_by_date:
            vals_by_date[item['date_label']] = {item['label']:float(item['value'])}
        else:
            vals_by_date[item['date_label']].update({item['label']:float(item['value'])})
        if item['realtime_end'] == '9999-12-31':
            vals_by_date[item['date_label']].update({'current':float(item['value'])})
    
    r = pd.DataFrame.from_dict(vals_by_date, orient='index', dtype=None)
    cols=['First', 'Second', 'Third', 'NaN', 'current']
    r = r[cols]
    r['diff_1to3'] = r['Third'] - r['First']
    r['abs_diff_1to3'] = abs(r['First'] - r['Third'])
    r['one_year_avg'] = pd.rolling_mean(r['abs_diff_1to3'], window=4, min_periods=1)
    r['total_avg'] = r['abs_diff_1to3'].mean()
    
    r.to_excel(writer, element)
    

writer.save()


