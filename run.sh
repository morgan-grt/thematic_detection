#!/bin/bash

# variables initialisation
PORT=9090;
FILE="cfp/block-low.json";
OUTPUT_FILE="result/res.json";
USER_MAX_CPU=-1;
USER_MAX_SIZE=-1;
USER_PRETTY="true";
CONTAINER_NAME="thematic_detection_app-api_1";
IMAGE_NAME="app_classifier";
NETWORK_NAME="thematic_detection_default";

printHelp() {
	cat << EOF
	
Select a parameter in the list below:
	-i|--init-docker : init the docker container
		use :
			-i

	-r|--remove-docker : remove default named container/image/network
		use : 
			-r --parameter value ...
		parameters (not required) :
			[--container-name, default=$CONTAINER_NAME] 
			[--image-name, default=$IMAGE_NAME] 
			[--network-name, default=$NETWORK_NAME]

	-c|--curl : do a curl request with a cfp file (json)
		use : 
			-c --parameter value ...
		parameters (not required) :
			[--port, default=$PORT] 
			[-f|--file, default=$FILE] 
			[-o|--output-file, default=$OUTPUT_FILE]
			[--max-cpu, default=$USER_MAX_CPU]
			[--max-size, default=$USER_MAX_SIZE]
			[--pretty, default=$USER_PRETTY]

	-h : for help
	
Some examples to launch : 
	- ./run.sh -i
	- ./run.sh -c -f cfp/block-low.json --output-file result/result.json --port 9090
	- ./run.sh -c -f cfp/block-low.json --max-cpu 4 --pretty true

Have a great time !
EOF
}

if [[ $1 == "" ]]; then
	echo "Missing parameter";
	printHelp;
	exit 0;
fi

# parsing arguments/parameters
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  	key="$1"

  	case $key in
  		# display help
	    -h|--help)
			ACTION='h';
			echo -e "Action set to display help";
	      	shift;
	      	break
	      	;;

	    # argument for action
	    -i|--init-docker)
			ACTION='i';
			echo -e "Action set to init docker";
	      	shift;
			break
	      	;;
	    -r|--remove-docker)
			ACTION='r';
			echo -e "Action set to remove docker";
			shift
			;;
	    -c|--curl)
			ACTION='c';
			echo -e "Action set to curl request";
	      	shift
	      	;;

	    # parameter for remove docker action
	    --container-name)
			CONTAINER_NAME=$2;
			echo -e "Parameter container_name set to $2";
			shift;
			shift
			;;
		--image-name)
			IMAGE_NAME=$2;
			echo -e "Parameter image_name set to $2";
			shift;
			shift
			;;
		--network-name)
			NETWORK_NAME=$2;
			echo -e "Parameter network_name set to $2";
			shift;
			shift
			;;
	    
	    # parameter for curl action
	    --port)
			PORT=$2;
			echo -e "Parameter port set to $2";
			shift;
			shift
			;;
	    -f|--file)
			FILE=$2;
			echo -e "Parameter userfile set to $2";
			shift;
			shift
			;;
		-o|--output-file)
			OUTPUT_FILE=$2;
			echo -e "Parameter output file set to $2";
			shift;
			shift
			;;
	    --max-cpu)
			USER_MAX_CPU=$2;
			echo -e "Parameter user_max_cpu set to $2";
			shift;
			shift
			;;
		--max-size)
			USER_MAX_SIZE=$2;
			echo -e "Parameter user_max_size set to $2";
			shift;
			shift
			;;
		--pretty)
			USER_PRETTY=$2;
			echo -e "Parameter user_pretty set to $2";
			shift;
			shift
			;;

		# unknown option
	    *)
	      	POSITIONAL+=("$1"); # save it in an array for later
	      	shift # past argument
	      	;;
  	esac
done

set -- "${POSITIONAL[@]}" # restore positional parameters

case $ACTION in
	h) 
		printHelp
		;;
	i)
		echo -e "Preparing the docker container ...\n";
		sudo docker-compose -f stack.yml up -d
		;;
	r)
		echo -e "Stopping docker named $CONTAINER_NAME ...\n";
		sudo docker stop $CONTAINER_NAME

		echo -e "Deleting docker named $CONTAINER_NAME ...\n";
		sudo docker rm $CONTAINER_NAME

		echo -e "Deleting image named $IMAGE_NAME ...\n";
		sudo docker rmi $IMAGE_NAME;

		echo -e "Deleting network named $NETWORK_NAME ...\n";
		sudo docker network rm $NETWORK_NAME;

		echo -e "Deletion completed ..."
		;;
	c)
		echo -e "Executing curl post request to api on port $PORT with parameters:";
		echo -e "	userfile=$FILE";
		echo -e "	user_max_cpu=$USER_MAX_CPU";
		echo -e "	user_max_size=$USER_MAX_SIZE";
		echo -e "	user_pretty=$USER_PRETTY";
		echo -e "	output_file=$OUTPUT_FILE";
		echo -e "";

		curl --location "http://localhost:$PORT/upload" \
			--form "userfile=@$FILE" \
			--form "user_max_cpu=$USER_MAX_CPU" \
			--form "user_max_size=$USER_MAX_SIZE" \
			--form "user_pretty=$USER_PRETTY" \
			> $OUTPUT_FILE
		;;
	*)
    	echo -e "Not recognized action: $ACTION, pass..."
    	;;
esac

if [[ -n $1 ]]; then
    echo -e "Not recognized argument: $1";
fi

echo -e "all done, end...";
echo -e "--------------";
exit 0;