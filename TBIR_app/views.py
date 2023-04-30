import os
import boto3
from django.shortcuts import render
from TBIR_app.searcher import Searcher
from TBIR_app.models import Photo

from django_project.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME

SEARCHER = Searcher()
S3_CLIENT = boto3.client("s3", region_name=AWS_S3_REGION_NAME,
                         aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def maybe_download(s3_client, photo, images_dir, bucket_name):
    image_name = photo.image_url.split("/")[-1]
    image_path = f"{images_dir}/{image_name}"
    if not os.path.exists(image_path):
        s3_client.download_file(
            bucket_name, image_name, image_path)
    return image_path


def index(request):
    return render(request, 'index.html')


def result(request):
    query = request.GET['index']
    search_res = SEARCHER.query(query, face_tags_ratio=0.2)  # id, score
    print(search_res)
    print(type(search_res))
    for i, score in search_res:
        print(Photo.objects.get(id=int(i + 1)))
        print(score)
    # assert 0
    photos = [(Photo.objects.get(id=int(i + 1)), score)
              for (i, score) in search_res]
    photos_processed = []
    for photo, score in photos:
        maybe_download(
            S3_CLIENT, photo, f"{os.path.dirname(__file__)}/../static/images", AWS_STORAGE_BUCKET_NAME)
        print(photo.image_url)
        photos_processed.append(
            (f"static/images/{photo.image_url.split('/')[-1]}", score))

    return render(request, 'result.html', {'photos': photos_processed})
