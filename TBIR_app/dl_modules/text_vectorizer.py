import numpy as np
import time
from transformers import pipeline
from transformers import AutoTokenizer

class TextVectorizer:
    def __init__(self, model="google/bert_uncased_L-4_H-256_A-4"):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = pipeline("feature-extraction", model=model, tokenizer=model)

    def __call__(self, sentence):
        return np.array(self.model(sentence)[0][0]) # Return representation of the first token.
    
if __name__ == "__main__":
    model = TextVectorizer()
    start_time = time.time()
    print(model("I am a sentence"))
    end_time = time.time()
    timer = end_time - start_time
    print(timer)