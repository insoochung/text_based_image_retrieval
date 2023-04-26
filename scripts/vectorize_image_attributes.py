import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # nopep8

import tqdm
import django
from django_project.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from TBIR_app.models import Photo  # nopep8
from TBIR_app.dl_modules.text_vectorizer import TextVectorizer  # nopep8


def vectorize_image_attributes(images_dir="images"):
    print("Vectorizing image attributes...")
    text_vectorizer = TextVectorizer()

    for photo in tqdm.tqdm(Photo.objects.all()):
        if photo.caption_vector:
            continue
        if not photo.caption_vector:
            photo.caption_vector = text_vectorizer(photo.caption)
        photo.save()


if __name__ == "__main__":
    vectorize_image_attributes()
