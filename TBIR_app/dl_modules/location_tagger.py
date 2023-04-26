import requests

import pathlib
import json

from GPSPhoto import gpsphoto
from .utils import maybe_download_and_call

from django.conf import settings
try:
    # Try to fetch from Django app setting
    MAPS_API_KEY = settings.MAPS_API_KEY
except:
    # On failure, fetch .env file - usually required if django app is not set up
    # and this file as ran as a script
    import environ
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
    env = environ.Env()

    environ.Env.read_env(
        env_file=str(BASE_DIR / ".env")
    )
    MAPS_API_KEY = env("MAPS_API_KEY")


class LocationTagger:
    def __init__(self):
        pass

    def get_tags(self, image_path):
        meta = gpsphoto.getGPSData(image_path)
        loc_type = "establishment"
        url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
               f"location={meta['Latitude']:.5f}%2C{meta['Longitude']:.5f}&type={loc_type}&radius=1500&key={MAPS_API_KEY}")
        response = requests.request("GET", url, headers={}, data={})
        results = json.loads(response.text)["results"]
        if len(results) > 5:
            results = results[:5]
        return ", ".join([j["name"] for j in results])

    def __call__(self, path_or_url):
        return maybe_download_and_call(path_or_url, self.get_tags)


if __name__ == "__main__":
    tagger = LocationTagger()
    print(tagger("https://www.geoimgr.com/images/samples/england-london-bridge.jpg"))
