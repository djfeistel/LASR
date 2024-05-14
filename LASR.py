#!/usr/bin/env python3

##########################################################
# Author: Dorian J. Feistel 
# personl email: djfeistel@gmail.com
# work email: OFX5@cdc.gov
# 
##########################################################

import requests
import sys
import yaml
import os
import pandas as pd
import argparse

def get_lineage_yml():
	r = requests.get('https://raw.githubusercontent.com/outbreak-info/outbreak.info/master/curated_reports_prep/lineages.yml')
	if r.status_code == 200:
		print(f"Dowloading lineages.yml", file=sys.stderr)
		with open('lineages.yml', 'w+') as wf:
			wf.write(r.text)
	sys.exit(0)

def create_color_dict(callout_lineage_color_file:str)->dict:
	'''
	takes in user defined callout group list with colors
	file must have a header and be two columns
	first column in the call out group or COG
	second column is the hex code, where each value starts with #

	returns a dictionary with the COG as key and HEX code as value
	if a key or a value is duplicated, the code with exit
	'''

	# check if the file exists
	if not os.path.isfile(callout_lineage_color_file):
		print(f"\n{callout_lineage_color_file} was not found\n", file=sys.stderr)
		sys.exit(1)

	# determine the format of the file, exit if not correct format
	file_format = {'.csv': ',', '.tsv': '\t'}
	ext = os.path.splitext(callout_lineage_color_file)[1]
	if ext not in file_format:
		print(f"\n'{callout_lineage_color_file}' needs the extention '.csv' or '.tsv'\nExiting\n", file=sys.stderr)
		sys.exit(1)

	# create df of two column file
	df = pd.read_csv(callout_lineage_color_file, sep=file_format[ext], header=None)
	
	if "Other" not in df.iloc[:, 0].values:
		# Append a new row with "Other" and "#000000"
		new_row = pd.DataFrame([["Other", "#000000"]], columns=df.columns)
		df = pd.concat([df, new_row], ignore_index=True)
		
	dup_pass, list_index = check_for_duplicates(df)
	
	if dup_pass:
		print(f"Duplicates found in callout group collor list", file=sys.stderr)
		print(df.loc[list_index])
		sys.exit(0)

	return df.set_index(df.columns[0])[df.columns[1]].to_dict()

def check_for_duplicates(df:pd.DataFrame):

	callout_dups = df.iloc[:, 0].duplicated(keep='first')
	true_indices_callout_dups = callout_dups[callout_dups].index
	hex_dups = df.iloc[:, 1].duplicated(keep=False)
	true_indices_hex_dups = hex_dups[hex_dups].index

	index_combined = list(true_indices_callout_dups) + list(true_indices_hex_dups)

	if len(index_combined) > 0:
		return True, index_combined
	else:
		return False, None
	
def load_lineage_yml_file(yml_file:str)->dict:
	'''
	open lineages.yml file and return a pandas df with lineage 'name' as index
	'''
	# check if file exists
	if not os.path.isfile(yml_file):
		print(f"\n{yml_file} was not found\n", file=sys.stderr)
		sys.exit(1)
	
	# open lineages.yml file and convert to pandas df
	with open(yml_file, 'r') as file:
		yaml_data = yaml.safe_load(file)
		
	return pd.DataFrame(yaml_data).set_index('name')

def CalloutRecursion(df: pd.DataFrame, callout_color_dict: dict, lineage: str) -> str:
	'''
	fucntion is used to map through every lineage (name) in the lineage.yml file
		and determine its most recent common ancestor wrt the callout groups
	callout groups are user defined (specifically the callout_lineage_color_file)
		and can be any known lineage in the lineage.yml file.
	a callout group lineage in the 'callout_lineage_color_file' that is not found
		in the lineage.yml file will not be detected so correctly spelling and choice 
		of a lineage must be taking with precausion
	'''
	## check to see if current lineage is in COG
	if lineage in callout_color_dict:
		return lineage

	## if lineage isnt a COG
	## get its parent or recombinant_parent
	parent = df.at[lineage, 'parent']
	recombinant_parents = df.at[lineage, 'recombinant_parents']

	## if the parent is a COG return parent 
	if parent in callout_color_dict:
		return parent
	## lineages with recombinat_parents do not have a single parent in teh lineage.yml file
	## so if this varible is true, then the lineage is considered a recombinant
	elif not pd.isna(recombinant_parents):
		return "Other" #"Recombinant"
	
	## used for the first lineage (i.e., A) as it is technically the LUCA
	elif pd.isna(parent) and pd.isna(recombinant_parents):
		return "Other"

	## if none of these work, rerun function with parent
	## keep doing this until a match from one of the above is found
	else:
		return CalloutRecursion(df=df, callout_color_dict=callout_color_dict, lineage=parent)

def opts():
	parser = argparse.ArgumentParser(description='LASR: Lineage Aggregation for SARS-CoV-2 using Recursion', epilog="")
	parser.add_argument('-c', '--cog', metavar='file', type=str, help='Callout-group (COG) file. Two column file with lineage and hex color (TSV or CSV format, no header)')
	parser.add_argument('-l', '--lineage', metavar='file', type=str, help='lineage.yml file')
	parser.add_argument('-o', '--output', metavar='file', default="COG", type=str, help='Name of output file (without extention)')
	parser.add_argument('-e', '--extension', default='t', choices=['t', 'c'], type=str, help='File extension for output: "t" for TSV, "c" for CSV [default=t]')
	parser.add_argument('-f', '--full', action='store_true', help='Write detailed output file (includes additional information for each named lineage)')
	parser.add_argument('-d', '--download', action='store_true', help='Download lineage.yml from from outbreak.info github')
	args = parser.parse_args()
	return args

def main():

	args = opts()
	if args.download:
		get_lineage_yml()

	cog_file = args.cog
	lineage_file = args.lineage
	output_file = args.output
	output_delimiter = {'t': '\t', 'c': ','}[args.extension]
	output_extention = {'t': '.tsv', 'c': '.csv'}[args.extension]

	callout_color_dict = create_color_dict(cog_file)
	df = load_lineage_yml_file(lineage_file)

	lineage_calloutgroup_assignment_dict = {
		'name': [],
		'cog': [],
		'hex': []
	}

	## loop through all lineages from the lineage.yml file
	## run each lineage through 'CalloutRecursion' function
 
	for lineage in df.index:
		calloutgroup = CalloutRecursion(df=df, callout_color_dict=callout_color_dict, lineage=lineage)

		hex = callout_color_dict[calloutgroup]
		lineage_calloutgroup_assignment_dict['name'].append(lineage)
		lineage_calloutgroup_assignment_dict['cog'].append(calloutgroup)
		lineage_calloutgroup_assignment_dict['hex'].append(hex)

	## make dictionary into pandas data frame
	df_callout_color = pd.DataFrame(lineage_calloutgroup_assignment_dict).set_index('name')

	## merge lineagel.yaml data frame with callout colors data frame on index (i.e., 'name' which is the lineage)
	df_merge = pd.merge(df, df_callout_color, left_index=True, right_index=True)
	
	## list or reorder the columns of the merge data frame
	new_order = [
		'cog',
		'hex',
		'parent',
		'recombinant_parents',
		'alias',
		'children',
	]

	## reorder
	df_merge = df_merge[new_order]
	## fill empty cells with NA
	df_merge.fillna('NA', inplace=True)
	## sort values by name for easy manual viewing
	df_merge.sort_values(by='name', inplace=True)
	## replace lists in children column to string seperated by comma
	df_merge['children'] = df['children'].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)
	## save data to output.tsv file
	if args.full:
		df_merge.to_csv(''.join([output_file, output_extention]), sep=output_delimiter)
	else:
		df_merge = df_merge[['cog', 'hex']]
		df_merge.to_csv(''.join([output_file, output_extention]), sep=output_delimiter)


if __name__ == "__main__":
	main()