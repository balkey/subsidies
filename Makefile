
run: data.csv
	python application.py

data.csv: scaffold
	if [ ! -f raw/data.csv ]; \
	then \
		curl -o raw/data.csv 'http://datastore.openspending.org/6018ab87076187018fc29c94a68a3cd2/eu-esif-funds-beneficiaries-2000-2020-full/data/eu-esif-funds-beneficiaries-2007-2020-full.csv'; \
	fi;

scaffold: build
	mkdir raw


build:
	$(shell read -p "User name: " REPLY ; ) \
	somevar= $$REPLY \
	echo $(somevar)




    #@read -p "Enter Module Name:" module; \  
    #module_dir=./modules/$$module; \
    #mkdir -p $$module_dir/build


#build:  
    #@read -p "Enter country code, which you want to geocode:" country; \  
    #export FOO \
	#export -p | grep FOO \
	#declare -x FOO=$$country