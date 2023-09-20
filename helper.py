import os
import uuid
import logging
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()


def write_to_temp(npz_file):
    # Ensure the upload directory exists
    os.makedirs('temp', exist_ok=True)

    with open(os.path.join('temp', 'data.npz'), 'wb') as f:
        f.write(npz_file.file.read())


def upload_images():
    logging.info('Uploading file...')

    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv('CONNECTION_STRING'))

    container_name = str(uuid.uuid4())

    list_url = {}
    for m in ["loss", "accuracy", "embeddings"]:
        blob_client = blob_service_client.get_blob_client(
            container=f"gcn/{container_name}", blob=f"{m}.png")

        with open(file=f"./temp/{m}.png", mode="rb") as data:
            blob_client.upload_blob(data)
            list_url[m] = blob_client.url

    return list_url
