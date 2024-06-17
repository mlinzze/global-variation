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

experiments = ['01a']

for experiment in experiments:

	fig, ax = plt.subplots(figsize=(5,4))

	df_pred_global = pd.read_csv('./results/predictions_byunit_{0:s}_POOLED.csv'.format(experiment))
	df_pred_global['t2m_mean'] = df_pred_global['t2m_mean'] - 273.15
	df_pred_global = df_pred_global.sort_values(by=['t2m_mean'], ascending=True)

	df_pred_global['index_new'] = df_pred_global['t2m_mean'].astype(str)
	t2m_optimal = df_pred_global.set_index('index_new')['fit'].idxmax()
	t2m_optimal_y = df_pred_global.set_index('index_new').loc[t2m_optimal, 'fit']
	t2m_optimal = float(t2m_optimal)

	ax.plot(df_pred_global['t2m_mean'].values, df_pred_global['fit'].values, 'g-', lw=1., label='Global response function')
	ax.plot(t2m_optimal, t2m_optimal_y, 'go', markersize=4.)

	df = pd.read_csv('./results/optimal_temperature_byunit_{0:s}.csv'.format(experiment))
	df = df.loc[df['t2m_optimal'].notnull(), :]
	units = df['id'].unique()

	ifiles = [f for f in os.listdir('./results/') if ('predictions_byunit_{0:s}_'.format(experiment) in f)]

	for i, ifile in enumerate(ifiles):

		unit = ifile.split('.csv')[0].split('_')[-1]
		if unit not in units:
			continue

		df_pred = pd.read_csv('./results/' + ifile)
		df_pred['t2m_mean'] = df_pred['t2m_mean'] - 273.15
		df_pred = df_pred.sort_values(by=['t2m_mean'], ascending=True)
		if i == 0:
			ax.plot(df_pred['t2m_mean'].values, df_pred['fit'].values, '-', color='grey', alpha=0.2, lw=0.1, label='Location-specific response functions')
		else:
			ax.plot(df_pred['t2m_mean'].values, df_pred['fit'].values, '-', color='grey', alpha=0.2, lw=0.1)

	ax.legend(loc='upper left')
	ax.set_xlabel('Daily temperature (degree Celsius)')
	ax.set_ylabel('Outdoor activiy')
	sns.despine(ax=ax, offset=1., right=True, top=True)
	fig.savefig('./figures/predictions_all_{0:s}.pdf'.format(experiment),
				bbox_inches='tight', transparent=True)

	ax.set_xticks(np.arange(-5., 30.+5., 5.))
	ax.set_xlim(-10., 35.)
	ax.set_ylim(-0.3, 0.3)
	fig.savefig('./figures/predictions_all_{0:s}_sel.pdf'.format(experiment),
				bbox_inches='tight', transparent=True)

	fig.savefig('./figures/predictions_all_{0:s}_sel.png'.format(experiment),
				bbox_inches='tight', transparent=True, dpi=400)

