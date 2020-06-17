import boto3
import csv
from datetime import datetime

import sys
doi = sys.argv[1]

session = boto3.session.Session(region_name= 'us-east-2')
dynamodb = session.resource('dynamodb')

# table 1: success or error
table1 = dynamodb.Table("run_log")

items = []
with open('run_log.csv') as csv_file:
	reader = csv.reader(csv_file)
	for rows in reader:
        	mydict = {
            		'doi':rows[0],
            		'filename':rows[1],
            		'error':rows[2],
			'date_time':datetime.now().isoformat()
        	}
        	items.append(mydict)
	print(items)


with table1.batch_writer() as batch:
	for item in items:
		batch.put_item(Item=item)


# table 2: checksum check
table2 = dynamodb.Table("run_log_ds")

items = []
with open('run_log_ds.csv') as csv_file:
	reader = csv.reader(csv_file)
	for rows in reader:
        	mydict = {
            		'doi':rows[0],
            		'fileid':rows[1],
            		'status':rows[2],
        	}
        	items.append(mydict)
	print(items)


with table2.batch_writer() as batch:
	for item in items:
		batch.put_item(Item=item)

# table 3: in file info
table3 = dynamodb.Table("run_log_st")

items = []
with open('run_log_st.csv') as csv_file:
	reader = csv.reader(csv_file)
	for rows in reader:
        	mydict = {
				    'doi':doi,
            		'comments_no':rows[0],
            		'dependen_no':rows[1],
            		'total_size':rows[2],
            		'list_of_all':rows[3],
        	}
        	items.append(mydict)
	print(items)


with table3.batch_writer() as batch:
	for item in items:
		batch.put_item(Item=item)


# table 4: in file info per file
table4 = dynamodb.Table("run_log_st1")

items = []
with open('run_log_st1.csv') as csv_file:
	reader = csv.reader(csv_file)
	for rows in reader:
        	mydict = {
				    'doi':doi,
					'filename':rows[0],
					'total_lines':rows[1],
            		'comments_no':rows[2],
            		'dep_no':rows[3],
					'func_no':rows[4],
					'test_no':rows[5],
					'class_no':rows[6],
					'encoding':rows[7],
					'confidence':rows[8]
        	}
        	items.append(mydict)
	print(items)

with table4.batch_writer() as batch:
	for item in items:
		batch.put_item(Item=item)
