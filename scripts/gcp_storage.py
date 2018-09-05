# Imports the Google Cloud client library
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/PierreK/Desktop/Dev/Python/CanISnooze/can-i-hit-snooze-today/.env/gcp_creds.json"
print 'Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))

# Instantiates a client
storage_client = storage.Client()
bucket_name = "pkarpov-traffic-images"
destination_blob_name = "test-blob"
source_file_name = "./image_data/images/2018/08/fd10484b-fa1d-4df0-b394-431e17b9ec44.jpg"

# Creates the new bucket
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(source_file_name)

print('File {} uploaded to {}.'.format(
    source_file_name,
    destination_blob_name))
