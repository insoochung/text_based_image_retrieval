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
        self.ids = None
        self.caption_embedding = self.initialize_caption_embedding()
        self.geoloc_embedding = self.initialize_geoloc_embedding()
        self.faceref_embedding = self.initialize_face_embedding()
        self.text_vectorizer = TextVectorizer()

    def initialize_caption_embedding(self):
        embedding = []
        ids = []
        for photo in Photo.objects.all():
            caption_vector = np.array(photo.caption_vector)
            embedding.append(caption_vector)
            ids.append(photo.id)

        if not self.ids:
            self.ids = ids
        else:
            assert self.ids == ids

        embedding = np.array(embedding)
        return embedding

    def initialize_geoloc_embedding(self):
        embedding = []
        ids = []
        for photo in Photo.objects.all():
            geo_vector = np.array(photo.geo_vector)
            embedding.append(geo_vector)
            ids.append(photo.id)

        if not self.ids:
            self.ids = ids
        else:
            assert self.ids == ids

        embedding = np.array(embedding)
        return embedding

    def initialize_face_embedding(self):
        embedding = []
        ids = []
        for photo in Photo.objects.all():
            name_vector = np.array(photo.name_vector)
            embedding.append(name_vector)
            ids.append(photo.id)

        if not self.ids:
            self.ids = ids
        else:
            assert self.ids == ids

        embedding = np.array(embedding)
        return embedding

    def query_caption_score(self, query="two men under sky", metric="cos_sim"):
        # captions
        caption_embedding = self.caption_embedding  # (N,256)
        query_embedding = self.text_vectorizer(
            query)  # get embedding for query
        query_embedding = query_embedding.reshape((1, -1))  # (1,256)

        if metric == "cos_sim":
            cosine = cosine_similarity(
                caption_embedding, query_embedding.reshape(1, -1))
            # reshape cosine similarity array to (1503, 1)
            scores = cosine.reshape(-1, 1)
        else:  # inv_l2_dist
            scores = np.power(caption_embedding -
                              query_embedding, 2)  # (N, 256)
            scores = np.sum(scores, axis=1)  # (N)
            scores = standardize(scores)
            scores = 1 - scores
            scores = scores.reshape((-1, 1))  # (N, 1)
        return scores

    def query_geoloc_score(self, query="grand canyon", metric="inv_l2_dist"):
        # geolocs
        geoloc_embedding = self.geoloc_embedding  # (N,256)
        query_embedding = self.text_vectorizer(
            query)  # get embedding for query
        query_embedding = query_embedding.reshape((1, -1))  # (1,256)

        if metric == "cos_sim":
            cosine = cosine_similarity(
                geoloc_embedding, query_embedding.reshape(1, -1))
            # reshape cosine similarity array to (1503, 1)
            scores = cosine.reshape(-1, 1)
        else:  # inv_l2_dist
            scores = np.power(geoloc_embedding -
                              query_embedding, 2)  # (N, 256)
            scores = np.sum(scores, axis=1)  # (N)
            scores = standardize(scores)
            scores = 1 - scores
            scores = scores.reshape((-1, 1))  # (N, 1)
        return scores

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
            if name in query.lower():
                np.put(one_hot, idx, 1)

        # face refs
        facerefs = self.faceref_embedding

        intersection = np.logical_and(one_hot, facerefs)
        union = np.logical_or(one_hot, facerefs)

        intersection_count = np.sum(intersection, axis=1)
        union_count = np.sum(union, axis=1)

        iou = intersection_count / (union_count + 1e-6)
        iou = iou.reshape(-1, 1)  # reshape to (1503)
        return iou

    def query(self, query, caption_ratio=1.0, face_tags_ratio=0.2, geoloc_ratio=0.0, top_k=25):
        scores = np.zeros(shape=(len(Photo.objects.all()), 1))
        scores_dict = {}
        if caption_ratio > 0:
            caption_scores = self.query_caption_score(query)
            assert not np.any(np.isnan(caption_scores))
            caption_scores = standardize(caption_scores)
            scores_dict["caption_scores"] = caption_scores
            scores += caption_scores * caption_ratio
        if face_tags_ratio > 0:
            face_scores = self.query_face_score(query)
            assert not np.any(np.isnan(face_scores))
            face_scores = standardize(face_scores)
            scores_dict["face_tag_scores"] = face_scores
            scores += face_scores * face_tags_ratio
        if geoloc_ratio > 0:
            geoloc_scores = self.query_geoloc_score(query)
            assert not np.any(np.isnan(geoloc_scores))
            geoloc_scores = standardize(geoloc_scores)
            scores_dict["geoloc_scores"] = geoloc_scores
            scores += geoloc_scores * geoloc_ratio

        scores = np.reshape(scores, (-1, 1))
        top_k_scores_indices = list(reversed(
            np.argsort(scores, axis=0)[-top_k:].flatten()))

        ret = []
        for idx in top_k_scores_indices:
            meta = {}
            meta["id"] = self.ids[idx]  # increment 1 to match table ids
            meta["score"] = float(scores[idx])
            for key in scores_dict.keys():
                meta[key] = float(scores_dict[key][idx])
            ret.append(meta)

        return ret


if __name__ == "__main__":
    searcher = Searcher()
    searcher.query_caption_score()
    searcher.query_face_score()
