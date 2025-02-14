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



main_table = pivot.drop(['line', 'year', 'month', 'date_t'], axis=1)

main_table = main_table[(main_table['date'] == main_table['date'].iloc[-1])]

main_table.to_csv('gdp_revisions.csv')
main_table.to_json('gdp_revisions.json')

main_table.to_html('main_table.html', classes = 'my_class" id = "gdp_main')

main_table_indexed = main_table.set_index(['code', 'description', 'date'])
main_table_indexed = main_table_indexed.stack()
main_table_indexed = main_table_indexed.reset_index()
main_table_indexed = main_table_indexed.rename(columns = {0:'value'})

main_table_indexed.to_csv('gdp_revisions.csv')

main_table.to_pickle('main_table')

#if I use line as an index then the codes don't combine, if I don't i get out of order
abs_revision_index = pivot.pivot_table('abs_two_year', ['code', 'description'], 'date')
abs_revision_t = abs_revision_index.reset_index()
abs_revision_t = pd.merge(line, abs_revision_t, how='left', on=['code'])

abs_revision_t.to_csv('Two_year_abs_revision.csv')

abs_revision_t.to_pickle('abs_revision_t')
abs_revision_index.to_pickle('abs_revision_index')





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
