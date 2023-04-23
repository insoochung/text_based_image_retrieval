from urllib import parse
from urllib import request
import requests

import tempfile
import pathlib
import json

from GPSPhoto import gpsphoto

from django.conf import settings
try:
    # Try to fetch from Django app setting
    MAPS_API_KEY = settings.MAPS_API_KEY
except:
    # On failure, fetch from local .env file
    import environ
    env = environ.Env()
    environ.Env.read_env()
    MAPS_API_KEY = env("MAPS_API_KEY")

def is_url(url):
    try:
        result = parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

class LocationTagger:
    def __init__(self):
        pass

    def get_tags(self, image_path):
        meta = gpsphoto.getGPSData(image_path)
        loc_type = "establishment"
        url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
               f"location={meta['Latitude']:.5f}%2C{meta['Longitude']:.5f}&type={loc_type}&radius=1500&key={MAPS_API_KEY}")
        response = requests.request("GET", url, headers={}, data={})
        return ", ".join([j["name"] for j in json.loads(response.text)["results"]])


    def __call__(self, image_path):
        if is_url(image_path):
            image_url = image_path
            with tempfile.TemporaryDirectory() as tempdir:
                # Temporarily download file
                image_path = str(
                    pathlib.Path(tempdir) / pathlib.Path(image_url.split("/")[-1]))
                request.urlretrieve(image_url, image_path)
                res = self.get_tags(image_path)
            return res
        else:
            return self.get_tags(image_path)


if __name__ == "__main__":
    tagger = LocationTagger()
    print(tagger("https://www.geoimgr.com/images/samples/england-london-bridge.jpg"))
