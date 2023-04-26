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
from TBIR_app.dl_modules.face_tagger import FaceTagger  # nopep8

NAME_TO_IDX = {
    "insoo": 0,
    "jinhyun": 1,
    "kwangkyu": 2,
    "youngki": 3,
    "unknown": 4,
}


def tag_names(images_dir="images"):
    print("Tagging images...")
    s3_client = boto3.client("s3", region_name=AWS_S3_REGION_NAME,
                             aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    tagger = FaceTagger()
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for photo in tqdm.tqdm(Photo.objects.all()):
        if photo.names:
            continue

        image_path = maybe_download(
            s3_client, photo, images_dir, AWS_STORAGE_BUCKET_NAME)
        try:
            names = list(set(tagger(image_path)))
            if not names:
                names = ["unknown"]
            tqdm.tqdm.write(f"{image_path.split('/')[-1]}: {names}")
            photo.names = ",".join(names)
            photo.name_vector = [0] * len(NAME_TO_IDX)
            for name in names:
                photo.name_vector[NAME_TO_IDX[name.lower()]] = 1
            photo.save()
        except UnidentifiedImageError:
            tqdm.tqdm.write(f"Failed to tag names for '{image_path}'")


if __name__ == "__main__":
    tag_names()
