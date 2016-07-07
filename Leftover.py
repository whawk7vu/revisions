# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 16:25:17 2016

@author: WHawk
"""

#leftovercode





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