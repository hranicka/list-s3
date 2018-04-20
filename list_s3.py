#!/usr/bin/python

import boto3
import time
import config


# execute
def main():
    get_s3(config.aws_access_key, config.aws_secret_key, config.aws_region_name, config.s3_bucket_name)


# retrieve metadata about all buckets
def get_s3(aws_access_key, aws_secret_key, aws_region_name, s3_bucket_name):
    session = boto3.session.Session()

    boto_client = session.client(
        's3',
        region_name=aws_region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=''
    )

    get_s3_obj(boto_client, s3_bucket_name)


# get object metadata from the bucket
def get_s3_obj(boto_client, s3_bucket_name, continuation_token=''):
    params = {'Bucket': s3_bucket_name, 'FetchOwner': True, 'MaxKeys': 1000}
    if continuation_token:
        params['ContinuationToken'] = continuation_token

    bucket = boto_client.list_objects_v2(**params)

    # capture metadata about objects in bucket
    if 'Contents' in bucket:
        time_format = '%Y-%m-%d %H:%M:%S'

        for z in bucket['Contents']:
            size = str(z['Size'])
            file = str(z['Key'])
            storage_type = z['StorageClass']
            last_modified = z['LastModified']

            last_modified_unix = int(time.mktime(last_modified.timetuple()))
            last_modified_date = last_modified.strftime(time_format)

            # write the results to a list
            row = [s3_bucket_name, file, size, storage_type, last_modified_date, last_modified_unix]
            csv_line = ','.join(map(str, row))

            print(csv_line)

    # if there is a token, retrieve additional files by calling the script again
    if 'NextContinuationToken' in bucket:
        continuation_token = bucket['NextContinuationToken']
        get_s3_obj(boto_client, s3_bucket_name, continuation_token)


# execute
if __name__ == "__main__":
    main()
