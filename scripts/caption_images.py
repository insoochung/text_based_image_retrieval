from utils import maybe_download
from PIL import UnidentifiedImageError
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # nopep8

import boto3
import tqdm
import django
from django_project.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from TBIR_app.models import Photo  # nopep8
from TBIR_app.dl_modules.caption_generator import CaptionGenerator  # nopep8


def caption_images(images_dir=os.path.join(os.path.dirname(__file__), "../static/images")):
    print("Captioning images...")
    s3_client = boto3.client("s3", region_name=AWS_S3_REGION_NAME,
                             aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    caption_gen = CaptionGenerator()
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for photo in tqdm.tqdm(Photo.objects.all()):
        # if photo.caption:
        #     continue
        image_path = maybe_download(
            s3_client, photo, images_dir, AWS_STORAGE_BUCKET_NAME)
        try:
            caption = caption_gen(image_path)
            tqdm.tqdm.write(f"{image_path.split('/')[-1]}: {caption}")
            photo.caption = caption
            photo.save()
        except UnidentifiedImageError:
            tqdm.tqdm.write(f"Failed to caption '{image_path}'")
            photo.caption = "<CANNOT_OPEN>"
            photo.save()


if __name__ == "__main__":
    caption_images()
