from urllib.parse import urlparse
from urllib.request import urlretrieve
from tempfile import TemporaryDirectory
from pathlib import Path

from geopy.geocoders import Nominatim
from GPSPhoto import gpsphoto

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

class AddressTagger:
    def __init__(self):
        self.tagger = Nominatim(user_agent="final_proj")
    
    def get_tag(self, image_path):
        meta = gpsphoto.getGPSData(image_path)
        location = self.tagger.reverse(f"{meta['Latitude']:.4f}, {meta['Longitude']:.4f}")
        return location.address


    def __call__(self, image_path):
        if is_url(image_path):
            image_url = image_path
            with TemporaryDirectory() as tempdir:
                # Temporarily download file
                image_path = str(Path(tempdir) / Path(image_url.split("/")[-1]))
                urlretrieve(image_url, image_path)
                res = self.get_tag(image_path)
            return res
        else:
            return self.get_tag(image_path)


if __name__ == "__main__":
    tagger = AddressTagger()
    print(tagger("https://www.geoimgr.com/images/samples/england-london-bridge.jpg"))