# PEPSE: PErsonal Photo Search Engine

*Conducted as a part of class project in CSCE670 at Texas A&M*

Most commercial photo libraries provide tag-based search functions (i.g. faces, geolocation), but this isn't enough to find your photos that got deeply buried into the tens of thousands of photos you took. Consider the following situation:

![](./images/intro.png)

In this project, we use image captioning and their vector representations (feat. huggingface LMs), to help find your photo.

## Demo

[![](./images/thumbnail.png)](https://youtu.be/ZiI4mklxKoY)

# Quick start

1. Install dependencies.
2. Migrate django table.
3. Set up an AWS S3 bucket.
4. Use scripts in `scripts/` to populate your DB.
    - Execute in the order of:
        - `preprocess_images.py`
        - `upload_images.py`
        - `tag_names.py`
        - `caption_images.py`
        - `vectorize_image_attributes.py`
5. Run server and enjoy!

# Approach

**Data Collection**
1) Our team members gathered 1,500 images, contributing approximately 300-400 each. We preprocessed these images by eliminating redundant spaces in their filenames and standardizing their extensions to .jpg. 
2) For face tagging, we each provided nine selfie images in various lights and angles, which were used as ground truth for face tagging.

**Pretrained model**
1) Salesforce/blip-image-captioning-large is utilized for generating image captions.
2) sentence-transformers/all-distilroberta-v1 is used for creating query embeddings/vectors.
3) DeepFace is used to extract facial embeddings.

**Faces matching**
1) We prepared reference face images of ourselves (Insoo, Kwangkyu, Youngki, Jinhyun) and precomputed face embeddings
2) Face bounding boxes are identified from images, and from them, face embeddings are computed (offline inference)
3) Distances between embeddings are used to determine whose face it is then face tags are attached to the images (offline inference).
4) Names are identified from user queries to compute face tag score!

# Results

[Website](https://sites.google.com/tamu.edu/pepse)
