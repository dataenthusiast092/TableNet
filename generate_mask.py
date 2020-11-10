# Source: https://github.com/jainammm/TableNet

'''
Generate Comumn and Table mask from Marmot Data
'''

import xml.etree.ElementTree as ET
import os
import numpy as np
from PIL import Image

# Returns if columns belong to same table or not
def sameTable(ymin_1, ymin_2, ymax_1, ymax_2):
    min_diff = abs(ymin_1 - ymin_2)
    max_diff = abs(ymax_1 - ymax_2)

    if min_diff <= 5 and max_diff <=5:
        return True
    elif min_diff <= 4 and max_diff <=7:
        return True
    elif min_diff <= 7 and max_diff <=4:
        return True
    return False


if __name__ == "__main__":
    directory = '../dataset/Marmot_data/'
    final_col_directory = '../dataset/column_mask/'
    final_table_directory = '../dataset/table_mask/'

    for file in os.listdir(directory):
        
        # os.fsdecode() method in Python is used to decode the specified filename (contd.)
        # from the filesystem encoding with ‘surrogateescape‘ error handler,
        filename = os.fsdecode(file)
        # Find all the xml files
        
        if filename.endswith(".xml"):
            # negative indexing and starting to -4 is basically fining out the file name using negative indexing
            filename = filename[:-4]

            # Parse xml file
            tree = ET.parse('../dataset/Marmot/' + filename + '.xml')
            root = tree.getroot()
            size = root.find('size')

            # Parse width
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            # Create grayscale image array
            col_mask = np.zeros((height, width), dtype=np.int32)
            table_mask = np.zeros((height, width), dtype = np.int32)

            got_first_column = False
            
            i=0
            
            table_xmin = 10000
            table_xmax = 0

            table_ymin = 10000
            table_ymax = 0

            # basically object is all columns, and iterating over all columns to figure out each columns 
            # each column tag in xml has bndbox tag
            # each bndbox tag has xmin, ymin, xmax, ymax
            for column in root.findall('object'):
                bndbox = column.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                # colmask numpy array, iterate ymin to ymax(top to bottom vertical coordinates)
                # colmask numpy array, iterate xmin to xmax(left to right horizontal coordinates)
                # column color set to 255 color code which is white color
                col_mask[ymin:ymax, xmin:xmax] = 255
                  
                # ===========DONE===============    
                # if we get first column
                if got_first_column:
                    # if we're in the same table as of the first column, then
                    if sameTable(prev_ymin, ymin, prev_ymax, ymax) == False:
                        # increment i
                        i+=1
                        # then set first column to false
                        got_first_column = False
                        
                        # ymin:ymax=height and xmin:xmax=width is getting set to white color basically 255
                        table_mask[table_ymin:table_ymax, table_xmin:table_xmax] = 255
                        
                        
                        #
                        table_xmin = 10000
                        table_xmax = 0

                        table_ymin = 10000
                        table_ymax = 0
                        
                if got_first_column == False:
                    got_first_column = True
                    first_xmin = xmin
                    
                prev_ymin = ymin
                prev_ymax = ymax
                
                table_xmin = min(xmin, table_xmin)
                table_xmax = max(xmax, table_xmax)
                
                table_ymin = min(ymin, table_ymin)
                table_ymax = max(ymax, table_ymax)

            # setting table's ymin to ymax = height and xmin to xmax=width to white color number
            table_mask[table_ymin:table_ymax, table_xmin:table_xmax] = 255

            # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
            # L is basically 8 bit pixel(black & white)
            im = Image.fromarray(col_mask.astype(np.uint8),'L')
            im.save(final_col_directory + filename + ".jpeg")

            im = Image.fromarray(table_mask.astype(np.uint8),'L')
            im.save(final_table_directory + filename + ".jpeg")
