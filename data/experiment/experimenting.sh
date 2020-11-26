structure=$1
sorting=$2
command="python3 python/speller_${structure}.py -d data/experiment/${sorting}/dict -m 0 data/experiment/${sorting}/infile"
echo -e "\n ${structure} - ${sorting} \n"
time $command
