args = commandArgs(trailingOnly=TRUE)
# parse command line args for path to the directory and preprocessing
dir_path_doi = args[1]

setwd("/usr/workdir")
library(stringr)

install.packages("R.utils",repos = "http://cran.us.r-project.org")
library(R.utils)

r_files = list.files(".", pattern="\\.[Rr]\\>", recursive=FALSE, full.names=FALSE)
r_files <- r_files[r_files != "exec_r_files.R"]
print(r_files)

for (r_file in r_files) {
	print(paste("Executing: ", r_file))

	# parse out file name, leaving out the ".R" part
	filename = substr(r_file, 1, nchar(r_file) - 2)

	save(dir_path_doi, r_files, r_file, filename,
		 file="get_reprod.RData")


	# try to run the R file with error handling
	error <- withTimeout({ 
		try(source(r_file), silent = TRUE);
	}, timeout=600, onTimeout="silent");

	# restore local variables
	load("get_reprod.RData")

	# if there was an error

	if (class(error) == "try-error") {
            # trim whitespace from beginning and end of string
	    error = str_trim(error[1])
	    # parse all the quotes from the error string
	    error = str_replace_all(error, "\"", "")
		# parse all the quotes from the error string
	    error = str_replace_all(error, "‘", "'") 
		error = str_replace_all(error, "’", "'")
	    # replace all newline characters in middle of string with special string
	    error = str_replace_all(error, "[\n]", "[newline]")
	}
	else {
		error = "success"
		}
	

	if (grepl("reached CPU time limit", error, fixed = TRUE)){
		error = "time limit exceeded"
	}


	# create dataframe from doi, filename, and errors to facilitate csv writing
	new_log_data = data.frame(doi=c(dir_path_doi), filename=c(r_file),
							  error=c(error), stringsAsFactors = FALSE)
	# write the new log data into the log file
	write.table(new_log_data, file="run_log.csv", sep=",", append=TRUE,
				row.names=FALSE, col.names=FALSE)

	print(new_log_data)
	}
