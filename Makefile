.PHONY: all clean

all:
	Rscript ./01_regressions.R
	python3 ./02_extract_optima.py
	python3 ./03_plot_optima.py
	python3 ./04_regress_optima.py
	python3 ./05_make_latextable.py
	python3 ./06_projections.py
	python3 ./07_plot_errorbars.py
	python3 ./08_plot_responses.py

clean:
	rm ./results/*
	rm ./tables/*
	rm ./figures/*
