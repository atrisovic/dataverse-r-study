# A large-scale Dataverse analysis

## Step 1. `get-dois` 

Code from `get-dois` enables communication with Harvard Dataverse repository and collects DOIs of datasets that contain R code.

## Step 2. `docker` 

Code from `docker` prepares the Docker image, which will download each dataset, conduct the analysis and save a result.

Step 3. `aws-cli` 

Code from `aws-cli` starts jobs on AWS Batch.

Step 4. `analysis` 

Code for result analysis.
