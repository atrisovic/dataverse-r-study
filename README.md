# A large-scale study on research code quality and execution

![](https://img.shields.io/badge/DOI-doi%3A10.7910%2FDVN%2FUZLXSZ-orange)

## Step 1. `get-dois` 

Code from `get-dois` enables communication with the Harvard Dataverse repository and collects DOIs of datasets that contain R code.

## Step 2. `aws-cli` 

The list of DOIs is used to define jobs for the AWS Batch. Code from `aws-cli` sends these jobs to the batch queue, where they will wait until resources become available for their execution.

## Step 3. `docker` 

When a job leaves the queue, it instantiates a pre-installed Docker image containing code to retrieve a replication package, executes R code, and collects data. Code from `docker` prepares the image.

## Step 4. `analysis` 

All collected data is retrieved and analyzed in `analysis`.

## Figure

![](https://i.imgur.com/DOBB1LI.jpeg)
