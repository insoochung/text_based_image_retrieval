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
from TBIR_app.dl_modules.text_vectorizer import TextVectorizer  # nopep8


def standardize(scores):
    _max = np.max(scores)
    _min = np.min(scores)
    return (scores - _min) / (_max - _min)  # force min to 0 and max to 1


class Searcher:
    def __init__(self):
        self.caption_embedding = self.initialize_caption_embedding()
        self.faceref_embedding = self.initialize_face_embedding()

    def initialize_caption_embedding(self):
        embedding = []
        ids = []
        for photo in Photo.objects.all():
            caption_vector = np.array(photo.caption_vector)
            embedding.append(caption_vector)
            ids.append(photo.id)

        assert ids == list(range(1, len(Photo.objects.all()) + 1))
        embedding = np.array(embedding)

        return embedding

    def initialize_face_embedding(self):
        embedding = []
        ids = []
        for photo in Photo.objects.all():
            name_vector = np.array(photo.name_vector)
            embedding.append(name_vector)
            ids.append(photo.id)

        assert ids == list(range(1, len(Photo.objects.all()) + 1))
        embedding = np.array(embedding)
        return embedding

    def query_caption_score(self, query="two men under sky", metric="cos_sim"):
        # retrive model
        model = TextVectorizer()

        # captions
        caption_embedding = self.caption_embedding  # (N,256)
        # print(caption_embedding[:3])
        query_embedding = model(query)  # get embedding for query
        # print(query_embedding)
        # assert 0
        query_embedding = query_embedding.reshape((1, -1))  # (1,256)

        if metric == "cos_sim":
            cosine = cosine_similarity(
                caption_embedding, query_embedding.reshape(1, -1))
            # reshape cosine similarity array to (1503, 1)
            scores = cosine.reshape(-1, 1)
        else:
            scores = np.power(caption_embedding -
                              query_embedding, 2)  # (N, 256)
            scores = np.sum(scores, axis=1)  # (N)
            scores = standardize(scores)
            scores = 1 - scores
            scores = scores.reshape((-1, 1))  # (N, 1)
        return scores
        # assert 0
        # assert 0
        # print(scores.shape)
        # assert 0
        # assert 0, (caption_embedding.shape, query_embedding.shape)

        # calculate cosine similarity between caption embeddings and query embedding
        # cosine = cosine_similarity(
        #     caption_embedding, query_embedding.reshape(1, -1))
        # # reshape cosine similarity array to (1503, 1)
        # cosine = cosine.reshape(-1, 1)
        return scores

        # # get the top 25 cosine similarity indices
        # top_25_cosine_indices = reversed(
        #     np.argsort(cosine, axis=0)[-25:].flatten())
        # # get the top 25 cosine similarity values
        # top_25_cosine_values = cosine.take(top_25_cosine_indices)

        # return list(zip(top_25_cosine_indices, top_25_cosine_values))

    def query_face_score(self, query="insoo and jinhyun"):

        NAME_TO_IDX = {
            "insoo": 0,
            "jinhyun": 1,
            "kwangkyu": 2,
            "youngki": 3,
            "unknown": 4,
        }

        # initialize one-hot vector
        one_hot = np.zeros((5,))

        # loop through each name in NAME_TO_IDX and check if it appears in the query
        for name, idx in NAME_TO_IDX.items():
            if name in query:
                np.put(one_hot, idx, 1)

        # face refs
        facerefs = self.faceref_embedding

        intersection = np.logical_and(one_hot, facerefs)
        union = np.logical_or(one_hot, facerefs)

        intersection_count = np.sum(intersection, axis=1)
        union_count = np.sum(union, axis=1)

        iou = intersection_count / union_count
        iou = iou.reshape(-1, 1)  # reshape to (1503)
        return iou
        # # get the top 25 cosine similarity indices
        # top_25_iou_indices = reversed(np.argsort(iou, axis=0)[-25:].flatten())
        # # get the top 25 cosine similarity values
        # top_25_iou_values = iou.take(top_25_iou_indices)

        # return list(zip(top_25_iou_indices, top_25_iou_values))

    def query(self, query, caption_ratio=1.0, face_tags_ratio=0.2, top_k=25):
        scores = np.zeros(shape=(len(Photo.objects.all()), 1))
        if caption_ratio > 0:
            caption_scores = self.query_caption_score(query)  # 0~1
            # scores += standardize(caption_scores) * caption_ratio
            # print(caption_scores)
            scores += standardize(caption_scores) * caption_ratio
            # print(scores)
            # assert 0
        if face_tags_ratio > 0:
            face_scores = self.query_face_score(query)  # 0~1
            scores += standardize(face_scores) * face_tags_ratio
        scores = np.reshape(scores, (-1, 1))
        top_k_scores_indices = list(reversed(
            np.argsort(scores, axis=0)[-top_k:].flatten()))
        # get the top 25 cosine similarity values
        top_k_scores_values = scores.take(top_k_scores_indices)

        return list(zip(top_k_scores_indices, top_k_scores_values))


if __name__ == "__main__":
    searcher = Searcher()
    searcher.query_caption_score()
    searcher.query_face_score()
