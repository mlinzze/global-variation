Overview
--------

The code in this replication package conducts the statistical analysis and produces the figures and tables presented in the journal article Linsenmeier, M. 2024: [Global variation in the preferred temperature for recreational outdoor activity](https://doi.org/10.1016/j.jeem.2024.103032). Journal of Environmental Economics and Management.

The package consists of several scripts written in Python 3 and R.

Data Availability
----------------------------

All original data are publicly available at no cost:

- Hourly weather data can be obtained from the European Center for Medium Range Weather Forecasts (ECMWF): ERA5: [https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels)
- Mobile phone location data can be obtained from Google: Google Mobility Reports: [https://www.google.com/covid19/mobility/](https://www.google.com/covid19/mobility/)
- Economic data can be obtained from the World Bank: GDP per capita: [https://databank.worldbank.org/source/world-development-indicators/Series/NY.GDP.PCAP.PP.KD](https://databank.worldbank.org/source/world-development-indicators/Series/NY.GDP.PCAP.PP.KD)

The pre-processed data can be accessed on Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11916968.svg)](https://doi.org/10.5281/zenodo.11916968)


Computational requirements
---------------------------

### Software Requirements

- Python 3.10.9
  - `numpy` 1.23.4
  - `pandas` 1.5.1
  - `scipy` 1.10.0
  - `statsmodels` 0.13.5
  - `geopandas` 0.12.0
  - `matplotlib` 3.6.1
  - `seaborn` 0.12.0

The file `requirements.txt` lists these dependencies, please run `pip install -r requirements.txt` as the first step. See [https://pip.readthedocs.io/en/1.1/requirements.html](https://pip.readthedocs.io/en/1.1/requirements.html) for further instructions on using the `requirements.txt` file.

- R 4.2.1
  - `fixest`
  - `splines`

### Memory and Runtime Requirements

The analysis and visualisation requires less than 1 hour on a standard (2024) desktop machine.

Instructions to Replicators
---------------------------

Replication of all figures:
- Note that all scripts require the data which can be accessed from the sources listed in the `Data availability` section.
- The file `parameters.py` includes the global variable DATAPATH that must be set by the user prior to executing the scripts. The variable links to the directory in which the data are stored.
- The name of each script also indicates its relative position in the intended order of execution (i.e. `01_`, `02_`, `03_`, ...).
- The replication is facilitated with a Makefile that runs the scripts in the correct order (`make clean; make all`).
- Some of the scripts store results (e.g. regression coefficients) in the folder `results`.
- Once all scripts have finished, all figures can be found in the folder `figures` and tables in the folder `tables`.

### License for Code and Data

The code in this repository is provided with a CC-BY license.
