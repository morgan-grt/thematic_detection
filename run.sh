#!/bin/bash

printHelp() {
	cat << EOF
	
Select a parameter in the list below:
	-i : init the docker container
	-c : do a curl request with a cfp,
	     need : -c [your_filename] [result_filename]
	     files are in json
	-h : for help
	
Some examples to launch : 
	- ./run.sh -i or 
	- ./run.sh -c cfp.json result.json

Have a great time !
EOF
}


if [[ $1 == "" ]]; then
	echo "Missing parameter";
	printHelp;
	exit 0;
fi

while getopts "cih" option
do
	echo -e "--------------\n";
	case $option in		
		c)
			echo -e "Executing cURL POST request to api ...\n";
			curl --location "http://localhost:8080/fileupload" --form "filetoupload=@$2" > $3;;
				
		i)
			echo -e "Preparing the docker container ...\n";
			sudo docker-compose -f stack.yml up -d;;
				
		h)
			echo -e "Parameter: $option\nAction: display help";
			printHelp;;
	esac
	echo -e "\ntask done"
done

echo "all done, ending ...";
echo -e "\n--------------";
exit 0;