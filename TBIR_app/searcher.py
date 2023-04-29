import numpy as np
from TBIR_app.models import Photo


class Searcher:
    def __init__(self):
        pass
        # self.caption_embedding = self.initialize_caption_embedding()
        # self.caption_embedding = self.initialize_caption_embedding()

    def initialize_caption_embedding(self):
        return []
        # embedding = []
        # for photo in Photo.objects.all():
        #     vec = photo.caption_vector
        #     embedding.append(np.array(vec))

        # return np.stack(embedding)

    def initialize_face_embedding(self):
        return []
        # embedding = []
        # for photo in Photo.objects.all():
        #     vec = photo.name_vector
        #     embedding.append(np.array(vec))

        # return np.stack(embedding)
