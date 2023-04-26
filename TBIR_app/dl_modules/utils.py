import os
import tempfile
import pathlib
from urllib import request
from urllib import parse


def is_url(url):
    try:
        result = parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def maybe_download_and_call(path_or_url, fn):
    if is_url(path_or_url):
        # URL
        image_url = path_or_url
        with tempfile.TemporaryDirectory() as tempdir:
            # Temporarily download file
            filepath = str(
                pathlib.Path(tempdir) / pathlib.Path(image_url.split("/")[-1]))
            request.urlretrieve(image_url, filepath)
            if not os.path.exists(filepath):
                raise RuntimeError(f"No file downloaded to {filepath}")
            res = fn(filepath)
        return res

    # Path
    filepath = path_or_url
    if not os.path.exists(filepath):
        raise RuntimeError(f"No such file {filepath}")

    return fn(filepath)
