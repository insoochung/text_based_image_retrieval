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


def vectorize_image_attributes(hidden_size=768):
    print("Vectorizing image attributes...")
    text_vectorizer = TextVectorizer()

    for photo in tqdm.tqdm(Photo.objects.all()):
        if "<CANNOT_OPEN>" in photo.caption or not photo.caption.strip():
            photo.caption_vector = [0.0] * 768
        # else:
        #     photo.caption_vector = text_vectorizer(photo.caption).tolist()

        if "<CANNOT_OPEN>" in photo.geolocation or not photo.geolocation.strip():
            photo.geo_vector = [0.0] * 768
        # else:
        #     photo.geo_vector = text_vectorizer(photo.geolocation).tolist()
        photo.save()


if __name__ == "__main__":
    vectorize_image_attributes()
