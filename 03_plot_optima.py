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

def linear_fit_predictions(dataframe, variable_y, variables_x):
	formula = '{0:s} ~ {1:s}'.format(variable_y, ' + '.join(variables_x))
	res = sm.OLS.from_formula(formula=formula, data=dataframe).fit(missing='drop').get_robustcov_results()
	pred = res.get_prediction(dataframe).summary_frame(alpha=0.05)
	pred.loc[:, variables_x] = dataframe.loc[:, variables_x].values
	dx = res.summary2(float_format="%.5f").tables[1].iloc[:, [0, 1, 3]]
	return pred, dx

## ===================================================================== ##

experiments = ['01a']

coeffs = {}

for experiment in experiments:

	df_optimal = pd.read_csv('./results/optimal_temperature_byunit_{0:s}.csv'.format(experiment))
	df_optimal = df_optimal.loc[df_optimal['t2m_optimal'].notnull(), :]
	df_optimal = df_optimal.sort_values(by=['t2m'], ascending=True)
	df_optimal = df_optimal.set_index('id')
	df_optimal = df_optimal.loc[df_optimal['iso3'].notnull(), :]

	## ==================================================================

	fig, ax = plt.subplots(figsize=(5,4))
	xall = df_optimal['t2m'].values
	yall = df_optimal['t2m_optimal'].values
	## ======
	pred, dx = linear_fit_predictions(df_optimal, 't2m_optimal', ['t2m'])
	ax.plot(pred['t2m'], pred['mean'], '-', color='grey', label='{0:3.2f} + {1:3.2f} x'.format(\
		dx.loc['Intercept', 'Coef.'], dx.loc['t2m', 'Coef.']), lw=2.)
	ax.fill_between(pred['t2m'], pred['mean_ci_lower'], pred['mean_ci_upper'], color='grey', alpha=0.3)
	## ======
	df_optimal['t2m_sq'] = df_optimal['t2m'] ** 2.
	pred, dx = linear_fit_predictions(df_optimal, 't2m_optimal', ['t2m', 't2m_sq'])

	ax.plot(pred['t2m'], pred['mean'], color='black', linestyle=':')

	for i, state in enumerate(df_optimal.index.values):
		x = df_optimal.loc[state, 't2m']
		y = df_optimal.loc[state, 't2m_optimal']
		ax.plot(x, y, 'o', markersize=1, markeredgecolor='none', markerfacecolor='k', alpha=0.7)
	ax.set_xlabel('Annual mean temperature (degree Celsius)')
	ax.set_ylabel('Preferred daily temperature (degree Celsius)')
	ax.legend(loc='upper left', title='', alignment='left')
	sns.despine(ax=ax, offset=1., right=True, top=True)
	fig.savefig('./figures/scatter_optimal_byunit_{0:s}.pdf'.format(experiment), bbox_inches='tight', transparent=True)

	pred, dx = linear_fit_predictions(df_optimal.loc[df_optimal['t2m'].between(df_optimal['t2m'].quantile(0.05), df_optimal['t2m'].quantile(0.95)), :], 't2m_optimal', ['t2m'])
	ax.plot(pred['t2m'], pred['mean'], 'm--', label='{0:3.2f} + {1:3.2f} x (excluding bottom 5% and top 5%)'.format(\
		dx.loc['Intercept', 'Coef.'], dx.loc['t2m', 'Coef.']), lw=3.)
	ax.legend(loc='upper left', title='', alignment='left')
	ax.set_ylim(ax.get_ylim() * np.array([1., 1.2]))
	fig.savefig('./figures/scatter_optimal_byunit_{0:s}_robustness.pdf'.format(experiment), bbox_inches='tight', transparent=True)

	## ====================================================================================================================================

	dfm = df_optimal.reset_index().groupby('iso3')[['t2m', 't2m_optimal', 't2m_sq']].mean()
	dfm = dfm.sort_values(by='t2m', ascending=True)

	## ==================================================================

	fig, ax = plt.subplots(figsize=(5,4))
	xall = dfm['t2m'].values
	yall = dfm['t2m_optimal'].values
	## ======
	pred, dx = linear_fit_predictions(dfm, 't2m_optimal', ['t2m'])
	ax.plot(pred['t2m'], pred['mean'], 'r-', label='{0:3.2f} + {1:3.2f} x'.format(\
		dx.loc['Intercept', 'Coef.'], dx.loc['t2m', 'Coef.']), lw=2.)
	ax.fill_between(pred['t2m'], pred['mean_ci_lower'], pred['mean_ci_upper'], color='r', alpha=0.3)
	## ======
	dfm['t2m_sq'] = dfm['t2m'] ** 2.
	pred, dx = linear_fit_predictions(dfm, 't2m_optimal', ['t2m', 't2m_sq'])
	ax.plot(pred['t2m'], pred['mean'], color='black', linestyle=':')

	for i, unit in enumerate(dfm.index.values):
		x = dfm.loc[unit, 't2m']
		y = dfm.loc[unit, 't2m_optimal']
		ax.plot(x, y, 'o', markersize=1, markeredgecolor='none', markerfacecolor='none', alpha=0.7)
		ax.annotate(text=unit, xy=(x, y), xycoords='data', va='center', ha='center', color='k', size='xx-small')
	ax.set_xlabel('Annual mean temperature (degree Celsius)')
	ax.set_ylabel('Preferred daily temperature (degree Celsius)')
	ax.legend(loc='upper left', title='', alignment='left')
	sns.despine(ax=ax, offset=1., right=True, top=True)
	fig.savefig('./figures/scatter_optimal_byunit_{0:s}_between.pdf'.format(experiment), bbox_inches='tight', transparent=True)

	## ====================================================================================================================================

	dfm = df_optimal.reset_index().groupby('iso3')[['t2m', 't2m_optimal', 't2m_sq']].transform(lambda x: x - x.mean())
	dfm.index = df_optimal['iso3'].values
	dfm = dfm.sort_values(by='t2m', ascending=True, ignore_index=True)

	## ==================================================================

	fig, ax = plt.subplots(figsize=(5,4))
	xall = dfm['t2m'].values
	yall = dfm['t2m_optimal'].values
	## ======
	pred, dx = linear_fit_predictions(dfm, 't2m_optimal', ['t2m'])
	ax.plot(pred['t2m'], pred['mean'], 'b-', label='{0:3.2f} + {1:3.2f} x'.format(\
		dx.loc['Intercept', 'Coef.'], dx.loc['t2m', 'Coef.']), lw=2.)
	ax.fill_between(pred['t2m'], pred['mean_ci_lower'], pred['mean_ci_upper'], color='b', alpha=0.3)
	#ax.plot(pred['t2m'], pred['mean'], color='black', linestyle=':')

	for i, unit in enumerate(dfm.index.values):
		x = dfm.loc[unit, 't2m']
		y = dfm.loc[unit, 't2m_optimal']
		ax.plot(x, y, 'o', markersize=1, markeredgecolor='none', markerfacecolor='k', alpha=0.7)
	ax.set_xlabel('Annual mean temperature (degree Celsius)\n deviation from country mean')
	ax.set_ylabel('Preferred daily temperature (degree Celsius)\n deviation from country mean')
	ax.legend(loc='upper left', title='', alignment='left')
	sns.despine(ax=ax, offset=1., right=True, top=True)
	fig.savefig('./figures/scatter_optimal_byunit_{0:s}_within.pdf'.format(experiment), bbox_inches='tight', transparent=True)

	pred, dx = linear_fit_predictions(dfm.loc[dfm['t2m'].between(dfm['t2m'].quantile(0.05), dfm['t2m'].quantile(0.95)), :], 't2m_optimal', ['t2m'])
	ax.plot(pred['t2m'], pred['mean'], 'm--', label='{0:3.2f} + {1:3.2f} x (excluding bottom 5% and top 5%)'.format(\
		dx.loc['Intercept', 'Coef.'], dx.loc['t2m', 'Coef.']), lw=3.)
	ax.legend(loc='upper left', title='', alignment='left')
	ax.set_ylim(ax.get_ylim() * np.array([1., 1.5]))
	fig.savefig('./figures/scatter_optimal_byunit_{0:s}_within_robustness.pdf'.format(experiment), bbox_inches='tight', transparent=True)
