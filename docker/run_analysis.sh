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
timeout 1h python2 download_dataset.py "$doi"

if [ $? -eq 124 ]; then
     echo "$doi,unknown,download error" >> run_log.csv
else
     # only needed for R 3.2.1
     #ln -s /lib/x86_64-linux-gnu/libreadline.so.7.0 /lib/x86_64-linux-gnu/libreadline.so.6

     # process all R files and collect data

     # add brackets to metrics.txt so that the file is readable with json
     echo "[" >> metrics.txt
     python2 set_environment.py $PWD

     # execute R files with 3 hour limit
     timeout 5h Rscript exec_r_files.R "$doi"

     # note if 3hr time limit exceeded 
     if [ $? -eq 124 ]; then
          echo "$doi,unknown,time limit exceeded" >> run_log.csv
     fi

     sed -i '$s/,$//' metrics.txt
     echo "]" >> metrics.txt
fi

# send results 
python2 save_result_in_dynamo.py "$doi" "$test"
