# list-s3

Lists all file objects stored in S3 bucket, including their sizes.


## Requirements

* python 3.6+
* pip
* boto3 package

## Installation

    cp config.py.dist config.py

Edit `config.py` and add your AWS credentials and S3 Bucket name.


## Usage

Run the script. 

    ./list_s3.py

Results of the scan are shown in stdout.


## Security

It is recommended to create a readonly AWS IAM account specifically for usage with this tool using a minimal amount of privileges.


## Credits

This tool is a fork of https://github.com/marekq/list-s3
