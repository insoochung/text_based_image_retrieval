import os


def maybe_download(s3_client, photo, images_dir, bucket_name):
    image_name = photo.image_url.split("/")[-1]
    image_path = f"{images_dir}/{image_name}"
    if not os.path.exists(image_path):
        s3_client.download_file(
            bucket_name, image_name, image_path)
    return image_path
