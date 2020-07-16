#!/bin/bash
doi="$1" # get DOI
test=False

# check if testing arg provided
if [ -n "$2" ]; then
    test=True
fi

# set default CRAN mirror
echo 'local({r <- getOption("repos");
       r["CRAN"] <- "http://cran.us.r-project.org"; 
       options(repos=r)})' >> ~/.Rprofile
echo '\n' >> ~/.Rprofile

# download dataset
python2 download_dataset.py "$doi"

# TODO testing
#sleep 10
#echo "a <- 10 + 2
#install.packages('stringr')
#require('a')
#install.packages('plyr')
#library('b')" > temp.R

# only needed for R 3.2.1
#ln -s /lib/x86_64-linux-gnu/libreadline.so.7.0 /lib/x86_64-linux-gnu/libreadline.so.6

# process all R files and collect data
python2 set_environment.py $PWD

# execute R files with 3 hour limit
timeout 3h Rscript exec_r_files.R "$doi"

# note if 3hr time limit exceeded 
if [ $? -eq 124 ]; then
     echo "$doi,unknown,time limit exceeded" >> run_log.csv
fi

# send results 
python2 save_result_in_dynamo.py "$doi" "$test"
