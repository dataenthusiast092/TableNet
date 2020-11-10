from PIL import Image
import os

if __name__ == "__main__":
    directory = '../dataset/Marmot_data/'
    saveDirectory = '../dataset/image_files/' 

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        # Find all the bmp files
        if filename.endswith(".bmp"):
            filename = filename[:-4]

            image = Image.open(directory + filename + '.bmp')
            # https://www.geeksforgeeks.org/python-pil-image-convert-method/
            # https://pillow.readthedocs.io/en/stable/handbook/concepts.html
            image.convert('RGB')
            # https://auth0.com/blog/image-processing-in-python-with-pillow/
            resized_image = image.resize((1024, 1024))
            
            resized_image.save(saveDirectory + filename + ".jpeg")
