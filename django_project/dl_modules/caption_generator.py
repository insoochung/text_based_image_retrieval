from transformers import pipeline


class CaptionGenerator:
    def __init__(self, model="nlpconnect/vit-gpt2-image-captioning"):
        self.model = pipeline("image-to-text", model=model)

    def __call__(self, image_path):
        """Pass image paths in a list of strings to generate captions.
        """
        return self.model(image_path)


if __name__ == "__main__":
    model = CaptionGenerator()
    print(model("https://ankur3107.github.io/assets/images/image-captioning-example.png"))
