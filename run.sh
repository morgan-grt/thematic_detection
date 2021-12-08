#!/bin/bash

printHelp() {
	cat << EOF
	
Select a parameter in the list below:
	-i : init the docker container
	-c : do a curl request with a cfp,
		need : -c [your_filename] [result_filename] [port, default=9090]
		files are in json
	-f : do a curl request with a cfp with default value
	-r : remove default named container/image/network, else it can 
		get parameter
		default : -r
		custom : -r [container_name] [image_name] [network_name]
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

while getopts "cifrh" option
do
	echo -e "--------------\n";
	case $option in		
		c)
			port=$4;
			if [[ $4 == "" ]]; then
				port=9090;
			fi
			echo -e "Executing cURL POST request to api on port $port ...\n";
			curl --location "http://localhost:$port/fileupload" --form "filetoupload=@$2" > $3;;
				
		i)
			echo -e "Preparing the docker container ...\n";
			sudo docker-compose -f stack.yml up -d;;

		f)
			port=$2;
			if [[ $2 == "" ]]; then
				port=9090;
			fi
			echo -e "Executing default cURL POST request to api on port $port ...\n";
			curl --location "http://localhost:$port/fileupload" --form 'filetoupload=@"cfp/block-low.json"' > 'result/res.json';;

		r)
			container_name=$2;
			image_name=$3;
			network_name=$4;

			if [[ $2 == "" ]]; then
				container_name="thematic_detection_app-api_1";
			fi
			if [[ $3 == "" ]]; then
				image_name="app_classifier";
			fi
			if [[ $4 == "" ]]; then
				network_name="thematic_detection_default";
			fi

			echo -e "Stopping docker named $container_name ...\n";
			sudo docker stop $container_name

			echo -e "Deleting docker named $container_name ...\n";
			sudo docker rm $container_name

			echo -e "Deleting image named $image_name ...\n";
			sudo docker rmi $image_name;

			echo -e "Deleting network named $network_name ...\n";
			sudo docker network rm $network_name;

			echo -e "Deletion completed ...";;
				
		h)
			echo -e "Parameter: $option\nAction: display help";
			printHelp;;
	esac
	echo -e "\ntask done"
done

echo "all done, ending ...";
echo -e "\n--------------";
exit 0;