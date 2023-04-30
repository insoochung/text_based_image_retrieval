import os
from deepface import DeepFace

from .utils import maybe_download_and_call

NAME_TO_IDX = {
    "insoo": 0,
    "jinhyun": 1,
    "kwangkyu": 2,
    "youngki": 3,
    "unknown": 4,
}


class FaceTagger:
    def __init__(self, reference_dir=f"{os.path.dirname(__file__)}/references"):
        # self.embeddings, self.labels = load_reference_embeddings(reference_dir)
        self.reference_dir = reference_dir

    def tag_faces(self, input_image_path, threshold=float(2/3) - 1e-6):
        try:
            result = DeepFace.find(
                input_image_path, self.reference_dir, model_name="ArcFace", detector_backend="retinaface", enforce_detection=False)
            df = result[0]
            refs = [os.path.basename(fp).split(".")[0][:-1]
                    for fp in df["identity"].tolist()]
            if refs:
                for name in NAME_TO_IDX.keys():
                    if refs.count(name) / len(refs) >= threshold:
                        return [name]
        except (ValueError, AttributeError):
            pass

        return []

    def __call__(self, path_or_url):
        return maybe_download_and_call(path_or_url, self.tag_faces)


if __name__ == "__main__":
    print(FaceTagger()("/Users/insoochung/Desktop/test.jpeg"))
