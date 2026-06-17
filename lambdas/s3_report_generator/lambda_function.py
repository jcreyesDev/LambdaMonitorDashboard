import boto3
import math
from botocore.exceptions import ClientError
from pathlib import Path
from collections import Counter

def format_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return '0B'
    
    size_name = ('B', 'KB', 'MB', 'GB', 'TB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    pow = math.pow(1024, i)
    size = round(size_bytes / pow, 2)

    return f'{size} {size_name[i]}'

def lambda_handler(event, context):
    client = boto3.client('s3')
    bucket_name = event.get('bucket_name', '')

    try:
        paginator = client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)
        objects = []

        for page in pages:
            for obj in page.get('Contents', []):
                objects.append(obj)
        
        total_files = len(objects)
        size = sum(obj['Size'] for obj in objects)
        total_size = format_size(size)
        extensions = [Path(obj['Key']).suffix.lower() for obj in objects]
        by_type = dict(Counter(extensions))

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': {
                'error': e.response['Error']['Message']
            }
        }
    
    return {
        'statusCode': 200,
        'body': {
            "bucket": bucket_name,
            "total_files": total_files,
            "total_size": total_size,
            "by_type": by_type
        }
    }