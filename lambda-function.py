import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 's3-cleanup-demo-indu'  # change this

def lambda_handler(event, context):
    
    time_threshold = datetime.now(timezone.utc) - timedelta(minutes=30)
    
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' not in response:
        print("No files found")
        return
    
    for obj in response['Contents']:
        file_name = obj['Key']
        last_modified = obj['LastModified']
        
        # Check if file is older than threshold
        if last_modified < time_threshold:
            print(f"Deleting file: {file_name}")
            
            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=file_name
            )
        else:
            print(f"Keeping file: {file_name}")
