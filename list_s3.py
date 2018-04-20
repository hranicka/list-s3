#!/usr/bin/python

import boto3
import time
import config


# execute
def main():
    get_s3(config.aws_acck, config.aws_seck, config.aws_region_name, config.s3_bname)


# retrieve metadata about all buckets
def get_s3(aws_acck, aws_seck, aws_region_name, s3_bname):
    global resu
    resu = []

    session = boto3.session.Session()

    sts_client = session.client(
        's3',
        region_name=aws_region_name,
        aws_access_key_id=aws_acck,
        aws_secret_access_key=aws_seck,
        aws_session_token=''
    )

    get_s3_obj(sts_client, s3_bname, '')


# get object metadata from the bucket
def get_s3_obj(sts_client, name, tok):
    if len(tok) > 0:
        b = sts_client.list_objects_v2(Bucket=name, FetchOwner=True, MaxKeys=1000, ContinuationToken=tok)
    else:
        b = sts_client.list_objects_v2(Bucket=name, FetchOwner=True, MaxKeys=1000)

    # capture metadata about objects in bucket
    if b.has_key('Contents'):
        timest = '%Y-%m-%d %H:%M:%S'

        for z in b['Contents']:
            size = str(z['Size'])
            skey = str(z['Key'])
            stor = z['StorageClass']
            fmod = z['LastModified']

            funix = int(time.mktime(fmod.timetuple()))
            fitim = fmod.strftime(timest)

            # write the results to a list
            x = [name, skey, size, stor, fitim, funix]
            y = ','.join(map(str, x))

            resu.append(y)
            print(y)

    # if there is a token, retrieve additional files by calling the script again
    if b.has_key('NextContinuationToken'):
        tok = b['NextContinuationToken']
        get_s3_obj(sts_client, name, tok)


# execute
if __name__ == "__main__":
    main()
