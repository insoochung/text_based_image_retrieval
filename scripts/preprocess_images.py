import os
from PIL import Image
import pillow_heif


def preprocess_images(folder_path, output_folder, new_extension='jpg'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        # Check if the file is an image
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            try:
                # Rename the file by changing its extension
                output_path = os.path.join(
                    output_folder, f"{os.path.splitext(file)[0]}.{new_extension}")
                os.rename(file_path, output_path)
                print(f"Renamed {file} to {os.path.basename(output_path)}")
            except Exception as e:
                print(f"Error renaming {file}: {e}")
        elif file.lower().endswith('.heic'):
            try:
                hf = pillow_heif.read_heif(file_path)
                image = Image.frombytes(hf.mode, hf.size, hf.data, "raw")
                image.save(f"{output_folder}/{file.split('.')[0]}.jpg")
            except Exception as e:
                print(f"Error converting {file}: {e}")
        else:
            print(f"Skipping non-image file {file}")


if __name__ == "__main__":
    input_folder = "images_raw"
    output_folder = "images"
    preprocess_images(input_folder, output_folder)
