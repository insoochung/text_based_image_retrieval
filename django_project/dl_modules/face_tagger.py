import os
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine


def generate_embeeddings_from_faces(reference_dir, subfolder):
    # Iterate through the subfolders in the main folder
    subfolder_path = os.path.join(reference_dir, subfolder)
    # Check if it is a folder
    if not os.path.isdir(subfolder_path):
        raise f"{subfolder_path} is not a directory"

    # Create a new folder for the npy files
    npy_folder = os.path.join(reference_dir, f"{subfolder}_npy")
    os.makedirs(npy_folder, exist_ok=True)

    # Iterate through the images in the subfolder
    for img_file in os.listdir(subfolder_path):
        img_file_path = os.path.join(subfolder_path, img_file)

        # Check if it is an image file (assuming jpg or png)
        if not img_file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        # Find face embedding
        try:
            embeddings = DeepFace.represent(
                img_file_path, model_name='VGG-Face', enforce_detection=False, detector_backend='opencv')
            if len(embeddings) > 1:
                print(
                    f"Warning: More than one face detected in {img_file}. Using the first detected face.")
                embedding = embeddings[0]['embedding']
            else:
                embedding = embeddings[0]['embedding']
        except ValueError:
            print(f"Unable to find a face in {img_file}")
            continue

        # Save the embedding as an npy file in the corresponding npy folder
        npy_file_name = os.path.splitext(img_file)[0] + '.npy'
        npy_file_path = os.path.join(npy_folder, npy_file_name)
        np.save(npy_file_path, embedding)


def load_reference_embeddings(reference_dir):

    # Load pre-calculated embeddings and their class labels
    embeddings = []
    labels = []

    for subfolder in os.listdir(reference_dir):
        subfolder_path = os.path.join(reference_dir, subfolder)

        if subfolder.endswith("_npy"):
            continue
        if not os.path.exists(subfolder_path + "_npy"):
            generate_embeeddings_from_faces(reference_dir, subfolder)

        for npy_file in os.listdir(subfolder_path + "_npy"):
            npy_file_path = os.path.join(subfolder_path + "_npy", npy_file)
            embedding = np.load(npy_file_path)
            embeddings.append(embedding)
            labels.append(subfolder)

    return embeddings, labels


class FaceTagger:
    def __init__(self, reference_dir="references"):
        self.embeddings, self.labels = load_reference_embeddings(reference_dir)

    def classify_image(self, input_image_path):
        # Calculate input image's face embedding
        input_embedding = DeepFace.represent(input_image_path, model_name='VGG-Face', enforce_detection=True,
                                             detector_backend='opencv')

        # Compare input image's embedding with pre-calculated embeddings
        similarities = [
            1 - cosine(np.array(input_embedding[0]['embedding']), emb) for emb in self.embeddings]

        # Find the top-5 most similar embeddings
        top_5_indices = np.argsort(similarities)[-5:]

        # Determine the class based on the majority of top-5 most similar embeddings
        top_5_classes = [self.labels[i] for i in top_5_indices]
        print("top_5_classes:", top_5_classes)
        predicted_class = max(set(top_5_classes), key=top_5_classes.count)

        return predicted_class
