#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import copy

import numpy as np
import pandas as pd

## ===================================================================== ##

from parameters import *

## ===================================================================== ##

# climatic mean temperature - use all observations
df_clim = pd.read_csv(os.path.join(DATAPATH, 'climatology_1981-2010.csv'))

df_quantiles = pd.read_csv(os.path.join(DATAPATH, 'unit2quantiles.csv'))
df_quantiles = df_quantiles.rename(columns={'t2m_mean': 't2m_optimal'})
df_quantiles['t2m_optimal'] = df_quantiles['t2m_optimal'] - 273.15

df_income = pd.read_csv(os.path.join(DATAPATH, 'countries_income.csv'))
df_income['log_gdp_pc_2011_2020'] = np.log(df_income['gdp_pc_2011_2020'])

## ===================================================================== ##

experiments = ['01a', '01b', '01c', '02', '01Y1', '01Y2']

for experiment in experiments:

	print(experiment)

	variable_optimal = 't2m_mean'

	## ===================================================================== ##
	## by unit

	if '01' in experiment:
		ifiles = [f for f in os.listdir('./results/') if ('predictions_byunit_{0:s}_'.format(experiment) in f)]
	elif '02' in experiment:
		ifiles = [f for f in os.listdir('./results/') if ('coeffs_byunit_{0:s}_'.format(experiment) in f)]

	units = [f.split('.csv')[0].split('_')[-1] for f in ifiles]

	df_results = pd.DataFrame(index=units, columns=['t2m_optimal', 'q1'], dtype=str)

	for i, ifile in enumerate(ifiles):

		unit = units[i]

		if '01' in experiment:

			## =====================================================
			## for model with splines

			df_pred = pd.read_csv('./results/' + ifile)
			indices = df_pred.index == df_pred['fit'].idxmax()
			df_results.loc[unit, 't2m_optimal'] = df_pred.loc[indices, variable_optimal].values[-1] - 273.15

		elif '02' in experiment:

			## =====================================================
			## for model with bins

			df_coeffs = pd.read_csv('./results/' + ifile)
			df_coeffs = df_coeffs.loc[df_coeffs.iloc[:, 0].str.contains('q1_'), :]

			if df_coeffs.shape[0] < 2:
				print('Not enough coeffs for unit: ', unit)
				continue
			df_coeffs['Estimate'] = df_coeffs['Estimate']
			idmax = df_coeffs['Estimate'].idxmax()
			qmax = df_coeffs.loc[idmax, 'Unnamed: 0']
			estimate = df_coeffs.loc[idmax, 'Estimate']
			if estimate < 0.:
				qmax = 'q1_6'

			df_results.loc[unit, 'q1'] = qmax

	## ===================================================================== ##

	df_results = df_results.reset_index().rename(columns={'index': 'id'})

	df_results = df_results.merge(df_clim, on='id', how='left')

	if '01' in experiment:
		df_results = df_results.merge(df_quantiles.groupby('id').first().drop(columns=['q1', 't2m_optimal']), on=['id'], how='left')
	elif '02' in experiment:
		df_results = df_results.drop(columns=['t2m_optimal']).merge(df_quantiles, on=['id', 'q1'], how='left')

	df_results = df_results.merge(df_income, on='iso3', how='left')

	indices = (df_results['iso2'] == 'US') & (df_results['id'].apply(lambda x: x[0] == 'F'))
	df_results.loc[indices, 'state'] = df_results.loc[indices, 'id'].apply(lambda x: 'S{0:02d}'.format(int(x[1:3])))

	df_results.to_csv('./results/optimal_temperature_byunit_{0:s}.csv'.format(experiment), index=False)
