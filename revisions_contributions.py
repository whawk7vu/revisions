# -*- coding: utf-8 -*-
"""
Created on Thu May  5 09:23:34 2016

@author: Swan
"""

import pandas as pd
import datetime
import numpy as np


###
### Step 1.0 Create URLS dataframe 
###

#clean  up urls
urls = pd.read_csv('url.csv', index_col = 0)
urls.x = urls.x.str.upper()
urls.x = urls.x.str.replace('HTTP://WWW.BEA.GOV/HISTDATA/RELEASES/GDP_AND_PI/','')
urls.x = urls.x.str.replace('_','/')

#change to pandas dataframe
urls = pd.DataFrame(urls.x.str.split('/').tolist())

#rename columns
urls.columns = ['year', 'quarter', 'est', 'date', 'section', 'xls']

#Change date to datetime.date() object
urls['date_pub'] = urls['date'].apply(lambda x: datetime.datetime.strptime(x,'%B-%d-%Y').date())

#Change Estimate names
urls.est.replace({'PRELIMINARY': 'SECOND', 'FINAL': 'THIRD'}, regex=True, inplace=True)

#sort by date
urls.sort_values('date_pub', inplace=True)

#create date variable year_Q
urls['date'] = urls['year'] + '_' + urls['quarter']

#keep relevent columns
urls = urls[['date','est', 'date_pub']]

#keep only files after 2004_Q1
urls = urls[urls['date_pub'] >= pd.datetime(2004, 4, 1).date()]

urls.to_pickle('urls')


#get list for final data:
final_dates = list(set(urls['date'].values.tolist()))
final_dates.sort()


#output urls to csv

#urls.to_csv('urls.csv')

###
#2.0 Read in 164 excel files
###

x=0
hist_file_all = pd.DataFrame()
long_file = pd.DataFrame()
#Range should be 1 to 150. using 10 just to test.
for x in range(1, 150):
    #read in xls files
    xls_file = pd.ExcelFile('histData' + str(x) + '.xls')
    
    if '10502 Qtr' in xls_file.sheet_names:
        
        #Create current values spreadsheet
        if x == 1:
            #Get the actual data values by parsing each xls file
            hist_file_current = xls_file.parse(sheetname = '10502 Qtr', skiprows=7, header=None)
            
            #Change rows into column names
            hist_col = hist_file_current[:2].transpose()
            hist_col["period"] = hist_col[0].apply(str).str[:4] + '_Q' + hist_col[1].apply(str).str[:1]
            col_names = hist_col['period'].tolist()
            col_names[0] = 'line'
            col_names[1] = 'description'
            col_names[2] = 'code'
            #col_names[-1] = 'value'
            hist_file_current.columns = col_names
            
            #drop NAs
            hist_file_current.dropna(inplace=True)
            
            #add date_pub to the files
            #hist_file_current['date_pub'] = date_pub
            #test = hist_file[list(hist_file.columns[:2]) + list(hist_file.columns[:-2])].copy()
            
            hist_file_current = pd.melt(hist_file_current, id_vars=["line", "description", "code"], 
                              var_name="date", value_name="CURRENT")
            hist_file_current = hist_file_current[(hist_file_current.date >= '2004_Q1')][['code','date','CURRENT']]        

        
        #This section is simply to get the date_pub variable to match with date_pub from urls
        hist_date = xls_file.parse(sheetname = '10502 Qtr', header=None)
        my_list = hist_date[0].astype(str)
        matching = [s for s in my_list if "Data published" in s]
        matching = [matching.replace("Data published","") for matching in matching]
        #change date into datime.date() format
        date_pub = datetime.datetime.strptime(matching[0].strip(' '), '%B %d, %Y').date()
        
        #Get the actual data values by parsing each xls file
        hist_file = xls_file.parse(sheetname = '10502 Qtr', skiprows=7, header=None)
        
        #Change rows into column names
        hist_col = hist_file[:2].transpose()
        hist_col["period"] = hist_col[0].apply(str).str[:4] + '_Q' + hist_col[1].apply(str).str[:1]
        col_names = hist_col['period'].tolist()
        col_names[0] = 'line'
        col_names[1] = 'description'
        col_names[2] = 'code'
        col_names[-1] = 'value'
        hist_file.columns = col_names
        
        #drop NAs
        hist_file.dropna(inplace=True)
               
        #add date_pub to the files
        hist_file['date_pub'] = date_pub
        #test = hist_file[list(hist_file.columns[:2]) + list(hist_file.columns[:-2])].copy()
        
        # keep columns 1-3 and the last 2
        hist_file = hist_file.ix[:,[0,1,2,-1,-2]]
        #Save these files to show what I want:        
        #hist_file.to_csv('mock'+str(x)+'.csv')
        
        #create a large file with all the data together
        hist_file_all = pd.concat([hist_file_all, hist_file])
        
        #if reading in the most recent vintage, create a long_file with the current GDP codes
        if x==1:
            codes = hist_file['code']
            descrip = hist_file[['code','description']]
            line = hist_file[['line','code']]
            urls_all = urls
            for item in codes:
                urls_all['code'] = item
                long_file = pd.concat([long_file, urls_all])
                


hist_file_all.to_pickle('hist_file_all')
descrip.to_pickle('descrip')


#hist_file_all = pd.read_pickle('hist_file_all')
#descrip = pd.read_pickle('descrip')



#sort the file
hist_file_all.sort_values(by=['date_pub', 'line'], inplace=True)

#change two release dates so they match up
hist_file_all.ix[hist_file_all['date_pub']==pd.datetime(2007, 1, 31).date(), 'date_pub'] = pd.datetime(2007, 1, 27).date()
hist_file_all.ix[hist_file_all['date_pub']==pd.datetime(2007, 3, 29).date(), 'date_pub'] = pd.datetime(2007, 3, 30).date()


hist_file_all = pd.merge(hist_file_all, descrip, how='left', on='code')

hist_file_all["description_y"].fillna(hist_file_all["description_x"], inplace=True)
hist_file_all.drop('description_x', axis=1, inplace=True)
hist_file_all.rename(columns = {'description_y':'description'}, inplace = True)


hist_file_all.to_pickle('hist_file_all')

#create final_data
final_data_cur = pd.merge(long_file, hist_file_all, how='left', on=['date_pub', 'code'])

long_file_all = long_file.drop('code', axis=1)

long_file_all.drop_duplicates(inplace=True)

final_data_all = pd.merge(hist_file_all, long_file_all, how='left', on=['date_pub'])

final_data_cur.dropna(inplace=True)
final_data_all.dropna(inplace=True)


#final_data.to_pickle('final_GDP_cont')
#final_data.to_excel('final_GDP_cont.xlsx')

pivot = final_data_cur.pivot_table('value', ['line', 'code', 'description', 'date'], 'est')

pivot.reset_index(inplace=True)

pivot = pd.merge(pivot, hist_file_current, how='left', on=['code', 'date'])

pivot['abs_adv'] = abs(pivot['ADVANCE'])
pivot['abs_second'] = abs(pivot['SECOND'])
pivot['abs_third'] = abs(pivot['THIRD'])
pivot['abs_current'] = abs(pivot['CURRENT'])

pivot['second_less_adv'] = (pivot['SECOND'] - pivot['ADVANCE']).round(4)
pivot['third_less_adv'] = (pivot['THIRD'] - pivot['ADVANCE']).round(4)
pivot['current_less_adv'] = (pivot['CURRENT'] - pivot['ADVANCE']).round(4)
pivot['third_less_second'] = (pivot['THIRD'] - pivot['SECOND']).round(4)


pivot['abs_second_less_adv'] = abs(pivot['SECOND'] - pivot['ADVANCE']).round(4)
pivot['abs_third_less_adv'] = abs(pivot['THIRD'] - pivot['ADVANCE']).round(4)
pivot['abs_third_less_second'] = abs(pivot['THIRD'] - pivot['SECOND']).round(4)


#rolling_mean is deprecated and needs to be replaced with Series.rolling(min_periods=1,center=False,window=8).mean()
pivot['abs_two_year'] = pivot.groupby('code')['abs_third_less_adv'].apply(pd.rolling_mean, 8, min_periods=1).round(4)

pivot.sort_values(['date','line'],inplace=True)

pivot['abs_current'] = abs(pivot['CURRENT']).round(4)
pivot['abs_current_less_adv'] = abs(pivot['CURRENT'] - pivot['ADVANCE']).round(4)
pivot['abs_current_less_third'] = abs(pivot['CURRENT'] - pivot['THIRD']).round(4)


pivot['year'] = pivot['date'].str[:4]
pivot['month'] = pivot['date'].str[-1:]

pivot['month'][pivot['month']=='4'] = '10'
pivot['month'][pivot['month']=='3'] = '7'
pivot['month'][pivot['month']=='2'] = '4'

pivot['date_t'] = pd.to_datetime(pivot['year']+pivot['month'],format='%Y%m')


pivot.to_pickle('pivot')




#######


pivot_all = final_data_all.pivot_table('value', ['line', 'code', 'description', 'date'], 'est')

pivot_all.reset_index(inplace=True)

pivot_all = pd.merge(pivot_all, hist_file_current, how='left', on=['code', 'date'])

pivot_all['abs_adv'] = abs(pivot_all['ADVANCE'])
pivot_all['abs_second'] = abs(pivot_all['SECOND'])
pivot_all['abs_third'] = abs(pivot_all['THIRD'])
pivot_all['abs_current'] = abs(pivot_all['CURRENT'])

pivot_all['second_less_adv'] = (pivot_all['SECOND'] - pivot_all['ADVANCE']).round(4)
pivot_all['third_less_adv'] = (pivot_all['THIRD'] - pivot_all['ADVANCE']).round(4)
pivot_all['current_less_adv'] = (pivot_all['CURRENT'] - pivot_all['ADVANCE']).round(4)
pivot_all['third_less_second'] = (pivot_all['THIRD'] - pivot_all['SECOND']).round(4)


pivot_all['abs_second_less_adv'] = abs(pivot_all['SECOND'] - pivot_all['ADVANCE']).round(4)
pivot_all['abs_third_less_adv'] = abs(pivot_all['THIRD'] - pivot_all['ADVANCE']).round(4)
pivot_all['abs_third_less_second'] = abs(pivot_all['THIRD'] - pivot_all['SECOND']).round(4)


#rolling_mean is deprecated and needs to be replaced with Series.rolling(min_periods=1,center=False,window=8).mean()
pivot_all['abs_two_year'] = pivot_all.groupby('code')['abs_third_less_adv'].apply(pd.rolling_mean, 8, min_periods=1).round(4)

pivot_all.sort_values(['date','line'],inplace=True)

pivot_all['abs_current'] = abs(pivot_all['CURRENT']).round(4)
pivot_all['abs_current_less_adv'] = abs(pivot_all['CURRENT'] - pivot_all['ADVANCE']).round(4)
pivot_all['abs_current_less_third'] = abs(pivot_all['CURRENT'] - pivot_all['THIRD']).round(4)


pivot_all['year'] = pivot_all['date'].str[:4]
pivot_all['month'] = pivot_all['date'].str[-1:]

pivot_all['month'][pivot_all['month']=='4'] = '10'
pivot_all['month'][pivot_all['month']=='3'] = '7'
pivot_all['month'][pivot_all['month']=='2'] = '4'

pivot_all['date_t'] = pd.to_datetime(pivot_all['year']+pivot_all['month'],format='%Y%m')


pivot_all.to_pickle('pivot_all')

pivot_all = pd.read_pickle('pivot_all')

pivot = pd.read_pickle('pivot')

comp_gdp = pivot_all


#comp_gdp['code'][comp_gdp['code']=="A165RY2"] = "DMOTRY2"



line = comp_gdp[['line', 'code']].drop_duplicates(['line'], keep='last')


comp_gdp['description'][comp_gdp['code']=='A937RY2'] = "Information processing equipment - other"
comp_gdp['description'][comp_gdp['code']=='B018RY2'] = "Change in private inventories - Farm"
comp_gdp['description'][comp_gdp['code']=='A015RY2'] = "Change in private inventories - Nonfarm"

comp_gdp['description'][comp_gdp['code']=='A253RY2'] = "Exports - goods"
comp_gdp['description'][comp_gdp['code']=='A646RY2'] = "Exports - services"
comp_gdp['description'][comp_gdp['code']=='A255RY2'] = "Imports - goods"
comp_gdp['description'][comp_gdp['code']=='A656RY2'] = "Imports - services"

comp_gdp['description'][comp_gdp['code']=='A997RY2'] = "National defense - consumption expenditures"
comp_gdp['description'][comp_gdp['code']=='A788RY2'] = "National defense - gross investment"

comp_gdp['description'][comp_gdp['code']=='A542RY2'] = "Nondefense - consumption expenditures"
comp_gdp['description'][comp_gdp['code']=='A798RY2'] = "Nondefense - gross investment"

comp_gdp['description'][comp_gdp['code']=='A991RY2'] = "State and local - consumption expenditures"
comp_gdp['description'][comp_gdp['code']=='A799RY2'] = "State and local - gross investment"



#Current vintage - lowest level
gdp_list = ["A191RL1"]
durgoods_list = ["DMOTRY2", 	"DFDHRY2", 	"DREQRY2", 	"DODGRY2"]
durgoods_list.extend(["A165RY2", "A166RY2", "A167RY2"])
nondurgoods_list = ["DFXARY2", 	"DCLORY2", 	"DGOERY2", 	"DONGRY2"]
nondurgoods_list.extend(["A168RY2", "A169RY2", "A173RY2", "A172RY2"])
houseserv_list = ["DHUTRY2", 	"DHLCRY2", 	"DTRSRY2", 	"DRCARY2", 	"DFSARY2", 	"DIFSRY2", 	"DOTSRY2"]
houseserv_list.extend(["A174RY2", "A175RY2", "A176RY2", "A177RY2", "A494RY2", "A490RY2", "A178RY2"])
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
comp_gdp['bea_code'] = ""


#lowest Level
comp_gdp['category'][comp_gdp['code'].isin(durgoods_list)] = "Durable goods"
comp_gdp['bea_code'][comp_gdp['code'].isin(durgoods_list)] = "DDURRY2"
comp_gdp['category'][comp_gdp['code'].isin(nondurgoods_list)] = "Nondurable goods"
comp_gdp['bea_code'][comp_gdp['code'].isin(nondurgoods_list)] = "DNDGRY2"
comp_gdp['category'][comp_gdp['code'].isin(houseserv_list)] = "Household consumption for services"
comp_gdp['bea_code'][comp_gdp['code'].isin(houseserv_list)] = "DHCERY2"
comp_gdp['category'][comp_gdp['code'].isin(info_list)] = "Information processing equipment"
comp_gdp['bea_code'][comp_gdp['code'].isin(info_list)] = "Y034RY2"
comp_gdp['category'][comp_gdp['code'].isin(intprop_list)] = "Intellectual property products"
comp_gdp['bea_code'][comp_gdp['code'].isin(intprop_list)] = "Y001RY2"
comp_gdp['category'][comp_gdp['code'].isin(inventory_list)] = "Change in private inventories"
comp_gdp['bea_code'][comp_gdp['code'].isin(inventory_list)] = "A014RY2"
comp_gdp['category'][comp_gdp['code'].isin(export_list)] = "Exports"
comp_gdp['bea_code'][comp_gdp['code'].isin(export_list)] = "A020RY2"
comp_gdp['category'][comp_gdp['code'].isin(import_list)] = "Imports"
comp_gdp['bea_code'][comp_gdp['code'].isin(import_list)] = "A021RY2"
comp_gdp['category'][comp_gdp['code'].isin(fedgovdef_list)] = "Federal government - defense"
comp_gdp['bea_code'][comp_gdp['code'].isin(fedgovdef_list)] = "A824RY2"
comp_gdp['category'][comp_gdp['code'].isin(fedgovnondef_list)] = "Federal government - nondefense"
comp_gdp['bea_code'][comp_gdp['code'].isin(fedgovnondef_list)] = "A825RY2"
comp_gdp['category'][comp_gdp['code'].isin(sandlgov_list)] = "State and local government"
comp_gdp['bea_code'][comp_gdp['code'].isin(sandlgov_list)] = "A829RY2"

comp_list1 = durgoods_list + nondurgoods_list + houseserv_list + info_list + intprop_list + inventory_list + export_list + import_list + fedgovdef_list + fedgovnondef_list + sandlgov_list

cat1 = comp_gdp[comp_gdp['code'].isin(comp_list1)]
cat1 = cat1.groupby([cat1['category'], comp_gdp['bea_code'], comp_gdp['description'].str.strip(), cat1['date']]).sum().round(4)

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

comp_gdp['bea_code'] = ""
comp_gdp['bea_code'][comp_gdp['code'].isin(goods_list)] = "DGDSRY2"
comp_gdp['bea_code'][comp_gdp['code'].isin(serv_list)] = "DSERRY2"
comp_gdp['bea_code'][comp_gdp['code'].isin(equip_list)] = "Y033RY2"
comp_gdp['bea_code'][comp_gdp['code'].isin(netexport_list)] = "A019RY2"
comp_gdp['bea_code'][comp_gdp['code'].isin(fed_list)] = "A823RY2"

comp_list2 = goods_list + serv_list + equip_list + netexport_list + fed_list

cat2 = comp_gdp[comp_gdp['code'].isin(comp_list2)]
cat2 = cat2.groupby([cat2['category2'], comp_gdp['bea_code'], comp_gdp['description'].str.strip(), cat2['date']]).sum().round(4)

#next level
pce_list = goods_list + serv_list
nonres_list = struct_list + equip_list + intprop_list 
gov_list = fed_list + sandlgov_list

comp_gdp['category3'] = ""
comp_gdp['category3'][comp_gdp['code'].isin(pce_list)] = "Personal consumption expenditures"
comp_gdp['category3'][comp_gdp['code'].isin(nonres_list)] = "Nonresidential investment"
comp_gdp['category3'][comp_gdp['code'].isin(gov_list)] = "Government"

comp_gdp['bea_code'] = ""
comp_gdp['bea_code'][comp_gdp['code'].isin(pce_list)] = "DPCERY2"
comp_gdp['bea_code'][comp_gdp['code'].isin(nonres_list)] = "A008RY2"
comp_gdp['bea_code'][comp_gdp['code'].isin(gov_list)] = "A822RY2"

comp_list3 = pce_list + nonres_list + gov_list

cat3 = comp_gdp[comp_gdp['code'].isin(comp_list3)]
cat3 = cat3.groupby([cat3['category3'], comp_gdp['bea_code'], comp_gdp['description'].str.strip(), cat3['date']]).sum().round(4)

#next level
fixedinv_list = nonres_list + resinv_list

comp_gdp['category4'] = ""
comp_gdp['category4'][comp_gdp['code'].isin(fixedinv_list)] = "Fixed investment"

comp_gdp['bea_code'] = ""
comp_gdp['bea_code'][comp_gdp['code'].isin(fixedinv_list)] = "A007RY2"


comp_list4 = fixedinv_list

cat4 = comp_gdp[comp_gdp['code'].isin(comp_list4)]
cat4 = cat4.groupby([cat4['category4'], comp_gdp['bea_code'], comp_gdp['description'].str.strip(), cat4['date']]).sum().round(4)


#next level
inv_list = fixedinv_list + inventory_list

comp_gdp['category5'] = ""
comp_gdp['category5'][comp_gdp['code'].isin(inv_list)] = "Investment"

comp_gdp['bea_code'] = ""
comp_gdp['bea_code'][comp_gdp['code'].isin(inv_list)] = "A006RY2"

comp_list5 = inv_list

cat5 = comp_gdp[comp_gdp['code'].isin(comp_list5)]
cat5 = cat5.groupby([cat5['category5'], comp_gdp['bea_code'], comp_gdp['description'].str.strip(), cat5['date']]).sum().round(4)

#next level
gdp_list = pce_list + inv_list + netexport_list + gov_list

comp_gdp['category6'] = ""
comp_gdp['category6'][comp_gdp['code'].isin(gdp_list)] = "Gross domestic product"

comp_gdp['bea_code'] = ""
comp_gdp['bea_code'][comp_gdp['code'].isin(gdp_list)] = "A191RL1"

comp_list6 = gdp_list

cat6 = comp_gdp[comp_gdp['code'].isin(comp_list6)]
cat6 = cat6.groupby([cat6['category6'], comp_gdp['bea_code'], comp_gdp['description'].str.strip(), cat6['date']]).sum().round(4)


comp_gdp['category7'] = ""
comp_gdp['category7'][comp_gdp['code'].isin(gdp_list)] = comp_gdp['description'].str.strip() +' - '+ comp_gdp['code']

comp_gdp['bea_code'] = ""
comp_gdp['bea_code'][comp_gdp['code'].isin(gdp_list)] = comp_gdp['code']

comp_list7 = gdp_list

cat7 = comp_gdp[comp_gdp['code'].isin(comp_list7)]
cat7 = cat7.groupby([cat7['category7'], comp_gdp['bea_code'], comp_gdp['description'].str.strip(), cat7['date']]).sum().round(4)


frames = [cat1, cat2, cat3, cat4, cat5, cat6, cat7]

gdp_data = pd.concat(frames)

gdp_data = gdp_data.reset_index(level=[]).reset_index().sort_values(by=['category', 'date'])

gdp_data['abs_adv_simple'] = abs(gdp_data['ADVANCE'])
gdp_data['abs_second_simple'] = abs(gdp_data['SECOND'])
gdp_data['abs_third_simple'] = abs(gdp_data['THIRD'])
gdp_data['abs_third_less_adv_simple'] = abs(gdp_data['third_less_adv'])


gdp_data.to_pickle('gdp_data')

gdp_data = pd.read_pickle('gdp_data')

final_gdp_data = gdp_data[['bea_code', 'category', 'description', 'date', 'ADVANCE', 'THIRD', 'abs_third_simple', 'abs_third', 'third_less_adv', 'abs_third_less_adv_simple', 'abs_third_less_adv']]
#comp_gdp["id"] = comp_gdp["code"] + " - " + comp_gdp["category"] + " - " + comp_gdp["description"]

final_gdp_data = pd.merge(final_gdp_data, line, how = 'left', left_on = 'bea_code', right_on = 'code')


final_gdp_data.drop('code', axis=1, inplace=True)

final_gdp_data.sort_values(by=['date','line'], inplace=True)

final_gdp_data['year'] = final_gdp_data['date'].str[:4]
final_gdp_data['month'] = final_gdp_data['date'].str[-1:]

final_gdp_data['month'][final_gdp_data['month']=='4'] = '10'
final_gdp_data['month'][final_gdp_data['month']=='3'] = '7'
final_gdp_data['month'][final_gdp_data['month']=='2'] = '4'

final_gdp_data['date_t'] = pd.to_datetime(final_gdp_data['year']+final_gdp_data['month'],format='%Y%m')

final_gdp_data.to_pickle('final_gdp_data')



#test = np.unique(final_data_all[['code','description']][final_data_all['code'].isin(new)].values)
#test = pd.unique(final_data_all[['code','description']][final_data_all['code'].isin(new)].values.ravel())



         