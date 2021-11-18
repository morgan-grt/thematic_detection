#!/bin/bash

printHelp() {
	cat << EOF
	
Select a parameter in the list below:
	-i : init the docker container
	-c : do a curl request with a cfp,
	     need : -c [your_filename] [result_filename] [port, default=9090]
	     files are in json
	-f : do a curl request with a cfp with default value
	-h : for help
	
Some examples to launch : 
	- ./run.sh -i or 
	- ./run.sh -c cfp/block-low.json result/result.json 9090

Have a great time !
EOF
}


if [[ $1 == "" ]]; then
	echo "Missing parameter";
	printHelp;
	exit 0;
fi

while getopts "cifh" option
do
	echo -e "--------------\n";
	case $option in		
		c)
			port=$4;
			if [[ $4 == "" ]]; then
				port=9090;
			fi
			echo -e "Executing cURL POST request to api ...\n";
			curl --location "http://localhost:$port/fileupload" --form "filetoupload=@$2" > $3;;
				
		i)
			echo -e "Preparing the docker container ...\n";
			sudo docker-compose -f stack.yml up -d;;

		f)
			echo $2;
			port=$2;
			if [[ $2 == "" ]]; then
				port=9090;
			fi
			echo $port;
			echo -e "Executing cURL POST request to api ...\n";
			curl --location "http://localhost:$port/fileupload" --form 'filetoupload=@"cfp/block-low.json"' > 'result/res.json';;
				
		h)
			echo -e "Parameter: $option\nAction: display help";
			printHelp;;
	esac
	echo -e "\ntask done"
done

echo "all done, ending ...";
echo -e "\n--------------";
exit 0;