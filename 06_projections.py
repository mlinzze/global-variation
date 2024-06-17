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

## ===================================================================== ##

from parameters import *

## ===================================================================== ##

df_data = pd.read_csv(os.path.join(DATAPATH, 'data_demeaned.csv'))

df_pred_global = pd.read_csv('./results/predictions_byunit_01a_POOLED.csv')

experiments = ['01a']

for experiment in experiments:

	df = pd.read_csv('./results/optimal_temperature_byunit_{0:s}.csv'.format(experiment))
	df = df.loc[df['t2m_optimal'].notnull(), :]
	units = df['id'].unique()

	df_results = pd.DataFrame(index=units)
	df_results['t2m_mean'] = np.nan

	ifiles = [f for f in os.listdir('./results/') if ('predictions_byunit_{0:s}_'.format(experiment) in f)]

	for ifile in ifiles:

		unit = ifile.split('.csv')[0].split('_')[-1]
		if unit not in units:
			continue

		print(unit)
		df_pred = pd.read_csv('./results/' + ifile)

		xvalues = df_data.loc[df_data['id'] == unit, 't2m_mean'].values

		## ===========

		df = pd.concat([df_pred, pd.DataFrame({'t2m_mean': xvalues, 'projection_past': True})], axis=0)
		df = pd.concat([df, pd.DataFrame({'t2m_mean': xvalues + 1., 'projection_future': True})], axis=0)
		df = df.loc[df['t2m_mean'].notnull(), :]
		df = df.set_index('t2m_mean')
		df = df.sort_index()
		dfi = df.drop(columns=['projection_past', 'projection_future']).interpolate(method='index')
		dfi['projection_past'] = df['projection_past']
		dfi['projection_future'] = df['projection_future']
		past = dfi.loc[dfi['projection_past'] == True, 'fit'].sum() / (dfi['projection_past'] == True).sum()
		future = dfi.loc[dfi['projection_future'] == True, 'fit'].sum() / (dfi['projection_future'] == True).sum()
		delta_unit = future - past 

		## ===========

		df = pd.concat([df_pred_global, pd.DataFrame({'t2m_mean': xvalues, 'projection_past': True})], axis=0)
		df = pd.concat([df, pd.DataFrame({'t2m_mean': xvalues + 1., 'projection_future': True})], axis=0)
		df = df.loc[df['t2m_mean'].notnull(), :]
		df = df.set_index('t2m_mean')
		df = df.sort_index()
		dfi = df.drop(columns=['projection_past', 'projection_future']).interpolate(method='index')
		dfi['projection_past'] = df['projection_past']
		dfi['projection_future'] = df['projection_future']
		past = dfi.loc[dfi['projection_past'] == True, 'fit'].sum() / (dfi['projection_past'] == True).sum()
		future = dfi.loc[dfi['projection_future'] == True, 'fit'].sum() / (dfi['projection_future'] == True).sum()
		delta_global = future - past 

		## ===========

		df_results.loc[unit, 'delta_unit'] = delta_unit
		df_results.loc[unit, 'delta_global'] = delta_global
		df_results.loc[unit, 't2m_mean'] = xvalues[pd.notnull(xvalues)].mean()

	df_results['bias'] = df_results['delta_global'] - df_results['delta_unit']

	df_results = df_results.sort_values(by='t2m_mean', ascending=True)
	df_results['t2m_mean'] = df_results['t2m_mean'] - 273.15

	fig, ax = plt.subplots(figsize=(5,4))
	ax.plot(df_results['t2m_mean'].values, df_results['bias'].values, 'ko', markersize=1., alpha=0.4, label='Bias from using global response function\ninstead of location-specific response functions')
	ax.plot([df_results['t2m_mean'].min(), df_results['t2m_mean'].max()], [0., 0.], 'k-', lw=1.)
	ax.legend()
	ax.set_xticks(np.arange(-5., 30.+5., 5.))
	ax.set_xlim(-10., 35.)
	ax.set_ylim(-0.1, 0.1)
	ax.set_yticks([])
	ax.set_xlabel('Annual mean temperature (degree Celsius)')

	sns.despine(ax=ax, offset=1., right=True, top=True, left=True)
	fig.savefig('./figures/projections_units_bias_{0:s}.pdf'.format(experiment),
				bbox_inches='tight', transparent=True)

	fig, ax = plt.subplots(figsize=(1,4))
	sns.boxplot(data=df_results, y='bias', fliersize=0.5, color='#D6D6D6')
	ax.plot([-1, 1], [0., 0.], 'k-', lw=1.)
	ax.set_ylim(-0.1, 0.1)
	ax.set_xlabel('')
	ax.set_ylabel('Change in outdoor activity\n from warming by 1 degree C')
	ax.yaxis.tick_right()
	ax.yaxis.set_label_position("right")

	sns.despine(ax=ax, offset=1., right=False, left=True, top=True)
	fig.savefig('./figures/projections_units_bias_{0:s}_boxplot.pdf'.format(experiment),
				bbox_inches='tight', transparent=True)
