import os
import django
# Set the environment variable for the project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Configure Django settings
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from TBIR_app.models import Photo
import boto3
from boto3.s3.transfer import TransferConfig

from django_project.settings import AWS_STORAGE_BUCKET_NAME,AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,AWS_S3_REGION_NAME

photo_folder_path = 'CSCE670_unified_final'

def upload_image():
    s3 = boto3.client('s3', region_name=AWS_S3_REGION_NAME, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    for filename in os.listdir(photo_folder_path):
        if filename.endswith('.jpg'):
            #s3 = boto3.client('s3')
            file_path = f'{photo_folder_path}/{filename}'
            transfer_config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10, multipart_chunksize=1024*25, use_threads=True)
            s3.upload_file(file_path, AWS_STORAGE_BUCKET_NAME, filename, Config=transfer_config)
            image_url = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}'
            # Save the image URL, name caption to SQLite3 DB
            image_obj = Photo(names=filename, caption=filename, image_url=image_url)
            image_obj.save()
            # obj_list = s3.list_objects(Bucket = AWS_STORAGE_BUCKET_NAME)
            # content_list = obj_list['Contents']
            # for content in content_list:
            #     print(content)

upload_image()
