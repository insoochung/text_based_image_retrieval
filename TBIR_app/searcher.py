import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # nopep8

import django
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from TBIR_app.models import Photo  # nopep8
from dl_modules.text_vectorizer import TextVectorizer  # nopep8


class Searcher:
    def __init__(self):
        self.caption_embedding = self.initialize_caption_embedding()
        self.faceref_embedding = self.initialize_face_embedding()

    def initialize_caption_embedding(self):
        embedding = []
        for photo in Photo.objects.all():
            caption_vector = np.array(photo.caption_vector)
            embedding.append(caption_vector)
        embedding = np.array(embedding)

        return embedding

    def initialize_face_embedding(self):
        embedding = []
        for photo in Photo.objects.all():
            name_vector = np.array(photo.name_vector)
            embedding.append(name_vector)
        embedding = np.array(embedding)

        return embedding

    def query_caption_score(self):
        # retrive model
        model = TextVectorizer()

        # query
        your_query = "hello world"

        # captions
        caption_for_allimgs = self.initialize_caption_embedding()

        query_embedding = model(your_query)  # get embedding for your_query
        # calculate cosine similarity between caption embeddings and query embedding
        cosine = cosine_similarity(
            caption_for_allimgs, query_embedding.reshape(1, -1))
        # reshape cosine similarity array to (1503, 1)
        cosine = cosine.reshape(-1, 1)

        # get the top 25 cosine similarity indices
        top_25_cosine_indices = np.argsort(cosine, axis=0)[-25:].flatten()
        # get the top 25 cosine similarity values
        top_25_cosine_values = cosine.take(top_25_cosine_indices)

        return list(zip(top_25_cosine_indices, top_25_cosine_values))

    def query_face_score(self):

        NAME_TO_IDX = {
            "insoo": 0,
            "jinhyun": 1,
            "kwangkyu": 2,
            "youngki": 3,
            "unknown": 4,
        }

        # query
        your_query = "insoo and jinhyun"

        # initialize one-hot vector
        one_hot = np.zeros((5,))

        # loop through each name in NAME_TO_IDX and check if it appears in the query
        for name, idx in NAME_TO_IDX.items():
            if name in your_query:
                np.put(one_hot, idx, 1)

        # face refs
        facerefs = self.initialize_face_embedding()

        intersection = np.logical_and(one_hot, facerefs)
        union = np.logical_or(one_hot, facerefs)

        intersection_count = np.sum(intersection, axis=1)
        union_count = np.sum(union, axis=1)

        iou = intersection_count / union_count
        iou = iou.reshape(-1, 1)  # reshape to (1503, 1)

        # get the top 25 cosine similarity indices
        top_25_iou_indices = np.argsort(iou, axis=0)[-25:].flatten()
        # get the top 25 cosine similarity values
        top_25_iou_values = iou.take(top_25_iou_indices)

        return list(zip(top_25_iou_indices, top_25_iou_values))


if __name__ == "__main__":
    searcher = Searcher()
    searcher.initialize_caption_embedding()
    searcher.initialize_face_embedding()
    searcher.query_caption_score()
    searcher.query_face_score()
