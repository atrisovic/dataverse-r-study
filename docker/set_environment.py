# find libraries in R files
import os
import re
import sys
import glob
import codecs
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
            'run_log_st.csv', 'run_log_st1.csv', 'execute_files.py', 'readability_analysis.py', \
            'readability_analysis.pyc', 'get_reprod.RData', 'run_log.csv', 'metrics.txt', 'vars.txt']
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
    ''' finds libs between two brackets 
    library(ABC) should be transformed into require(ABC)
    and if not accessible install ABC'''

    lib = line.replace(" ", "") 
    lib = line[line.find("(")+1:line.find(")")]
    lib = lib.strip('"')
    lib = lib.strip("'")

    return_str = 'if (!require(\"{}\")) install.packages(\"{}\")\n'.format(lib, lib)

    if "," in lib: # there are unparced arguments
        return line 
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


def parse_libraries(line):
    temp = line.strip()
    temp = line.replace(" ", "")
    temp = temp.replace('"', "")
    temp = temp.replace("'", "")
    temp = temp.rstrip(",")

    if ")" in line:
        libs = re.findall(r'\((.*?)\)', temp)
        return libs[0].split(",")

    libs = re.findall(r'\((.*)', temp)
    return libs[0].split(",")


def parse_packages(line):
    temp = line.strip()
    temp = temp.replace(" ", "")
    temp = temp.replace('"', "")
    temp = temp.replace("'", "")
    temp = temp.rstrip(",")

    if ")" in line:
        libs = re.findall(r'\((.*?)\)', temp)
        return libs[0].split(",")

    libs = re.findall(r'\((.*)', temp)
    return libs[0].split(",")


def main():
    total_libraries = 0 # count of dependencies
    total_comments = 0 # count of comments
    list_of_libs = []

    for r_file in list_of_r_files:

        # encode to ascii
        allcode = open(r_file, 'r').read()
        encoding, confidence = detect_encoding(allcode)
        if encoding != 'ascii':
            allcode = allcode.decode(encoding).encode('ascii', 'ignore')
            with codecs.open(r_file, 'w', encoding='ascii') as f:
                f.write(allcode)     
        
        # collect metrics
        from readability_analysis import get_readability_metrics
        get_readability_metrics(allcode, r_file)

        libraries_no = 0 # libraries per file
        comments_no = 0 # count of comments per file
        lines_no = 0 # count of total lines of code per file
        func_no = 0 # count of functions 
        test_no =0 # count of 'test' appearance 
        class_no=0 # count 'class' appearances

        not_authorized = False

        for linenum, line in enumerate(fileinput.input(r_file, inplace=True)):
            lines_no +=1 # increase no of lines

            if "you are not authorized to access this object via this api endpoint" in line:
                not_authorized = True
                break

            if linenum == 0:
                wd = sys.argv[1]
                print("setwd('{}')\n".format(wd))

            # ignore empty lines
            if not line.strip():
                print(line.rstrip())
                continue

            # ===================
            # = CODE PROPERTIES =
            # ===================


            # if line is commented no point analyzing it
            if line.strip().startswith('#') or line.strip().startswith('"'):
                comments_no += 1
                print(line.rstrip())
                continue

            # count comments elsewhere in code
            if "#" in line: 
                comments_no += 1

            if "test" in line:
                test_no += 1

            # remove white spaces to detect function calls easier
            temp_line = line.replace(" ", "") 

            if "<-function(" in temp_line: 
                func_no += 1
        
            if "class(" in temp_line: 
                class_no += 1

            # ===============
            # = CHANGE CODE =
            # ===============

            # setwd already set, remove this to avoid absolute paths
            if "setwd(" in temp_line: 
                print(line.replace(line, ''))
                continue

            if "libraries(" in temp_line:
                list_of_libs.extend(parse_libraries(line))

            if "library(" in temp_line and "install.packages" in line and "#" not in line:
                libraries_no += 1
                print(line.rstrip())

                list_of_libs.extend(re.findall(r'library\((.*?)\)', line))
                continue

            elif "require" in line and "install.packages" in line and "#" not in line:
                libraries_no += 1
                print(line.rstrip())

                list_of_libs.extend(re.findall(r'require\((.*?)\)', line))
                continue

            elif "library(" in temp_line:
                libraries_no += 1
                for match in re.finditer("library", line):
                    print(line.replace(line, parse_dependencies(line[match.start():])))

                list_of_libs.extend(re.findall(r'library\((.*?)\)', line))
                continue

            elif line.strip().startswith("install.packages"):
                # install packages should work as is when default CRAN mirror is set
                libraries_no += 1
                print(line.rstrip())

                list_of_libs.extend(re.findall(r'install.packages\((.*?)\)', line))
                continue
                
            elif temp_line.strip().startswith("require("):
                libraries_no += 1
                print(line.replace(line, parse_dependencies(line)))

                list_of_libs.extend(re.findall(r'require\((.*?)\)', line))
                continue

            # find packages that did not qualify for "install.packages"
            if "packages" in temp_line and "," in temp_line and "(" in temp_line:
                list_of_libs.extend(parse_packages(line))

            if "file.path(" in temp_line:
                index = line.find('file.path')
                print(line.replace(line, fix_abs_paths(line, index)))

            elif "source(" in temp_line and "/" in line:
                if "http" not in line:
                    index = line.find('source')+6
                    rest = line[index:]
                    # finding (
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
        
        
        if not_authorized is False:
            with open('run_log_st1.csv','a') as f:
                # file_name, total lines, number of comments, number of dependencies
                f.write("{},{},{},{},{},{},{},{},{}\n".format(r_file, \
                    lines_no, comments_no, libraries_no, func_no, test_no, class_no, encoding, confidence))


    list_of_libs = [l.replace('"',"") for l in list_of_libs]
    list_of_libs = [l.replace(' ',"") for l in list_of_libs]
    list_of_libs = [l.replace("'","") for l in list_of_libs]

    list_of_libs = set(list_of_libs)

    if not_authorized is False:
        with open('run_log_st.csv','a') as f:
            # number of comments, number of dependencies, size, list of files
            size = get_size_of_replication_package()
            f.write("{},{},{},{},{}\n".format(total_comments, total_libraries, size, ";".join(get_list_of_all()), ";".join(list_of_libs)))


if __name__ == "__main__":
    main()