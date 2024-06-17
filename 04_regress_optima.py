#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import copy

import numpy as np
import pandas as pd
import scipy

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

import statsmodels
import statsmodels.api as sm

## ===================================================================== ##

from parameters import *

## ===================================================================== ##

experiments = ['01a', '01b', '01c', '02', '01Y1', '01Y2']

for experiment in experiments:

	print(experiment)

	## ========================================================================

	df = pd.read_csv('./results/optimal_temperature_byunit_{0:s}.csv'.format(experiment))
	df = df.loc[df['t2m_optimal'].notnull(), :]
	df['weight'] = df.groupby('iso3')['t2m'].transform(lambda x: 1. / x.count())

	dfm = df.groupby('iso3')[['t2m_optimal', 't2m']].mean().reset_index()

	dft = pd.read_csv(os.path.join(DATAPATH, 'correlations_rainfall.csv'))
	negative_correlation = dft.loc[dft['corr'] < 0., 'Unnamed: 0'].unique()
	dfnr = df.loc[df['id'].isin(negative_correlation), :]

	formula = 't2m_optimal ~ t2m'
	res = sm.OLS.from_formula(formula=formula, data=df).fit(missing='drop').get_robustcov_results()
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	dx['rsq'] = res.rsquared_adj
	dx['rsq_adj'] = res.rsquared_adj
	dx['nobs'] = res.nobs
	dx.to_csv('./results/coeffs_stage2_byunit_{0:s}_main.csv'.format(experiment))

	formula = 't2m_optimal ~ t2m'
	res = sm.OLS.from_formula(formula=formula, data=dfnr).fit(missing='drop').get_robustcov_results()
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	dx['rsq'] = res.rsquared_adj
	dx['rsq_adj'] = res.rsquared_adj
	dx['nobs'] = res.nobs
	dx.to_csv('./results/coeffs_stage2_byunit_{0:s}_negcorr.csv'.format(experiment))

	formula = 't2m_optimal ~ t2m + log_gdp_pc_2011_2020 + tp'
	res = sm.OLS.from_formula(formula=formula, data=df).fit(missing='drop').get_robustcov_results()
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	dx['rsq'] = res.rsquared_adj
	dx['rsq_adj'] = res.rsquared_adj
	dx['nobs'] = res.nobs
	dx.to_csv('./results/coeffs_stage2_byunit_{0:s}_controls.csv'.format(experiment))

	formula = 't2m_optimal ~ t2m'
	res = sm.WLS.from_formula(formula=formula, data=df, weights=df['weight']).fit(missing='drop').get_robustcov_results()
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	dx['rsq'] = res.rsquared_adj
	dx['rsq_adj'] = res.rsquared_adj
	dx['nobs'] = res.nobs
	dx.to_csv('./results/coeffs_stage2_byunit_{0:s}_weighted.csv'.format(experiment))

	# within countries
	formula = 't2m_optimal ~ t2m + iso3'
	res = sm.OLS.from_formula(formula=formula, data=df).fit(missing='drop').get_robustcov_results()
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	dx['rsq'] = res.rsquared_adj
	dx['rsq_adj'] = res.rsquared_adj
	dx['nobs'] = res.nobs
	dx.to_csv('./results/coeffs_stage2_byunit_{0:s}_within.csv'.format(experiment))

	# between countries
	formula = 't2m_optimal ~ t2m'
	res = sm.OLS.from_formula(formula=formula, data=dfm).fit(missing='drop').get_robustcov_results()
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	dx['rsq'] = res.rsquared_adj
	dx['rsq_adj'] = res.rsquared_adj
	dx['nobs'] = res.nobs
	dx.to_csv('./results/coeffs_stage2_byunit_{0:s}_between.csv'.format(experiment))

## =============================================================================

## random (full acclimatisation)
print('Placebo test')

experiment = '01a'

df = pd.read_csv('./results/optimal_temperature_byunit_{0:s}.csv'.format(experiment))
df = df.loc[df['t2m_optimal'].notnull(), :]

units = df['id'].unique()
df = df.set_index('id')

## ======================

df_data = pd.read_csv(os.path.join(DATAPATH, 'data_demeaned.csv'))
df_data = df_data.loc[:, ['id', 't2m_mean']]

values_dict = {}
for unit in df_data['id'].unique():
	values_dict[unit] = df_data.loc[df_data['id'] == unit, 't2m_mean'].values

n_montecarlo = 1000
df_mc = pd.DataFrame(index=range(0, n_montecarlo, 1))
for i in range(0, n_montecarlo, 1):
	print(i)
	df['t2m_optimal'] = np.nan
	for c in units:
		df.loc[c, 't2m_optimal'] = np.random.choice(values_dict.get(c, [np.nan]))

	formula = 't2m_optimal ~ t2m'
	res = sm.OLS.from_formula(formula=formula, data=df).fit(missing='drop').get_robustcov_results()
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	df_mc.loc[i, 'coef'] = dx.loc['t2m', 'Coef.']

df_mc.to_csv('./results/coeffs_stage2_byunit_{0:s}_random.csv'.format(experiment))
