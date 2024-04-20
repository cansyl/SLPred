#!/bin/sh
cd ncbi-blast
chmod 777 psiblast
chmod 777 psiblastMAC
cd ..

#!/bin/sh



if [ -f saved_models.zip ]; then
	echo "Aldready downloaded saved models!"
else
	echo "Downloading saved models"
        if [ -x "$(which wget)" ] ; then
	    wget --no-check-certificate -r 'https://slpred.kansil.org/saved_models.zip' -O saved_models.zip
	    echo "Saved models download completed!"
	    echo "Extracting saved models..."
            unzip saved_models.zip
            echo "Saved models extraction completed!."
	elif [ -x "$(which curl)" ] ; then
	    curl 'https://slpred.kansil.org/saved_models.zip' -O saved_models.zip
	    echo "Saved models download completed!"
	    echo "Extracting saved models..."
            unzip saved_models.zip
            echo "Saved models extraction completed!."
            rm saved_models.zip
	else 
	    echo "***Please install wget or curl***"
	fi
        
fi



if [ -f Trust_all_data.zip ]; then
	echo "Aldready downloaded Trust data!"
else
	echo "Downloading Trust data"
	if [ -x "$(which wget)" ] ; then
	    wget --no-check-certificate -r 'https://slpred.kansil.org/Trust_all_data.zip' -O Trust_all_data.zip
	    echo "Trust data download completed!"
	    echo "Extracting Trust data..."
            unzip Trust_all_data.zip
            echo "Trust data extraction completed!."
	elif [ -x "$(which curl)" ] ; then
	    curl 'https://slpred.kansil.org/Trust_all_data.zip' -O Trust_all_data.zip
	    echo "Trust data download completed!"
	    echo "Extracting Trust data..."
            unzip Trust_all_data.zip
            echo "Trust data extraction completed!."
            rm Trust_all_data.zip
	else 
	    echo "***Please install wget or curl***"
	fi
        
fi





