#Python3
"""
MAIN FLASK APP FILE
"""
from baseline_figures import *

from flask import Flask, request
app = Flask(__name__)

home_str = open("baseline_viz_manager.html").read()
generic_home_str = open("generic_viz_manager.html").read()

@app.route('/')
def home():
    return home_str

@app.route('/baseline')
def baseline():
	new_home_str = generic_home_str.format("District Baseline", "District Court", "baseline District Court", "baseline")
	return new_home_str

@app.route('/allnp')
def allnp():
	new_home_str = generic_home_str.format("District Nolle Pross", "District Nolle Pross", "District Court - all charges nolle prossed (dropped) -", "allnp")
	return new_home_str

@app.route('/allnpheld')
def allnpheld():
	new_home_str = generic_home_str.format("District NP Held", "District Nolle Pross Detention", "District Court - all charges nolle prossed (dropped) and detained pretrial-", "allnpheld")

	find_str = "<option class = \"d-none\" value=\"detention\">"
	replace_str = "<option value=\"detention\">"
	new_home_str = new_home_str.replace(find_str, replace_str)
	return new_home_str

@app.route('/circuit')
def circuit():
	new_home_str = generic_home_str.format("Circuit Baseline", "Circuit Court", "baseline Circuit Court", "circuit")

	#Hide init
	find_str = "value=\"length_case_init\""
	replace_str = "class='d-none' value='length_case_init'"
	new_home_str = new_home_str.replace(find_str, replace_str)
	
	find_str = "value=\"init_outcome\""
	replace_str = "class='d-none' value='init_outcome'"
	new_home_str = new_home_str.replace(find_str, replace_str)

	return new_home_str

@app.route('/circuitnp')
def circuitnp():
	new_home_str = generic_home_str.format("Circuit Nolle Pross", "Circuit Nolle Pross", "Circuit Court - all charges nolle prossed (dropped) -", "circuit_allnp")

	#Hide init
	find_str = "value=\"length_case_init\""
	replace_str = "class='d-none' value='length_case_init'"
	new_home_str = new_home_str.replace(find_str, replace_str)
	
	find_str = "value=\"init_outcome\""
	replace_str = "class='d-none' value='init_outcome'"
	new_home_str = new_home_str.replace(find_str, replace_str)

	return new_home_str

@app.route('/compare')
def compare():
	new_home_str = generic_home_str.format("Comparsion", "Comparison", "comparison", "compare")


	#Erase Number of cases
	find_str = "<option value=\"numcases\">Number of Cases</option>"
	replace_str = ""
	new_home_str = new_home_str.replace(find_str, replace_str)

	#Hide everything else
	find_str = "<option value=\""
	replace_str = "<option class='d-none' value=\""
	new_home_str = new_home_str.replace(find_str, replace_str)

	#Show Compare
	find_str = "<option class = \"d-none\" value=\"compare_"
	replace_str = "<option value=\"compare_"
	new_home_str = new_home_str.replace(find_str, replace_str)
	
	return new_home_str


@app.route('/data', methods=['GET', 'POST'])
def vizform():
	if request.method == 'GET':
		source = request.args.get('source')
		begin_year = request.args.get('begin_year')
		end_year = request.args.get('end_year')
		balt_city = not (request.args.get('balt_city') is None)
		balt_county = not (request.args.get('balt_county') is None)
		pg_county = not (request.args.get('pg_county') is None)
		mont_county = not (request.args.get('mont_county') is None)
		cat = request.args.get('cat')

		var_dict = {'source':source, 'begin_year': begin_year, 'end_year': end_year, 'balt_city': balt_city, 'balt_county':balt_county, 'pg_county':pg_county, 'mont_county': mont_county, 'cat': cat}

		if ((cat=="compare_district") or (cat=="compare_circuit")):
			return winnowCompare_serveHTML(var_dict)
		else:
			return winnowBaseline_serveHTML(var_dict)
