# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 19:22:17 2016

@author: WHawk
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 09:47:19 2016

@author: Swan
"""

#import a bunch of stuff
import pandas as pd
import urllib
#%matplotlib inline
import numpy as np  # (*) numpy for math functions and arrays


#Download all the data sets from Census
#Set Start year
start_year = 2013

#Set End year
end_year = 2016

#Do not edit
month = 1
year = start_year

#Create empty dataframe called house
house_raw = pd.DataFrame()

#outfilename = temp_file
#url_of_file = "http://www2.census.gov/retail/releases/historical/marts/rs1601.xls"
#urllib.request.urlretrieve(url_of_file, outfilename) 


#For each year, download the file, unzip the file, and delete the zip files
#Read in each Excel file.
#Create df house_raw for all years selected
while year <= end_year:
    abv_year = str(year)[-2:]
    while month <= 9:
        temp_url = "http://www2.census.gov/retail/releases/historical/marts/"
        temp_file =  "rs" + abv_year + "0" + str(month) + ".xls"
        temp_path = temp_url + temp_file       
        urllib.request.urlretrieve(temp_path, temp_file)
        tempbook = pd.read_excel(temp_file, sheetname=1, parse_cols=9)
        house_raw = house_raw.append(tempbook)
        month += 1
    while month <= 12:
        temp_url = "http://www2.census.gov/retail/releases/historical/marts/"
        temp_file =  "rs" + abv_year + str(month) + ".xls"
        temp_path = temp_url + temp_file       
        urllib.request.urlretrieve(temp_path, temp_file)
        tempbook = pd.read_excel(temp_file, sheetname=1, parse_cols=9)
        house_raw = house_raw.append(tempbook)
        month += 1
    year += 1      # equivalent to 'count = count + 1'
    month = 1



urllib.request.urlretrieve('http://www2.census.gov/retail/releases/historical/marts/rs1601.xls')
temp_file =  "rs1403.xls"
tempbook = pd.read_excel(temp_file, sheetname=1)



#Reset Year
year = start_year

#Create df house and preserve the raw file
house = house_raw

#To get housing completetions from 1999 to 2014
#Data contains houses completed in 2014 (because of 4 months data added to each file)
house = house_raw[(house_raw.COMP>199900) & (house_raw.COMP<201500)]

house.is_copy = False

#Create COMP_YEAR as an integer (monthly data)
house.loc[:,"COMP_YEAR"] = house["COMP"].astype(str).str[:4].astype(int)

#Create list of columns to recrate boolean
boolist = ["ACS", "AGER", "ASSOC", "CLOS", "CON", "DECK", "DET", "FNBS"]
mis = ["FINC", "STOR", "AREA", "BEDR", "COMP", "FNSQ", "SLPR", "SQFS"]
mis9 = ["FPLS", "FULB", "HAFB"]

#Recreate booleans
for col in boolist:
    house[col].replace({0:np.nan,1:True,2:False}, inplace=True)
    
for col in mis:
    house[col].replace({0:np.nan}, inplace=True)
    
for col in mis9:
    house[col].replace({9:np.nan}, inplace=True)
    
house.METRO.replace({1:True,2:False}, inplace=True)

my_vars = ["ACS", "AGER", "ASSOC", "CLOS", "CON", "DECK", "DET", "FNBS", "FINC", "STOR", "AREA", "BEDR", "COMP", "FNSQ", "SLPR", "SQFS", "FPLS", "FULB", "HAFB", "DIV", "METRO", "FFNSQ", "WEIGHT"]

house = house[my_vars]

#Create file with just 2004 onward for graphs
house04 = house[house.COMP>200400]

#Create file with just 2014 for graphs
house14 = house[(house.COMP>201400) & (house.COMP<201500)]
house14 = house14[['COMP_YEAR','DIV', 'METRO', 'SQFS', 'SLPR', 'ACS']]

#Take mean of each numeric by year
housemeans = house.groupby("COMP_YEAR").mean()
housemeans04 = house04.groupby("COMP_YEAR").mean()

#Create csv files for plotly
housemeans.to_csv('housemeans.csv')
housemeans04.to_csv('housemeans04.csv')
house14.to_csv('house14.csv')


  
house.describe()
house.to_csv('house.csv')
