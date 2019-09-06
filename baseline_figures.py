#Python3
"""
This is the main Python code to power the back end of the wolf_base FLASK app
All of the slicing and diceing of data, calculations and etc
"""

from math import pi
import datetime, calendar
import pandas as pd
import numpy

#bokeh imports
#from bokeh.io import output_file, show
from bokeh.palettes import Category10, Category20
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import Legend
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.core.properties import value

from bs4 import BeautifulSoup as BS

#GLOBAL VARS
Jurisdictions = ("BALTIMORE CITY", "BALTIMORE COUNTY", "PRINCE GEORGE'S COUNTY", "MONTGOMERY COUNTY")
#Jurisdictions = (['BALTIMORE CITY'])

Juris_short_hash = { "BALTIMORE CITY": "Balt City", 
					"BALTIMORE COUNTY": "Balt Co", 
					"PRINCE GEORGE'S COUNTY": "PG Co",
					"MONTGOMERY COUNTY": "Mont Co"}

Cat_short_hash = {"numcases": "Number of Cases", "race": "Race", "sex": "Sex", "init_outcome": "Commissioner Outcome", "top_disposition": "Top Charge Outcome", "age_at_issue": "Defendant Age", "num_charges": "Number of Charges", "length_case": "Length of Case (case issued)", "length_case_init": "Length of Case (init)", "top_charge": "Top 20 Charges", "zipcode": "Top 20 Zipcodes", "detention": "Detained - All Charges Dropped", "compare_district":"District Court", "compare_circuit": "Circuit Court"}

Source_short_hash = {"baseline": "Baseline", "allnp": "All Nolle Pross", "allnpheld": "All Nolle Pross Held", "circuit": "Circuit", "circuit_allnp": "Circuit All Nolle Pross", "compare": "Comparison"}

race_legend_hash = {"BLACK, AFRICAN AMERICAN": "African American", "WHITE, CAUCASIAN, ASIATIC INDIAN, ARAB": "White", "UNKNOWN, OTHER": "Unknown or other", "ASIAN, NATIVE HAWAIIAN, OTHER PACIFIC ISLANDER": "Asian", "AMERICAN INDIAN, ALASKA NATIVE": "Native American", "nan": "Null data", "BLACK": "African American", "WHITE": "White", "OTHER": "Other", "UNKNOWN":"Unknown", "INDIAN": "Native American", "Caucasian": "White", "African American/Black": "African American", "Hispanic": "Hispanic", "Other Asian": "Asian" }
sex_legend_hash = {"M": "Male", "F": "Female", "U": "Unknown/Not given", "nan": "Null data", "MALE": "Male", "FEMALE": "Female", "UNKNOWN": "Unknown/Not given"}
legend_hash_hash = {"race": race_legend_hash, "sex": sex_legend_hash}

sex_table_hash = {"M": "Male", "F": "Female", "U": "Unknown or not given", "nan": "Null data", "MALE": "Male", "FEMALE": "Female", "UNKNOWN": "Unknown/Not given"}
init_table_hash = {"ROR": "Release (ROR)", "HDOB": "Money Bail (HDOB)", "HWOB": "Detention (HWOB)", "TCMT": "Temporary Commitment (TCMT)", "nan": "Null data"}
table_hash_hash = {"init_outcome": init_table_hash, "sex": sex_table_hash}

pie_list = ("race", "sex", "init_outcome", "top_disposition") 

top20_list = ("top_charge", "zipcode")

timecategories = ("age_at_issue", "length_case", "length_case_init", "detention")

mobile_pie_height = 475
mobile_pie_width = 400
big_pie_height = 550
big_pie_width = 550

#Don't know why it can't recognize file folders

#MASTERDF = Baseline
masterdf = pd.read_csv('all_counties_baseline_merged_2013_2018.csv')
masterdf['issueddate'] = pd.to_datetime(masterdf['issueddate'])
masterdf['dob'] = pd.to_datetime(masterdf['dob'])
masterdf['top_dispo_date'] = pd.to_datetime(masterdf['top_dispo_date'])
masterdf['init_date'] = pd.to_datetime(masterdf['init_date'])
masterdf['init_outcome'] = masterdf['init_outcome'].str.strip()

#calculate_categories
masterdf['age_at_issue'] = masterdf.issueddate-masterdf.dob
masterdf['length_case'] = masterdf.top_dispo_date-masterdf.issueddate
masterdf['length_case_init'] = masterdf.top_dispo_date-masterdf.init_date
#This deletes some cases where there was data error entry
masterdf = masterdf[masterdf['length_case'] >= numpy.timedelta64(0,'D')]
masterdf = masterdf[masterdf['length_case_init'] >= numpy.timedelta64(0,'D')]

#ALLNPDF = Baseline narrowed to all NP'd cases
allnpdf = pd.read_csv('all_counties_all_np_merged_2013_2018.csv')
allnpdf['issueddate'] = pd.to_datetime(allnpdf['issueddate'])
allnpdf['dob'] = pd.to_datetime(allnpdf['dob'])
allnpdf['top_dispo_date'] = pd.to_datetime(allnpdf['top_dispo_date'])
allnpdf['init_date'] = pd.to_datetime(allnpdf['init_date'])
allnpdf['init_outcome'] = allnpdf['init_outcome'].str.strip()
#calculate_categories
allnpdf['age_at_issue'] = allnpdf.issueddate-allnpdf.dob
allnpdf['length_case'] = allnpdf.top_dispo_date-allnpdf.issueddate
allnpdf['length_case_init'] = allnpdf.top_dispo_date-allnpdf.init_date
#This deletes some cases where there was data error entry
allnpdf = allnpdf[allnpdf['length_case'] >= numpy.timedelta64(0,'D')]
allnpdf = allnpdf[allnpdf['length_case_init'] >= numpy.timedelta64(0,'D')]

#ALLNPHELDDF = Baseline narrowed to all NP'd cases where held before release
allnp_helddf = pd.read_csv('all_counties_held_np_merged_2013_2018.csv')
allnp_helddf['issueddate'] = pd.to_datetime(allnp_helddf['issueddate'])
allnp_helddf['dob'] = pd.to_datetime(allnp_helddf['dob'])
allnp_helddf['top_dispo_date'] = pd.to_datetime(allnp_helddf['top_dispo_date'])
allnp_helddf['init_date'] = pd.to_datetime(allnp_helddf['init_date'])
allnp_helddf['rels_date'] = pd.to_datetime(allnp_helddf['rels_date'])
allnp_helddf['init_outcome'] = allnp_helddf['init_outcome'].str.strip()
#calculate_categories
allnp_helddf['age_at_issue'] = allnp_helddf.issueddate-allnp_helddf.dob
allnp_helddf['length_case'] = allnp_helddf.top_dispo_date-allnp_helddf.issueddate
allnp_helddf['length_case_init'] = allnp_helddf.top_dispo_date-allnp_helddf.init_date
allnp_helddf['detention']= allnp_helddf.rels_date-allnp_helddf.init_date
#This deletes some cases where there was data error entry
allnp_helddf = allnp_helddf[allnp_helddf['length_case'] >= numpy.timedelta64(0,'D')]
allnp_helddf = allnp_helddf[allnp_helddf['length_case_init'] >= numpy.timedelta64(0,'D')]

#Circuit Baseline
circuitdf = pd.read_csv('circuit_merged_2013_2018.csv')

#Getting a warning cols 4,7,8 have mixed types - test
#WISHLIST figure it out

circuitdf['filingdate'] = pd.to_datetime(circuitdf['filingdate'])
circuitdf['dob'] = pd.to_datetime(circuitdf['dob'])
circuitdf['top_dispo_date'] = pd.to_datetime(circuitdf['top_dispo_date'])

#calculate_categories
circuitdf['age_at_issue'] = circuitdf.filingdate-circuitdf.dob
circuitdf['length_case'] = circuitdf.top_dispo_date-circuitdf.filingdate
#This deletes some cases where there was data error entry
circuitdf = circuitdf[circuitdf['length_case'] >= numpy.timedelta64(0,'D')]

#Circuit All NP
circuit_allnpdf = pd.read_csv('circuit_all_np_merged_2013_2018.csv')
circuit_allnpdf['filingdate'] = pd.to_datetime(circuit_allnpdf['filingdate'])
circuit_allnpdf['dob'] = pd.to_datetime(circuit_allnpdf['dob'])
circuit_allnpdf['top_dispo_date'] = pd.to_datetime(circuit_allnpdf['top_dispo_date'])

#calculate_categories
circuit_allnpdf['age_at_issue'] = circuit_allnpdf.filingdate-circuit_allnpdf.dob
circuit_allnpdf['length_case'] = circuit_allnpdf.top_dispo_date-circuit_allnpdf.filingdate
#This deletes some cases where there was data error entry
circuit_allnpdf = circuit_allnpdf[circuit_allnpdf['length_case'] >= numpy.timedelta64(0,'D')]




#GET THE TEMPLATE HTML
base_viz_template = open('baseline_viz_template.html').read()
			

#MAIN FUNCTIONS
def winnowBaseline_serveHTML(var_dict):

	begin_year = int(var_dict['begin_year'])
	end_year = int(var_dict['end_year'])

	source = var_dict['source'] #baseline, all_np, np_held

	#Will take care of this on front end, but for now
	if (end_year < begin_year):
		end_year = begin_year

	#Years
	begin = datetime.datetime(begin_year,1,1)
	end = datetime.datetime(end_year, 12, 31)

	#Here tweak which is the master
	yeardf = ""
	if (source=="baseline"):
		yeardf = masterdf[masterdf['issueddate']>=begin]
		yeardf = yeardf[yeardf['issueddate']<=end]
	elif (source == "allnp"): 
		yeardf = allnpdf[allnpdf['issueddate']>=begin]
		yeardf = yeardf[yeardf['issueddate']<=end]
	elif (source == "allnpheld"):
		yeardf = allnp_helddf[allnp_helddf['issueddate']>=begin]
		yeardf = yeardf[yeardf['issueddate']<=end]
	elif (source == "circuit"):
		yeardf = circuitdf[circuitdf['filingdate']>=begin]
		yeardf = yeardf[yeardf['filingdate']<=end]
	else:
		#put circuit all np here
		yeardf = circuit_allnpdf[circuit_allnpdf['filingdate']>=begin]
		yeardf = yeardf[yeardf['filingdate']<=end]
		


	#Jurisdictions
	juris_list = []
	if (var_dict["balt_city"]):
		juris_list.append("BALTIMORE CITY")
	if (var_dict["balt_county"]):
		juris_list.append("BALTIMORE COUNTY")
	if (var_dict["pg_county"]):
		juris_list.append("PRINCE GEORGE'S COUNTY")
	if (var_dict["mont_county"]):
			juris_list.append("MONTGOMERY COUNTY")

	#Again, will take care at front end, but for now
	if (len(juris_list)==0):
		juris_list.append("BALTIMORE CITY")


	#This is ugly, but I couldn't figure any other way to do it
	jurisdf = ""
	num_juris = len(juris_list)
	if (num_juris==1):
		jurisdf = yeardf[yeardf['jurisdiction']==juris_list[0]]
	elif (num_juris==2):
		jurisdf = yeardf[ (yeardf['jurisdiction']== juris_list[0]) | (yeardf['jurisdiction']== juris_list[1])]
	elif (num_juris==3)	:
		jurisdf = yeardf[ (yeardf['jurisdiction']== juris_list[0]) | (yeardf['jurisdiction']== juris_list[1]) | (yeardf['jurisdiction']== juris_list[2])]	
	else:
		#all jurisdictions, nothing to winnow 
		jurisdf = yeardf

	#Category
	category = var_dict['cat']

	data_table = ""
	chart_html = "none" #default
	if (category in pie_list):
		#This weirdness is for pie charts in Bokeh
		#However it can do double-duty for table creation so will use it
		#The angle is just irrelevant
		x= dict()
		#Need to group by AS TYPE to address the null data problem
		targetgroups = jurisdf.astype(str).groupby(category)

		print("Looking at jurisdf with length of ", len(jurisdf))
		trackTotal = 0
		for cat, group in targetgroups:
			group_total = len(group)
			x[cat] = group_total
			print("For",cat,"found a subtotal of", group_total)
			trackTotal += group_total
			print("The new trackTotal is", trackTotal)

		focus_data = pd.Series(x).reset_index(name='value').rename(columns={'index':'category'})
		focus_data = focus_data.sort_values('value', ascending=False)
		focus_data['angle'] = focus_data['value']/focus_data['value'].sum() * 2*pi
		focus_data['percent'] = focus_data['value']/(focus_data['value'].sum())*100

		data_table = makePieDataTable(focus_data, category)
		chart_html = custom_pie_chart (focus_data, category)

	elif (category=="numcases"):
		data_hash = makeNumCasesDataHash(source, yeardf, begin_year, end_year, juris_list)
		data_table = makeNumCasesDataTable(data_hash, begin_year, end_year, juris_list)
		chart_html = numbers_chart(data_hash, begin_year, end_year, juris_list)

	elif (category in top20_list):
		data_table = makeTopDataTable(jurisdf, category)

	else:
		#Follow mode - average, median, max, min
		data_table = makeGenericDataTable(jurisdf, category)
		
	#title construction before winnow?
	title_hash = makeTitle(begin_year, end_year, source, category, juris_list)
	full_html = render_template_from_pieces (data_table, chart_html, title_hash)

	#Temp just for test
	#with open('colin_random_test.html', 'w') as file:
	#	file.write(full_html)
	#Temp just for test

	return full_html


def winnowCompare_serveHTML(var_dict):

	#Model this off of main, just need to simplify 
	begin_year = int(var_dict['begin_year'])
	end_year = int(var_dict['end_year'])
	#Will take care of this on front end, but for now
	if (end_year < begin_year):
		end_year = begin_year
	#Years
	begin = datetime.datetime(begin_year,1,1)
	end = datetime.datetime(end_year, 12, 31)

	#Jurisdictions
	juris_list = []
	if (var_dict["balt_city"]):
		juris_list.append("BALTIMORE CITY")
	if (var_dict["balt_county"]):
		juris_list.append("BALTIMORE COUNTY")
	if (var_dict["pg_county"]):
		juris_list.append("PRINCE GEORGE'S COUNTY")
	if (var_dict["mont_county"]):
		juris_list.append("MONTGOMERY COUNTY")
	#Again, should take care at front end, but for now
	if (len(juris_list)==0):
		juris_list.append("BALTIMORE CITY")
	num_juris = len(juris_list)

	#Category
	category = var_dict['cat']

	data_table = ""
	chart_html = "none" #default

	if (category=="compare_district"):
		#COMPARE DISTRICT
		baseline_df= masterdf[masterdf['issueddate']>=begin]
		baseline_df = baseline_df[baseline_df['issueddate']<=end]
		allnp_df= allnpdf[allnpdf['issueddate']>=begin]
		allnp_df = allnp_df[allnp_df['issueddate']<=end]
		npheld_df= allnp_helddf[allnp_helddf['issueddate']>=begin]
		npheld_df = npheld_df[npheld_df['issueddate']<=end]

		#Winnow by jurisdiction. Note no winnowing if all 4 juris selected
		if (num_juris==1):
			baseline_df = baseline_df[baseline_df['jurisdiction']==juris_list[0]]
			allnp_df = allnp_df[allnp_df['jurisdiction']==juris_list[0]]
			npheld_df = npheld_df[npheld_df['jurisdiction']==juris_list[0]]
		elif (num_juris==2):
			baseline_df = baseline_df[ (baseline_df['jurisdiction']== juris_list[0]) | (baseline_df['jurisdiction']== juris_list[1])]
			allnp_df = allnp_df[ (allnp_df['jurisdiction']== juris_list[0]) | (allnp_df['jurisdiction']== juris_list[1])]
			npheld_df = npheld_df[ (npheld_df['jurisdiction']== juris_list[0]) | (npheld_df['jurisdiction']== juris_list[1])]
		elif (num_juris==3):
			baseline_df = baseline_df[ (baseline_df['jurisdiction']== juris_list[0]) | (baseline_df['jurisdiction']== juris_list[1]) | (baseline_df['jurisdiction']== juris_list[2])]
			allnp_df = allnp_df[ (allnp_df['jurisdiction']== juris_list[0]) | (allnp_df['jurisdiction']== juris_list[1]) | (allnp_df['jurisdiction']== juris_list[2])]
			npheld_df = npheld_df[ (npheld_df['jurisdiction']== juris_list[0]) | (npheld_df['jurisdiction']== juris_list[1]) | (npheld_df['jurisdiction']== juris_list[2])]	
		else:
			#Do nothing 
			pass

		#Finally the calculations
		base_num = len(baseline_df)
		allnp_num = len(allnp_df)
		npheld_num = len(npheld_df)
		allnp_pc = round((allnp_num/base_num*100), 2)
		npheld_pc_base = round((npheld_num/base_num*100), 2)
		npheld_pc_allnp = round((npheld_num/allnp_num*100), 2)
		data_table = createCompareTable(base_num, allnp_num, allnp_pc, npheld_num, npheld_pc_allnp, npheld_pc_base)
		

	else:
		# COMPARE CIRCUIT
		baseline_df= circuitdf[circuitdf['filingdate']>=begin]
		baseline_df = baseline_df[baseline_df['filingdate']<=end]
		allnp_df= circuit_allnpdf[circuit_allnpdf['filingdate']>=begin]
		allnp_df = allnp_df[allnp_df['filingdate']<=end]

		#Winnow by jurisdiction. Note no winnowing if all 4 juris selected
		if (num_juris==1):
			baseline_df = baseline_df[baseline_df['jurisdiction']==juris_list[0]]
			allnp_df = allnp_df[allnp_df['jurisdiction']==juris_list[0]]
		elif (num_juris==2):
			baseline_df = baseline_df[ (baseline_df['jurisdiction']== juris_list[0]) | (baseline_df['jurisdiction']== juris_list[1])]
			allnp_df = allnp_df[ (allnp_df['jurisdiction']== juris_list[0]) | (allnp_df['jurisdiction']== juris_list[1])]
		else:
			baseline_df = baseline_df[ (baseline_df['jurisdiction']== juris_list[0]) | (baseline_df['jurisdiction']== juris_list[1]) | (baseline_df['jurisdiction']== juris_list[2])]
			allnp_df = allnp_df[ (allnp_df['jurisdiction']== juris_list[0]) | (allnp_df['jurisdiction']== juris_list[1]) | (allnp_df['jurisdiction']== juris_list[2])]

		#Finally the calculations
		base_num = len(baseline_df)
		allnp_num = len(allnp_df)
		allnp_pc = round((allnp_num/base_num*100), 2)
		data_table = createCompareTable(base_num, allnp_num, allnp_pc)
		


	#title construction
	source = var_dict['source'] #baseline, all_np, np_held
	title_hash = makeTitle(begin_year, end_year, source, category, juris_list)
	full_html = render_template_from_pieces (data_table, chart_html, title_hash)

	return full_html

def createCompareTable(base_num, allnp_num, allnp_pc, npheld_num=None, npheld_pc_allnp=None, npheld_pc_base=None):

	tbl_str = "<table class='table table-bordered table-sm' id='data_table'><tbody>"
	tbl_str += "<tr><th>All Cases</th><td>"+str(base_num)+"</td></tr>"
	tbl_str += "<tr><th>All Charges Nolle Pross</th><td>"+str(allnp_num)+"</td></tr>"
	tbl_str += "<tr><th>Percent All Nolle Pross</th><td>"+str(allnp_pc)+"%</td></tr>"
	if (npheld_num):
		tbl_str += "<tr><th>Complete Detention Before All Nolle Pross</th><td>"+str(npheld_num)+"</td></tr>"
		tbl_str += "<tr><th>Percent All Nolle Pross Complete Detention</th><td>"+str(npheld_pc_allnp)+"%</td></tr>"
		tbl_str += "<tr><th>Percent All Cases Complete Detention</th><td>"+str(npheld_pc_base)+"%</td></tr>"
	tbl_str += "</tbody></table>"

	#Make Element
	temp_html = BS(tbl_str, 'html.parser')
	table_element = temp_html.table

	return table_element



def makeTopDataTable(jurisdf, category, top_num=20):
	
	denom = len(jurisdf)
	groupdf = jurisdf.groupby(category).size().reset_index(name="count").sort_values(['count'], ascending=False)
	
	tbl_str = "<table class='table table-bordered table-sm' id='data_table'><tbody>"
	tbl_str += "<tr><th>"+"</th><th>Num Cases</th><th>Percent of Total</th></tr>"

	total = 0
	for i in range(0,top_num):
		cat = groupdf[category].values[i]
		num = groupdf['count'].values[i]
		total += num
		percent = round(num/denom*100, 2)
		
		try:
			tbl_str += "<tr><td>"+cat+"</td><td>"+str(num)+"</td><td>"+str(percent)+"</td></tr>"
		except TypeError:
			tbl_str += "<tr><td>"+str(int(cat))+"</td><td>"+str(num)+"</td><td>"+str(percent)+"</td></tr>"

	remaining_num = groupdf['count'].sum()-total
	remaining_pc = round(remaining_num/denom*100,2)
	tbl_str += "<tr><td>Remaining "+str((len(groupdf)-top_num))+"</td><td>"+str(remaining_num)+"</td><td>"+ str(remaining_pc)+"</td></tr>"

	tbl_str += "</tbody><table>"

	#Make Element
	temp_html = BS(tbl_str, 'html.parser')
	table_element = temp_html.table

	return table_element


def makeGenericDataTable(df, category):
	#Make Table String
	tbl_str = "<table class='table table-bordered table-sm' id='data_table'><tbody>"
	
	colhash={}

	if (category in timecategories):
		colhash['mean'] = df[category].dt.days.mean()
		colhash['median'] = df[category].dt.days.median()
		colhash['min_val'] = df[category].dt.days.min()
		colhash['max_val'] = df[category].dt.days.max()
		tempdf = df[category].dt.days
		colhash['total'] = tempdf.sum()
	else:
		colhash['mean'] = round(df[category].mean(),2)
		colhash['median'] = df[category].median()
		colhash['min_val'] = df[category].min()
		colhash['max_val'] = df[category].max()
		colhash['total'] = df[category].sum()

	strhash={}
	numcases = len(df[category])
	strhash['num_cases'] = str(numcases)
	strhash['mean_str'] = str(colhash['mean'])
	strhash['median_str'] = str(colhash['median'])
	strhash['min_val_str'] = str(colhash['min_val'])
	strhash['max_val_str'] = str(colhash['max_val'])
	#strhash['total_str'] = str(colhash['total'])

	max_row = df.loc[df[category]==df[category].max(), ['casenumber']]
	max_casenumber = max_row['casenumber'].values[0]
	min_row = df.loc[df[category]==df[category].min(), ['casenumber']]
	min_casenumber = min_row['casenumber'].values[0]
	

	if (category in timecategories):
		for key in colhash:
			years = round(colhash[key]/365.25)
			years = int(colhash[key]//365.25)
			days = int(round(colhash[key] - round(years*365.25)))
			temp_str = str(days) +" days"
			if (years>0):
				temp_str = str(years)+ " y "+ temp_str
			temp_key = key+"_str"
			strhash[temp_key]= temp_str

	tbl_str +="<tr><th>Number of Cases</th><td>" + strhash['num_cases'] + "</td></tr>"
	if (category=="detention"):
		tbl_str +="<tr><th>Total Time Detained</th><td>" + strhash['total_str'] + "</td></tr>"	
	tbl_str +="<tr><th>Average</th><td>" + strhash['mean_str'] + "</td></tr>"
	tbl_str +="<tr><th>Median</th><td>" + strhash['median_str'] + "</td></tr>"
	tbl_str +="<tr><th>Max</th><td>" + strhash['max_val_str'] + "</td></tr>"
	tbl_str +="<tr><th>Max Casenumber</th><td>" + makeCasenumLinkStr(max_casenumber) + "</td></tr>"
	tbl_str +="<tr><th>Min</th><td>" + strhash['min_val_str'] + "</td></tr>"
	tbl_str +="<tr><th>Min Casenumber</th><td>" + makeCasenumLinkStr(min_casenumber) + "</td></tr>"
	tbl_str += "</tbody><table>"

	#Make Element
	temp_html = BS(tbl_str, 'html.parser')
	table_element = temp_html.table

	return table_element


def makeCasenumLinkStr(casenumber):

	#Right now, just use the premade
	#WISH_LIST - make a more private link
	tag_str=""
	try:
		tag_str ="<a href='http://colinstarger.website/Pages/basic_clue_echo.php?case="+casenumber+"'>"+casenumber+"</a>"
	except TypeError:
		tag_str ="<a href='http://colinstarger.website/Pages/basic_clue_echo.php?case="+str(casenumber)+"'>"+str(casenumber)+"</a>"
	return tag_str

def makePieDataTable(df, category):

	#Make Table String
	tbl_str = "<table class='table table-bordered table-sm' id='data_table'><tbody>"
	tbl_str += "<tr><th>" + Cat_short_hash[category] + "</th><th>Cases</th><th>Percent (%)</th></tr>"
	for index, row in df.iterrows():
		if (category in table_hash_hash):
			tbl_str += "<tr><td>" + table_hash_hash[category][row['category']] + "</td>"	
		else:
			tbl_str += "<tr><td>" + row['category'] + "</td>"	
		tbl_str += "<td>" + str(row['value']) + "</td>"
		tbl_str += "<td class='text-right'>" + str(round(row['percent'],3)) + "</td></tr>"
	
	tbl_str += "<tr><th class='text-left'>Total Cases</th><td>" + str(df['value'].sum()) + "</td><td class='text-right'>100</td></tr>"
	tbl_str += "</tbody><table>"

	#Make Element
	temp_html = BS(tbl_str, 'html.parser')
	table_element = temp_html.table

	return table_element


def custom_pie_chart(data, category, mobile=True, tolerance=.5):

	#Don't need to show categories with less than tolerance percent
	data = data[data['percent']>tolerance]


	#Make adjustment to legend categories
	if (category in legend_hash_hash):
		for i in data.index:
			#I think this line is dodgy, assigning values while iterating - CHANGE!
			data.at[i, 'category'] = legend_hash_hash[category][data.at[i, 'category']]

	palette = ""
	color_len = len(data['category'])
	if(color_len>10):
		palette = Category20
	elif(color_len>2):
		palette = Category10
	else:
		palette = {1: ['#1f77b4'], 2: ['#1f77b4', '#ff7f0e']}
	data['color'] = palette[color_len]

	plot_height = mobile_pie_height
	plot_width = mobile_pie_width

	#Adjust height by number of categories
	if (color_len>5):
		plot_height = round(plot_height * (1+ (color_len-5)/15))
	#Section it off

	if (not mobile):
		plot_height = big_pie_height
		plot_width = big_pie_width

	p = figure(plot_height=plot_height, plot_width=plot_width, toolbar_location=None,
           #tools="hover", tooltips="@category: @percent %", x_range=(-0.5, .5), y_range=(-1.7, 1))
	       tools="hover", tooltips=[("", "@category"), ("total", "@value"), ("%", "@percent")], x_range=(-0.5, .5), y_range=(-1.7, 1))

	p.wedge(x=0, y=0, radius=0.3,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='category', source=data)

	p.axis.axis_label=None
	p.axis.visible=False
	p.grid.grid_line_color = None

	p.legend.location = "bottom_left"
	
	#adjust legend font if there are too many categoris
	#if (len(data['category'])>5):
	#	p.legend.label_text_font_size = "8pt"


	#html = file_html(p, CDN, title)
	html = file_html(p, CDN)
	
	return html

def makeNumCasesDataHash(source, df, begin_year, end_year, juris_list):

	begin_category = 'issueddate'
	if (source == "circuit" or source=="circuit_allnp"): 
		begin_category = 'filingdate'
	datahash = {}
	grandTotal = 0
	for year in range (begin_year, end_year+1):
		temp_year = df[(df[begin_category] >= datetime.datetime(year, 1, 1)) & (df[begin_category] <= datetime.datetime(year, 12, 31))]
		temp = temp_year.groupby("jurisdiction")
		yearhash={}
		for juris, group in temp:
			if (juris in juris_list):
				num = len(group)
				yearhash[juris]= num
				grandTotal += num
		datahash[year]=yearhash
	datahash['grandTotal']= grandTotal
	return datahash

#def makeNumCasesDataTable(df, begin_year, end_year, juris_list):
def makeNumCasesDataTable(datahash, begin_year, end_year, juris_list):

	#Make Table String
	tbl_str = "<table class='table table-bordered table-sm' id='data_table'><tbody>"
	tbl_str += "<tr><th>Jurisdiction</th><th>Year</th><th>Total Cases</th><tr>"


	for year in range (begin_year, end_year+1):
		for juris in juris_list:
			tbl_str += "<tr><td>"+juris+"</td><td>"+str(year)+"</td><td>"
			num = datahash[year][juris]
			tbl_str+=str(num)+"</td></tr>"
	grandTotal=datahash['grandTotal']

	tbl_str+= "<tr><th>Grand Total</th><th></th><th>"+str(grandTotal)+"</th></tr>"
	tbl_str += "</tbody><table>"

	#Make Element
	temp_html = BS(tbl_str, 'html.parser')
	table_element = temp_html.table

	return table_element


def numbers_chart(datahash, begin_year, end_year, juris_list):

	bar_data = {}

	years=[]
	for year in range(begin_year, end_year+1):
		years.append(str(year))
	bar_data['years']= years

	for juris in juris_list:
		juris_totals=[]
		for year in range(begin_year, end_year+1):
			juris_totals.append(datahash[year][juris])
		bar_data[juris]=juris_totals

	palette = ""
	color_len = len(juris_list)
	if(color_len>10):
		palette = Category20
	elif(color_len>2):
		palette = Category10
	else:
		palette = {1: ['#1f77b4'], 2: ['#1f77b4', '#ff7f0e']}

	colors = palette[color_len]

	#WISH_LIST: Make plot_height mobile variant
	
	plot_height = 350
	plot_width = 375
	p = figure(x_range=years, plot_height=plot_height, plot_width = plot_width, toolbar_location=None, tools="hover", tooltips=[("","$name"), ("year", "@years"), ("total","@$name")])


	width = ((len(years)+2)/10)
	p.vbar_stack(juris_list, x='years', width=width, color=colors, source=bar_data,
             legend=[value(x) for x in juris_list])

	p.y_range.start = 0
	p.x_range.range_padding = 0.1
	p.xgrid.grid_line_color = None
	p.axis.minor_tick_line_color = None
	p.outline_line_color = None
	
	#p.legend.location = "top_right"
	p.legend.location = "bottom_left"
	p.legend.orientation = "vertical"
	#p.legend.background_fill_alpha = 0
	p.legend.background_fill_alpha = .75
	p.legend.background_fill_color = "white"

	html = file_html(p, CDN)
	
	return html



def render_template_from_pieces (data_table, chart_html, title_hash):

	#Copy global into local
	local_html = base_viz_template

	#Get Template and Initial Configure
	templ_soup = BS(local_html, 'html.parser')

	#Page Title
	templ_soup.find(id="page_title_top").append(title_hash['top'])
	templ_soup.find(id="page_title_bot_a").append(title_hash['bot_a'])
	templ_soup.find(id="page_title_bot_b").append(title_hash['bot_b'])

	#The data table
	(templ_soup.find(id="table_inner_div")).append(data_table)

	if (chart_html!="none"):
		#NBokeh Graphic
		bokeh_soup = BS(chart_html, 'html.parser')
		templ_soup.head.append(bokeh_soup.find("link"))
		for script in bokeh_soup.head.find_all("script"):
			templ_soup.head.append(script)
		target = templ_soup.find(id="bokeh_container")
		target.append(bokeh_soup.body.div)
		for script in bokeh_soup.body.find_all("script"):
			target.append(script)
	
	return (str(templ_soup))

def makeTitle(begin_year, end_year, source, cat, juris_list):

	top_str = Source_short_hash[source] + " " + Cat_short_hash[cat]+" Breakdown"

	bot_a_str = ""
	if (begin_year == end_year):
		bot_a_str += str(begin_year)
	else:
		bot_a_str += str(begin_year) +"-" + str(end_year)
	
	bot_b_str = ""

	comma = False
	for juris in juris_list:
		if (comma):
			bot_b_str +=", "
		bot_b_str += Juris_short_hash[juris]
		comma = True
	
	return {"top": top_str, "bot_a": bot_a_str, "bot_b": bot_b_str}


