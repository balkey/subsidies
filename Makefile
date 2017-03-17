run: data.csv
	python application.py

data.csv:
	curl -o raw/data.csv 'http://datastore.openspending.org/6018ab87076187018fc29c94a68a3cd2/eu-esif-funds-beneficiaries-2000-2020-full/data/eu-esif-funds-beneficiaries-2007-2020-full.csv'


