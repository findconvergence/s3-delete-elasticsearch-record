# s3-delete-elasticsearch-record
This Python 3.6 package for AWS Lambda deletes a record in AWS Elasticsearch when sent an 'ObjectDelete' event from an s3 bucket. 
* Set up "ObjectDelete" event triggers to this Lambda function from as many s3 buckets as you like. Can handle multiple staging environments.
* See the accompanying repo to **create records** as well.

## Thanks:
Credit to Amit Sharma (@amitksh44) for the [original scripts](https://aws.amazon.com/blogs/database/indexing-metadata-in-amazon-elasticsearch-service-using-aws-lambda-and-python/) in Python 2.7.  This update allows you to use Python 3.6 and the latest Elasticsearch build to keep a dynamic catalog of your Data Lake objects in AWS S3.  

## Requirements:
* AWS S3 bucket
* AWS Lambda 
* AWS Elasticsearch endpoint

## Configuration 
* First time packaging a Python script for Lambda?  [Read this guide.](https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/)
* Update your AWS Lambda endpoint under *user constants* in **lambda_function.py** (Note the AWS default port for Elasticsearch is 80.)
* All required modules are currently included in the AWS Lambda environment, except for Elasticsearch. 
* If you need, `pip install elasticsearch -t .` inside the `delete-record` directory to update Elasticsearch locally (will install urllib as well.)
* Run `chmod -R 755` on the entire `delete-record` directory.
* Zip up the `delete-record` directory and upload file to your Lambda function.
