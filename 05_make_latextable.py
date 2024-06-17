#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
from copy import deepcopy

import numpy as np
import pandas as pd

from scipy.stats import t 

## ===== define some functions ===== ##

def get_stars(p, mode=1):
	if mode == 0:
		if p < 0.001:
			return '$^{* * *}$'
		elif p < 0.01:
			return '$^{* *}$'
		elif p < 0.05:
			return '$^{*}$'
		else:
			return ''
	elif mode == 1:
		if p < 0.01:
			return '$^{* * *}$'
		elif p < 0.05:
			return '$^{* *}$'
		elif p < 0.1:
			return '$^{*}$'
		else:
			return ''

CONTROLS_GROUPS = {}
intercept_variables = ['Intercept']

var2name = {\
				't2m': 'Annual mean temperature',
				'log_gdp_pc_2011_2020': 'log GDP pc',
				'tp': 'Annual total precipitation',
				'Intercept': 'Intercept',
				'empty': ''
}

for controls_group in CONTROLS_GROUPS.keys():
	var2name[controls_group] = controls_group

def get_dataframe(df, index_col_est, index_col_se, index_col_p, model_name='Model X'):
	columns = df.columns
	df = df.iloc[:, [0, index_col_est, index_col_se, index_col_p]].rename(columns={'Unnamed: 0': 'Variable',
						columns[index_col_est]: 'Estimate', columns[index_col_se]: 'SE', columns[index_col_p]: 'P'})
	df_new = df.iloc[np.repeat(np.arange(len(df)), 2)].reset_index(drop=True)

	# remove variable label from every second column
	df_new.loc[np.arange(1, df_new.shape[0], 2), 'Variable'] = df_new.loc[np.arange(1, df_new.shape[0], 2), 'Variable'] + '_SE'

	# correct for number of figures to show
	df_new.loc[:, 'Estimate'] = df_new.apply(lambda x: '{0:5.4f}{1:s}'.format(x['Estimate'], get_stars(x['P'])), axis=1)
	df_new.loc[:, 'SE'] = df_new['SE'].apply(lambda x: '({0:5.4f})'.format(x))

	# copy in SE in every second row
	df_new.loc[np.arange(1, df_new.shape[0], 2), 'Estimate'] = df_new.loc[np.arange(1, df_new.shape[0], 2), 'SE']

	# rename column
	df_new = df_new.rename(columns={'Estimate': model_name})

	return df_new[['Variable', model_name]]

def sort_variables(df, var2name):
	df['var_sort'] = df['Variable']
	categories_estimates = list(var2name.keys())
	categories_SE = [c + '_SE' for c in categories_estimates]
	categories_all = [None]*(len(categories_estimates)+len(categories_SE))
	categories_all[::2] = categories_estimates
	categories_all[1::2] = categories_SE
	df['var_sort'] = pd.Categorical(
	    df['var_sort'], 
	    categories=categories_all, 
	    ordered=True
	)
	df = df.sort_values(by='var_sort', ignore_index=True)
	df = df.drop(columns=['var_sort'])
	return df


for TABLE_ID in ['01', '02']:

	REMOVE_BIN_INTERCEPTS = True

	###

	if TABLE_ID == '01':
		EXPERIMENTS = ['stage2_byunit_01a_main',
						'stage2_byunit_01a_between',
						'stage2_byunit_01a_within',
						'stage2_byunit_01a_weighted',
						'stage2_byunit_01a_controls',
						]
		COLUMN_NAMES = [str(i+1) for i in range(np.size(EXPERIMENTS))]
		INDEX_COL_EST = 1
		INDEX_COL_SE = 2
		INDEX_COL_P = 3

	elif TABLE_ID == '02':
		EXPERIMENTS = ['stage2_byunit_01a_main',
						'stage2_byunit_01b_main',
						'stage2_byunit_01c_main',
						'stage2_byunit_02_main',
						]
		COLUMN_NAMES = [str(i+1) for i in range(np.size(EXPERIMENTS))]
		INDEX_COL_EST = 1
		INDEX_COL_SE = 2
		INDEX_COL_P = 3

	else:
		continue

	df_all = pd.DataFrame(columns=['Variable'])

	for i, EXPERIMENT in enumerate(EXPERIMENTS):

		COLUMN_NAME = COLUMN_NAMES[i]

		# read in regression results as data frame
		datapath = './results/'
		ifile = 'coeffs_{0:s}.csv'.format(EXPERIMENT)
		df = pd.read_csv(os.path.join(datapath, ifile))

		# transform data frame to get all information in one column
		df_new = get_dataframe(df, index_col_est=INDEX_COL_EST, index_col_se=INDEX_COL_SE, index_col_p=INDEX_COL_P, model_name=COLUMN_NAME)

		# read in R2 and other statistics
		datapath = './results/'
		ifile = 'coeffs_{0:s}.csv'.format(EXPERIMENT)
		df = pd.read_csv(os.path.join(datapath, ifile))

		# add empty line
		df_new = pd.concat([df_new, pd.DataFrame({'Variable': 'empty'}, index=[0])], axis=0, ignore_index=True)
		df_new = pd.concat([df_new, pd.DataFrame({'Variable': 'R2', COLUMN_NAME: '{0:3.2f}'.format(df['rsq'].values[0])}, index=[0])], axis=0, ignore_index=True)
		df_new = pd.concat([df_new, pd.DataFrame({'Variable': 'N', COLUMN_NAME: '{0:3.0f}'.format(df['nobs'].values[0])}, index=[0])], axis=0, ignore_index=True)

		if REMOVE_BIN_INTERCEPTS == True:
			df_new = df_new.loc[~df_new['Variable'].isin(intercept_variables), :]
			df_new = df_new.loc[~df_new['Variable'].isin([c + '_SE' for c in intercept_variables]), :]

		# add column of this model to dataframe, merging on variables
		df_all = df_all.merge(df_new, on=['Variable'], how='outer')

	var2name_plus = deepcopy(var2name)
	variables = [variable for variable in df_all['Variable'].unique() if '_SE' not in variable]
	for variable in variables:
		if variable not in var2name.keys():
			var2name_plus[variable] = variable.replace('_', '.')

	var2name_plus_stats = {**var2name_plus,
							'R2': 'R2',
							'R2 (within)': 'R2 (within)',
							'R2 adj.': 'R2 adj.',
							'df': 'df',
							'N': 'N',}

	df_all = sort_variables(df_all, var2name_plus_stats)

	# replace variable names
	index_SE = (df_all['Variable'].str.contains('_SE'))
	df_all.loc[index_SE, 'Variable'] = ''
	df_all.loc[~index_SE, 'Variable'] = df_all.loc[~index_SE, 'Variable'].apply(lambda x: var2name_plus_stats[x])

	tablepath = './tables'
	tablefile = 'table_results_{0:s}.tex'.format(TABLE_ID)
	with pd.option_context("max_colwidth", 1000):
		df_all.to_latex(buf=os.path.join(tablepath, tablefile), index=False, encoding='utf-8', escape=False, column_format='l'+'r'*(df_all.shape[1]-1), na_rep='')

