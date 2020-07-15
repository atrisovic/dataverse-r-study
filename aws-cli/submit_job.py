#!/usr/bin/env python3
"Submit a job to AWS Batch."

import boto3

batch = boto3.client('batch')

import random
import time


with open('../get-dois/dataset_dois.txt') as fp:
   doi = fp.readline()
   i=0
   #while doi:
   while i<600:
       if i<300:
          i=i+1
          doi = fp.readline()
          continue
       i=i+1
       response = batch.submit_job(jobName='dv'+''.join(str(random.randint(1,999))),
                       jobQueue='dataverse-queue',
                       jobDefinition='dataverse-job-def',
                       containerOverrides={
                           "environment": [
                               {"name": "DOI", "value": doi}
                           ]
                       })
   
       print("Job ID is {}.".format(response['jobId']))
       doi = fp.readline()


