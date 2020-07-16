#!/usr/bin/env python3
"Submit a job to AWS Batch."

import boto3

batch = boto3.client('batch')

import random
import time


with open('../get-dois/dataset_dois.txt') as fp:
   doi = fp.readline()
   i=0

   while doi:
       response = batch.submit_job(jobName='dvPY360'+''.join(str(random.randint(1,999))),
                       jobQueue='dataverse-queue',
                       jobDefinition='dataverse-job-def',
                       containerOverrides={
                           "environment": [
                               {"name": "DOI", "value": doi}
                           ]
                       })
   
       print("{} : Job ID is {}.".format(i, response['jobId']))

       i=i+1
       doi = fp.readline()

       if i % 502 == 0:
              time.sleep(1200)


