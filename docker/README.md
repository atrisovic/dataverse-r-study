# Analysis environment

Building the Docker image:

```
docker build -t aws-image .
```

## Testing with existing image

Test the analysis workflow on a local computer with a single DOI:

```
docker pull atrisovic/aws-image
docker run -d --name=logtest -e DOI='doi:10.7910/DVN/VCFMBI' -e TEST='True' atrisovic/aws-image
# see what's happening in the container
docker attach logtest
docker rm logtest
```

On AWS, the image is executed as:

```
docker run -e DOI='doi:10.7910/DVN/VCFMBI' atrisovic/aws-image
```
