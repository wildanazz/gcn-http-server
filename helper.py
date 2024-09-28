import os
import uuid
import logging
import boto3
# from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()


def write_to_temp(npz_file):
    # Ensure the upload directory exists
    os.makedirs('temp', exist_ok=True)

    with open(os.path.join('temp', 'data.npz'), 'wb') as f:
        f.write(npz_file.file.read())


def upload_images():
    # Azure Storage
    # blob_service_client = BlobServiceClient.from_connection_string(
    #     os.getenv('CONNECTION_STRING'))

    # container_name = str(uuid.uuid4())

    # list_url = {}
    # for m in ["loss", "accuracy", "embeddings"]:
    #     blob_client = blob_service_client.get_blob_client(
    #         container=f"gcn/{container_name}", blob=f"{m}.png")

    #     with open(file=f"./temp/{m}.png", mode="rb") as data:
    #         blob_client.upload_blob(data)
    #         list_url[m] = blob_client.url

    # return list_url

    # Spaces Object Storage
    try:
        # Initialize the session and client
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name = 'syd1',
                                endpoint_url = 'https://gcn.syd1.digitaloceanspaces.com',
                                aws_access_key_id=os.getenv('SPACES_KEY'),
                                aws_secret_access_key=os.getenv('SPACES_SECRET'))
        
        # Define a lifecycle policy to delete files after a certain number of days
        bucket_lifecycle_configuration = {
            'Rules': [
                {
                     'ID': 'AutoDeleteAfterXDays',
                     'Prefix': '',  # Apply to all files in the bucket
                     'Status': 'Enabled',
                     'Expiration': { 
                        'Days': 1  # Number of days after which files will be deleted
                     },
                },
            ]
        }
        
        # Apply the lifecycle policy to the bucket
        client.put_bucket_lifecycle_configuration(
            Bucket='plots',
            LifecycleConfiguration=bucket_lifecycle_configuration
        )

        # Create a unique container name
        folder_name = str(uuid.uuid4())

        # Create a list to store URLs
        file_urls = {}

        # Upload files and store the URLs in the list
        for m in ['loss', 'accuracy', 'embeddings']:
            file_name = f'./temp/{m}.png'
            key_name = f'{folder_name}/{m}.png'

            # Upload the file
            client.upload_file(Filename=file_name,
                               Bucket='plots',
                               Key=key_name,
                               )
            
            # Generate the presigned URL for the uploaded file
            file_url = client.generate_presigned_url('get_object',
                                             Params={'Bucket': 'plots', 'Key': key_name},
                                             ExpiresIn=3600)  # URL will expire in 1 hour
            
            # Append the URL to the list
            file_urls[m] = file_url

        return file_urls

    except Exception as e:
        pass
