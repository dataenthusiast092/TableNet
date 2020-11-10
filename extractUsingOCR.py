import pytesseract
from PIL import Image
import os

if __name__ == "__main__":
    directory = '../dataset/image_files/'
    saveDirectory = '../dataset/text_files/' 
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        # Find all the bmp files
        if filename.endswith(".png"):
            filename = filename[:-4]

            image = Image.open(directory + filename + '.png')
            
            # https://stackabuse.com/pytesseract-simple-python-optical-character-recognition/
            text = pytesseract.image_to_string(image)
            
            with open(saveDirectory + filename + ".txt", 'w') as f:
                f.write(text)

            
    