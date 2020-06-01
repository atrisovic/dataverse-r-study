import requests
import json
import os
import hashlib
import subprocess
import time
import re
import sys

directory = sys.argv[1] # DOI

server = "http://dataverse.harvard.edu/api/"
version = ":latest"
query = server + "datasets/:persistentId/versions/" + version + "?persistentId=" + directory

def curl_files(dlurl, fullpath, fileid, d):
    if d == 3:
        # after code tries to curl 3 times without success
        # it writes down this results and it is the end of the run
        with open('run_log_ds.csv', 'a') as out_file:
            out_file.write("{},{},checksum error\n".format(directory, fileid))
        return

    # curl to present directory (sigh) but use filename.label as output
    print("downloading from {}".format(dlurl))

    # -s suppresses progress bar, -S shows errors, -L follows redirects, -o is the output path/file
    curlcmd = 'curl -s -S -L -o "' + fullpath + '" ' + '\"' + dlurl + '\"'
    subprocess.call(curlcmd, shell=True)        # give slow disks a second
    time.sleep(1)        # check md5 against downloaded file
    hash = hashlib.md5()
    with open(str(fullpath), 'rb') as afile:
      buf = afile.read()
      hash.update(buf)
      localmd5 = hash.hexdigest()
    if md5 == localmd5:
       print 'MD5 match: Dataverse ' + md5 + ' Local copy ' + localmd5
    else:
       print 'CHECKSUM ERROR: Dataverse ' + md5 + ' Local copy ' + localmd5
       curl_files(dlurl, fullpath, fileid, d + 1)


print("Requesting file metadata from  {}".format(query))

r = requests.get(query)
j = json.loads(r.text)

for obj in j['data']['files']:
    fileid = obj['dataFile']['id']
    filename = obj['label']    # for ingested tabular files, restore the original file name extension:
    if 'originalFileFormat' in obj['dataFile'].keys():
        dlurl = server + '/access/datafile/' + str(fileid) + '?format=original'
        originaltype = obj['dataFile']['originalFileFormat']
        if originaltype == 'application/x-rlang-transport':
            filename = re.sub('\.[^\.]*$', '.RData', filename)
        elif originaltype.startswith('application/x-stata'):
            filename = re.sub('\.[^\.]*$', '.dta', filename)
        elif originaltype == 'application/x-spss-sav':
            filename = re.sub('\.[^\.]*$', '.sav', filename)
        elif originaltype == 'application/x-spss-por':
            filename = re.sub('\.[^\.]*$', '.por', filename)
        elif originaltype == 'text/csv':
            filename = re.sub('\.[^\.]*$', '.csv', filename)
    else:
        dlurl = server + '/access/datafile/' + str(fileid)
    fullpath = filename
    md5 = obj["dataFile"]["md5"]    # check if file already exists
    if os.path.isfile(fullpath) is True:
        hash = hashlib.md5()
        with open(str(fullpath), 'rb') as afile:
            buf = afile.read()
            hash.update(buf)
            prevmd5 = hash.hexdigest()
            if md5 == prevmd5: # exists and checksum match
                    print("MD5 match: " + fullpath)
                    continue
            else: # exists and corrupt
                    curl_files(dlurl, fullpath, fileid, 0)
    else: # doesn't exist
        curl_files(dlurl, fullpath, fileid, 0)

from os import path
if not path.exists("run_log_ds.csv"): # to check if no files had checksum error
    with open('run_log_ds.csv', 'a') as out_file:
        out_file.write("{},all,ok\n".format(directory))