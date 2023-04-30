import numpy as np
import time
from sentence_transformers import SentenceTransformer


class TextVectorizer:
    def __init__(self, model="sentence-transformers/all-distilroberta-v1"):
        self.model = SentenceTransformer(model)

    def __call__(self, sentence):
        return self.model.encode([sentence])[0]


if __name__ == "__main__":
    model = TextVectorizer()
    start_time = time.time()
    result = model("I am a sentence")
    print(result)
    print(result.shape)
    end_time = time.time()
    timer = end_time - start_time
    print(timer)
