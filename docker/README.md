# Testing

Test workflow on a local computer:

```
docker pull atrisovic/aws-image
docker run -d --name=logtest -e DOI='doi:10.7910/DVN/VCFMBI' aws-image
# see what's happening in the container
docker attach logtest
docker rm logtest
```