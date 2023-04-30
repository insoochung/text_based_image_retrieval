import os
from urllib.request import urlretrieve
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class CaptionGenerator:
    def __init__(self, model="Salesforce/blip-image-captioning-large"):
        self.processor = BlipProcessor.from_pretrained(model)
        self.model = BlipForConditionalGeneration.from_pretrained(model)

    def __call__(self, image_path):
        """Pass image paths in a list of strings to generate captions.
        """
        if not os.path.exists(image_path):  # URL
            _image_path = f".tmp.{image_path.split('.')[-1]}"
            urlretrieve(image_path, _image_path)
            image_path = _image_path
        raw_image = Image.open(image_path).convert("RGB")
        inputs = self.processor(
            raw_image, "a photography of", return_tensors="pt")
        out = self.model.generate(**inputs)
        # [0]["generated_text"]
        return self.processor.decode(out[0], skip_special_tokens=True)


if __name__ == "__main__":
    model = CaptionGenerator()
    print(model("https://cdn.britannica.com/35/238335-050-2CB2EB8A/Lionel-Messi-Argentina-Netherlands-World-Cup-Qatar-2022.jpg"))
