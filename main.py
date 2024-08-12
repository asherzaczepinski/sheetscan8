#fix the notes that aren't working!
#i think dashed white might be an issue w the in a row thingy



#the dashed white has that little bump
#for all the other stuff do u rly need to remove and replace everything like only the middle lines should be the ones getting split open
#need better side logic for those black notes


#keep grinding


#make a check for lines incase crescendos fuck things up
from return_notes import return_notes

from PIL import Image, ImageDraw
from pathlib import Path
import fitz  # PyMuPDF
import bisect

import numpy as np
import os

import argparse

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("inputfolder", help="Input Folder", nargs='?', default="input")

args = parser.parse_args()

all_rows = []

#for testing purposes only
def draw_example_rectangle(image_path, rect):
    # Validate rectangle coordinates
    if not all(isinstance(coord, (int, float)) for coord in rect):
        print(f"Invalid rectangle coordinates: {rect}")
        return

    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Draw each rectangle
    try:
        draw.rectangle(rect, fill=None, outline="black", width=1)
    except ValueError as e:
        print(f"Failed to draw rectangle {rect} on {image_path}: {e}")
        return

    # Save the image with rectangles
    img.save(image_path)


def sort_pairs(input_array):
    # Initialize an empty list to store the pairs
    pairs = []
    for sublist in input_array:
        pairs.extend(sublist)
    # Sort the pairs list by the first element of each pair
    pairs.sort(key=lambda x: x[0])
    # Calculate the middle value (rounded mean) for each pair and add to middle_values list
    middle_values = [round((pair[0] + pair[1]) / 2) for pair in pairs]
    return middle_values

def y_assigner(y_array, y):
    if not y_array:
        return None
    # Find the closest value using binary search
    pos = bisect.bisect_left(y_array, y)
    if pos == 0:
        return y_array[0]
    if pos == len(y_array):
        return y_array[-1]
    before = y_array[pos - 1]
    after = y_array[pos]
    if after - y < y - before:
        return after
    else:
        return before    

def extract_highlighted_lines_and_columns_from_image_took_out(pdf_path, input_folder, new_input, image_path):
    global all_rows
    open_pdf_into_input(pdf_path, input_folder, new_input)

    # Load the image
    img = Image.open(image_path).convert("L")  # Convert to grayscale

    # Convert the PIL Image to a NumPy array
    img_array = np.array(img)

    # Get image width
    width = img_array.shape[1]

    height = img_array.shape[0]

    # This will hold the lines found in the image
    lines = []

    # Variable to track the start of a line
    start_line = -1



    #edited out the tookout logic to take out oneline above for that light layer above!!!!
    for row_index, row in enumerate(img_array):
        # Count non-white (in grayscale, white is 255) pixels in the row
        consecutive = 0
        found_row = False
        for temp_x_index in range (width):
            temp_pixel = img_array[row_index, temp_x_index]
            if temp_pixel != 255:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive > 0.3 * width:
                found_row = True
        if found_row:
            img_array[row_index - 1: row_index + 1, 0: width] = 255
            if start_line == -1:
                start_line = row_index
        else:
            if start_line != -1:
                lines.append([0, start_line, width, row_index])
                start_line = -1  # Reset start_line

    #replace the part we took out
    for row in lines:
        upper_line_y = row[1] - 1
        bottom_line_y = row[3] 
        for x_index in range(width):
            if img_array[upper_line_y, x_index] != 255 and img_array[bottom_line_y, x_index] != 255:
                for y in range(upper_line_y + 1, bottom_line_y):
                    img_array[y, x_index] = 0
    
    invisible_lines = []

    #Space it in middle for line identification
    difference_between_lines_for_line_drawing = lines[1][1] - lines[0][1] 

    #difference between lines

    difference_between_lines = lines[1][1] - lines[0][3]

    #line height

    line_height = lines[0][3] - lines[0][1]

    #For note heights

    staff_white_range = (lines[len(lines) - 5][1] - lines[len(lines) - 6][1]) / 2 
    
    group = []

    temp_difference = -1

    for row_index in range(len(lines)):
        row = lines[row_index]
        current_y = row[1]
        if (row_index + 1) % 5 == 0:
            if row_index == len(lines) - 1:
                stopping_point = row[1]
                while stopping_point < height and stopping_point <= row[1] + staff_white_range:
                    stopping_point += round(temp_difference / 2)
                stopping_point -= round(temp_difference / 2)
            else:
                stopping_point = (row[1] + lines[row_index + 1][1]) / 2
            while current_y <= stopping_point:
                group.extend([[current_y, current_y + round(line_height / 2)]])
                current_y += round(temp_difference / 2)
            invisible_lines.append(group)
            group = []
        #this is on the first line of a staff and goes up 
        elif row_index % 5 == 0:
            temp_difference = lines[row_index + 1][1] - current_y
            if row_index == 0:
                stopping_point = row[1] 
                while stopping_point > 0 and stopping_point >= row[1] - staff_white_range:
                    stopping_point -= round(temp_difference / 2)
                stopping_point += round(temp_difference / 2)
            else:
                stopping_point = (row[1] + lines[row_index - 1][1]) / 2
            while current_y >= stopping_point:
                group.extend([[current_y, current_y + round(line_height / 2)]])
                current_y -= round(temp_difference / 2)
            for add_row_index in range(4): 
                future_line = lines[row_index + add_row_index + 1][1] 
                group.extend([[int((future_line + lines[row_index + add_row_index][1]) / 2), int((future_line + lines[row_index + add_row_index][1]) / 2) + round(line_height / 2)]])
                if add_row_index != 3:
                    group.extend([[future_line, future_line + round(line_height / 2)]])
    
    new_notes, all_rows = return_notes(invisible_lines, img_array, width, difference_between_lines_for_line_drawing, difference_between_lines, line_height, image_path, Image, all_rows, lines)

    sorted_middles = sort_pairs(invisible_lines)
    #only return the extra stuff here bc this looks at everything so it feels better
    return new_notes, sorted_middles, difference_between_lines_for_line_drawing
    
def extract_highlighted_lines_and_columns_from_image_kept_in(pdf_path, input_folder, new_input, image_path):
    global all_rows

    open_pdf_into_input(pdf_path, input_folder, new_input)

    # Load the image
    img = Image.open(image_path).convert("L")  # Convert to grayscale

    # Convert the PIL Image to a NumPy array
    img_array = np.array(img)

    # Get image width
    width = img_array.shape[1]

    # This will hold the lines found in the image
    lines = []

    # Variable to track the start of a line
    start_line = -1

    for row_index, row in enumerate(img_array):
        # Count non-white (in grayscale, white is 255) pixels in the row
        consecutive = 0
        found_row = False
        for temp_x_index in range (width):
            temp_pixel = img_array[row_index, temp_x_index]
            if temp_pixel != 255:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive > 0.3 * width:
                found_row = True
        if found_row:
            if start_line == -1:
                start_line = row_index
        else:
            if start_line != -1:
                lines.append([0, start_line, width, row_index])
                start_line = -1  # Reset start_line
  
    #theres going to be way too many lines this way
    #replace the part we took out
    for row in lines:
        upper_line_y = row[1] - 1
        bottom_line_y = row[3] 
        for x_index in range(width):
            if img_array[upper_line_y, x_index] != 255 and img_array[bottom_line_y, x_index] != 255:
                for y in range(upper_line_y + 1, bottom_line_y):
                    img_array[y, x_index] = 0
    
    invisible_lines = []

    #Space it in middle for line identification

    difference_between_lines_for_line_drawing = lines[1][1] - lines[0][1] 

    #difference between lines

    difference_between_lines = lines[1][1] - lines[0][3]

    #line height

    line_height = lines[0][3] - lines[0][1]

    #For note heights

    staff_white_range = (lines[len(lines) - 5][1] - lines[len(lines) - 6][1]) / 2 
    
    group = []
    
    temp_difference = -1

    #Going to work on the removal of the every other line HERE!!!!
    for row_index in range(len(lines)):
        row = lines[row_index]
        current_y = row[1]
        if row_index % 5 == 0:
            #Going to work on the removal of the every other line HERE!!!!
            temp_difference = lines[row_index + 1][1] - current_y
            if row_index == 0:
                stopping_point = row[1] 
                while stopping_point > 0 and stopping_point >= row[1] - staff_white_range:
                    stopping_point -= round(temp_difference / 2)
                stopping_point += round(temp_difference / 2)
            else:
                stopping_point = (row[1] + lines[row_index - 1][1]) / 2
            #before first
            group.extend([[current_y - round(temp_difference / 2), current_y - round(temp_difference / 2) + round(line_height / 2)]])
            last_line = -1
            for add_row_index in range(4): 
                future_line = lines[row_index + add_row_index + 1][1] 
                last_line = future_line
                group.extend([[int((future_line + lines[row_index + add_row_index][1]) / 2), int((future_line + lines[row_index + add_row_index][1]) / 2) + round(line_height / 2)]])
                if add_row_index != 3:
                    group.extend([[future_line, future_line + round(line_height / 2)]])
            #after first
            #make it draw the lines
            group.extend([[last_line + round(temp_difference / 2), last_line + round(temp_difference / 2) + round(line_height / 2)]])
            invisible_lines.append(group)
            group = []

    new_notes, all_rows = return_notes(invisible_lines, img_array, width, difference_between_lines_for_line_drawing, difference_between_lines, line_height, image_path, Image, all_rows, lines)

    return new_notes

def open_pdf_into_input(pdf_path, input_folder, new_input):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Ensure input folder exists
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(new_input, exist_ok=True)

    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Render page to a pixmap (an image) at 300 DPI
        pix = page.get_pixmap(dpi=300)
        
        # Convert the pixmap to a PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save the image to a file
        image_path = os.path.join(input_folder, f"page_{page_num + 1}.png")
        image_path2 = os.path.join(new_input, f"page_{page_num + 1}.png")
        if not os.path.exists(os.path.dirname(image_path2)):
            os.makedirs(os.path.dirname(image_path2))
        img.save(image_path)

def find_and_combine_extra(arr1, arr2):
    # Convert each sub-array and inner lists to a tuple for hashability
    set1 = {tuple(map(tuple, sub_array)) for sub_array in arr1}
    set2 = {tuple(map(tuple, sub_array)) for sub_array in arr2}

    # Find the elements in arr2 that are not in arr1
    extra_in_arr2 = set2 - set1

    # Convert the extra elements back to lists of lists and combine with arr1
    result = arr1 + [list(map(list, item)) for item in extra_in_arr2]

    return result

# Example usage
pdf_path = "testingnewinput.pdf"
input_folder = "input"
new_input = 'new_input'



#need to open this somehow
open_pdf_into_input(pdf_path, input_folder, new_input)

for filename in os.listdir(input_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        try:
            image_path = os.path.join(input_folder, filename)

            new_image_path = os.path.join(new_input, filename)
            # Load the image
            img = Image.open(image_path).convert("L")  # Convert to grayscale

            # Convert the PIL Image to a NumPy array
            img_array = np.array(img)

            took_out, sorted_middles, difference_between_lines_for_line_drawing = extract_highlighted_lines_and_columns_from_image_took_out(pdf_path, input_folder, new_input, image_path)

            kept_in = extract_highlighted_lines_and_columns_from_image_kept_in(pdf_path, input_folder, new_input, image_path)

            notes = find_and_combine_extra(took_out, kept_in)
            
            for note in notes:
                top_left = note[0]
                bottom_right = note[1]
                assigned_value = y_assigner(sorted_middles, top_left[1] + (round(difference_between_lines_for_line_drawing / 2) - 1))
                top_left[1] = assigned_value - (round(difference_between_lines_for_line_drawing / 2) - 1)
                bottom_right[1] = assigned_value + (round(difference_between_lines_for_line_drawing / 2) - 1)
                #right side
                img_array[top_left[1] - 5: bottom_right[1] + 5, bottom_right[0] + 5] = 0
                #left side
                img_array[top_left[1] - 5: bottom_right[1] + 5, top_left[0] - 5] = 0
                #top side
                img_array[top_left[1] - 5, top_left[0] - 5:bottom_right[0] + 5] = 0
                #bottom side
                img_array[bottom_right[1] + 5, top_left[0] - 5:bottom_right[0] + 5] = 0  
                
            img = Image.fromarray(img_array)
            img.save(new_image_path)
        except IndexError as e:
            print(e) 