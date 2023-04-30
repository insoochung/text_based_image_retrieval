import os
import boto3
from django.shortcuts import render

from TBIR_app.searcher import Searcher
from TBIR_app.models import Photo

from django_project.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME

SEARCHER = Searcher()
S3_CLIENT = boto3.client("s3", region_name=AWS_S3_REGION_NAME,
                         aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def index(request):
    return render(request, "index.html")


def result(request):
    # print(request)
    search_args = {"query": request.GET["query"],
                   "caption_ratio": float(request.GET["caption_ratio"]),
                   "face_tags_ratio": float(request.GET["face_tags_ratio"]),
                   "geoloc_ratio": float(request.GET["geoloc_ratio"]),
                   "top_k": int(request.GET["top_k"])}
    result = SEARCHER.query(**search_args)

    ret = []
    for photo_dict in result:
        photo_obj = Photo.objects.get(id=photo_dict["id"])
        photo_dict["caption"] = photo_obj.caption
        photo_dict["names"] = photo_obj.names
        photo_dict["geolocation"] = photo_obj.geolocation
        ret.append((photo_obj.image_url, photo_dict))

    return render(request, "result.html", {"search_results": ret, "search_args": search_args})
