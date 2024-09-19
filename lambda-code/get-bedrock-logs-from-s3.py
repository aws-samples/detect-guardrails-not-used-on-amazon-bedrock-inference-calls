import gzip
import boto3
import os

# Create an S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['bucket']
    object_key = event['key']

    # Fetch the object from S3
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        print(f"Error getting object {object_key} from bucket {bucket_name}. Make sure they exist and your bucket is in the same region as this function.")
        raise e

    # Check if the object is gzipped
    if response['ContentEncoding'] == 'gzip':
        # Unzip the object
        compressed_data = response['Body'].read()
        unzipped_data = gzip.decompress(compressed_data)
        return unzipped_data
    else:
        # Return the object content as a string
        return response['Body'].read().decode('utf-8')
