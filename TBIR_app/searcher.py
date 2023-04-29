import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # nopep8

import django
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from TBIR_app.models import Photo  # nopep8


class Searcher:
    def __init__(self):
        self.caption_embedding = self.initialize_caption_embedding()

    def initialize_caption_embedding(self):
        embedding = []
        for photo in Photo.objects.all():
            vec = photo.caption_vector
            print(vec)
            embedding.append(np.array(vec))

        return np.stack(embedding)

    def initialize_face_embedding(self):
        return []


if __name__ == "__main__":
    searcher = Searcher()
    searcher.initialize_caption_embedding()
