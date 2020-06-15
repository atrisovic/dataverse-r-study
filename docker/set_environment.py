# find libraries in R files
import os
import sys
import glob
import chardet
import fileinput

list_of_r_files = glob.glob("*.R")
list_of_r_files.extend(glob.glob('*.r'))
list_of_r_files.remove('exec_r_files.R')

def get_list_of_all():
    ''' collect file names of all files '''
    list_of_all = glob.glob("*")
    study_files = ['run_analysis.sh', 'download_dataset.py', 'set_environment.py', \
            'exec_r_files.R', 'save_result_in_dynamo.py', 'run_log_ds.csv', \
            'run_log_st.csv', 'run_log_st1.csv']
    for sf in study_files:
        if sf in list_of_all: list_of_all.remove(sf)

    return list_of_all

def get_size_of_replication_package():
    ''' calculate size of the replication package '''
    list_of_all = get_list_of_all()
    return sum(os.path.getsize(f) for f in list_of_all if os.path.isfile(f))


def detect_encoding(input):
    result = chardet.detect(input)
    return result['encoding'], result['confidence']


def parse_dependencies(line):
    ''' finds libs between two brackets '''
    lib = line[line.find("(")+1:line.find(")")]
    lib = lib.strip('"')
    lib = lib.strip("'")
    return_str = 'install.packages(\"{}\", repos=\"http://cran.us.r-project.org\")\n'.format(lib)
    return return_str


def fix_abs_paths(line, index):
    ''' returns file name without absolute path '''
    rest = line[index:]

    count = 0 # when -1 add ")"
    for i,w in enumerate(rest):
        if w == "(":
            count = count +1
        if w == ")":
            count = count -1
        if count == -1:
            break
    newline = line[:index]+"basename("+rest[:i]+")"+rest[i:]   
    return newline


def fix_abs_path_in_readcsv(line):
    index = line.find('read.csv')+8
    rest = line[index:]
    # find (
    b = rest.find("(")+1
    rest = line[index + b:]

    count = 0 # when -1 add ")"
    for i,w in enumerate(rest):
        if w == "," and count == 0: # in this case there are arguments
            break
        if w == "(":
            count = count +1
        if w == ")":
            count = count -1
        if count == -1: # found both open and closed brackets
            break
    newline = line[:index + b]+"basename("+rest[:i]+")"+rest[i:]
    return newline


def main():
    total_libraries = 0 # count of dependencies
    total_comments = 0 # count of comments

    for r_file in list_of_r_files:
        libraries_no = 0 # libraries per file
        comments_no = 0 # count of comments per file
        lines_no = 0 # count of total lines of code per file
        func_no = 0 # count of functions 
        test_no =0 # count of 'test' appearance 
        class_no=0 # count 'class' appearances

        for linenum, line in enumerate(fileinput.input(r_file, inplace=True)):
            lines_no +=1 # increase no of lines

            if linenum == 0:
                wd = sys.argv[1]
                print("setwd('{}')\n".format(wd))

            if ("#" in line) or (line.strip().startswith('"')): # count comments
                comments_no += 1
                print(line.rstrip())
                continue # go to the next line 

            if line.strip().startswith("setwd"): # setwd already set, remove this to avoid absolute paths
                print(line.replace(line, ''))
                continue

            if "library" in line.strip():
                libraries_no += 1

                # more than one lib
                import re
                for match in re.finditer("library", line):
                    print(line.replace(line, parse_dependencies(line[match.start():])))
                print(line.rstrip())
                continue

            elif line.strip().startswith("install.packages"):
                libraries_no += 1
                print(line.rstrip())
                continue
                
            elif line.strip().startswith("require"):
                libraries_no += 1
                print(line.replace(line, parse_dependencies(line)))
                print(line.rstrip())
                continue

            temp_line = line.replace(" ", "") # remove white spaces to detect function calls easier
            if "test" in line:
                test_no += 1
        
            if "<-function(" in temp_line: # use temp line
                func_no += 1
        
            if "class(" in temp_line: # use temp line
                class_no += 1

            if "file.path(" in temp_line:
                index = line.find('file.path')
                print(line.replace(line, fix_abs_paths(line, index)))

            elif "source(" in temp_line and "/" in line:
                index = line.find('source')+6
                rest = line[index:]
                # find (
                b = rest.find("(")+1
                index = index + b
                print(line.replace(line, fix_abs_paths(line, index)))

            elif "read.csv(" in temp_line and "/" in line:
                print(line.replace(line, fix_abs_path_in_readcsv(line)))

            else: # for all other lines
                print(line.rstrip())

        # increase total counts
        total_libraries += libraries_no 
        total_comments += comments_no
        
        encoding, confidence = detect_encoding(open(r_file, 'r').read())
        with open('run_log_st1.csv','a') as f:
            # file_name, total lines, number of comments, number of dependencies
            f.write("{},{},{},{},{},{},{},{},{}\n".format(r_file, \
                lines_no, comments_no, libraries_no, func_no, test_no, class_no, encoding, confidence))


    with open('run_log_st.csv','a') as f:
        # number of comments, number of dependencies, size, list of files
        size = get_size_of_replication_package()
        f.write("{},{},{},{}\n".format(total_comments, total_libraries, size, ";".join(get_list_of_all())))


if __name__ == "__main__":
    main()