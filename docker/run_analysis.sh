#!/bin/bash
doi="$1" # get DOI

# download dataset
python2 download_dataset.py "$doi"

# process all R files and collect data
python2 set_environment.py $PWD

# execute R files
Rscript exec_r_files.R "$doi"

FILE=run_log.csv
if [ -f "$FILE" ]; then
     echo "$FILE exists"
else
     echo "$doi,unknown,source,other error" > run_log.csv
fi

FILEDS=run_log_ds.csv
if [ -f "$FILEDS" ]; then
     echo "$FILEDS exists"
else
     echo "$doi,unknown,download error" > run_log_ds.csv
fi

FILES=run_log_st.csv
if [ -f "$FILES" ]; then
     echo "$FILES exists"
else
     echo "0,0,0,download error" > run_log_st.csv
fi

FILEST=run_log_st1.csv
if [ -f "$FILEST" ]; then
     echo "$FILEST exists"
else
     echo "download error,0,0,0,0,0" > run_log_st1.csv
fi

# send results 
python2 save_result_in_dynamo.py "$doi"