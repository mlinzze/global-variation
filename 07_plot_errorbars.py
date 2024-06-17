#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import copy
import string

import numpy as np
import pandas as pd
import scipy

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

## ===================================================================== ##
## within versus between

letters = list(string.ascii_uppercase)

fig, ax = plt.subplots(figsize=(3,2))

xticklabels = []
xticks = []
x = 0.
e = 0.

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_between.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='r'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_within.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='b'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_weighted.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k')

ax.set_xticks(list(np.arange(0., e+1, 1.)))
ax.set_xticklabels(letters[:int(e)+1])

xlims = [-1., e+1]
ax.set_xlim(xlims)
ax.plot(xlims, [0., 0.], 'k', lw=0.5)
ax.set_ylim(-0.1, 1.)

sns.despine(ax=ax, offset=1., right=True, top=True)
fig.savefig('./figures/coeffs_optimal_byunit_01.pdf', bbox_inches='tight', transparent=True)

## ============
## controls

letters = list(string.ascii_uppercase)[4:]

fig, ax = plt.subplots(figsize=(3,2))

xticklabels = []
xticks = []
x = 0.
e = 0.

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_controls.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k')

ax.set_xticks(list(np.arange(0., e+1, 1.)))
ax.set_xticklabels(letters[:int(e)+1])

xlims = [-1., e+1]
ax.set_xlim(xlims)
ax.plot(xlims, [0., 0.], 'k', lw=0.5)
ax.set_ylim(-0.1, 1.)

sns.despine(ax=ax, offset=1., right=True, top=True)
fig.savefig('./figures/coeffs_optimal_byunit_02.pdf', bbox_inches='tight', transparent=True)

## ============
## functional form 

letters = list(string.ascii_uppercase)[6:]

fig, ax = plt.subplots(figsize=(3,2))

xticklabels = []
xticks = []
x = 0.
e = 0.

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01b_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01c_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_02_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k')

ax.set_xticks(list(np.arange(0., e+1, 1.)))
ax.set_xticklabels(letters[:int(e)+1])

xlims = [-1., e+1]
ax.set_xlim(xlims)
ax.plot(xlims, [0., 0.], 'k', lw=0.5)
ax.set_ylim(-0.1, 1.)

sns.despine(ax=ax, offset=1., right=True, top=True)
fig.savefig('./figures/coeffs_optimal_byunit_03.pdf', bbox_inches='tight', transparent=True)

## ============
## year 1 versus 2

letters = list(string.ascii_uppercase)[10:]

fig, ax = plt.subplots(figsize=(3,2))

xticklabels = []
xticks = []
x = 0.
e = 0.

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_negcorr.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01Y1_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1

df = pd.read_csv('./results/coeffs_stage2_byunit_01Y2_main.csv')
print(df['nobs'].values[0])
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k')

ax.set_xticks(list(np.arange(0., e+1, 1.)))
ax.set_xticklabels(letters[:int(e)+1])

xlims = [-1., e+1]
ax.set_xlim(xlims)
ax.plot(xlims, [0., 0.], 'k', lw=0.5)
ax.set_ylim(-0.1, 1.)

sns.despine(ax=ax, offset=1., right=True, top=True)
fig.savefig('./figures/coeffs_optimal_byunit_04.pdf', bbox_inches='tight', transparent=True)

## ===================================================================== ##
## placebo

fig, ax = plt.subplots(figsize=(5,4))

xticklabels = []
xticks = []
x = 0.
e = 0.

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_main.csv')
df = df.set_index(df.columns[0])
y = df.loc['t2m', 'Coef.']
yerr = 1.96 * df.loc['t2m', 'Std.Err.']
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='k'); e+= 1.

df = pd.read_csv('./results/coeffs_stage2_byunit_01a_random.csv')
y = df['coef'].mean()
yerr = np.abs(df['coef'].quantile([0.975, 0.025]).values - y).reshape(2, 1)
ax.errorbar(x+e, y, yerr, marker='o', markersize=4., lw=2., capsize=6., color='grey'); e+= 1.

ax.set_xticks(list(np.arange(0., e, 1.)))
letters = list(string.ascii_uppercase)
ax.set_xticklabels(letters[:int(e)])

xlims = ax.get_xlim()
xlims = [-1., 2.]
ax.plot(xlims, [0., 0.], 'k', lw=0.5)

ax.set_ylabel('Change in the preferred temperature\n per degree C in annual mean temperature')
sns.despine(ax=ax, offset=1., right=True, top=True)
fig.savefig('./figures/coeffs_optimal_byunit_placebo.pdf', bbox_inches='tight', transparent=True)
