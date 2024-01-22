#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Please specify a single suffix as an argument to this script"
    exit 1
fi

suffix=$1

files=`find -name "*.$suffix"`

numFiles=`echo $files | wc -w`

if [[ $numFiles -ne 1 ]]; then
    echo "There are $numFiles files with suffix .$suffix"
else
    echo "There is $numFiles file with suffix .$suffix"    
fi
if [[ $numFiles -eq 0 ]]; then
    exit 0
fi

tar -cjf Files_$suffix.tar.bz2 $files
