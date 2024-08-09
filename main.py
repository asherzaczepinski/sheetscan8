#it should also scan rythms with that orchestra thingy i used to have that could do that and like outline it then the students could record themselves clapping to it
#once this was done i would try to sell it to the districts
#make it so for every note it will go back and associate exactly the outline of it!
#eventually put in alternate fingerings

#---- i would then start selling bulk packages to districts
#the idea would be the teachers search of enter in pdfs for each studnets thing
#the students go onto website and use the class code for all there different music
#it could be clarinet trombone you name it
#it would put it in and let the students work w/ it
#read up: https://github.com/AbdallahHemdan/Orchestra
#don't need full outline lit just need its results!
#dev the spacebar tapping interface

#maybe use pre-combined everything logic for testing!
#for each note we'll store a max top max bottom max left max right return it w/ this along w what type of note it is
#using this we can make it super accurately outlined for the user clicking the notes!

#if to things r too close to each other on the same line choose the one on the right
#do for the line added back only the current loop y in that middle range!
#do something where we run it first w/ lines removed
#then we make sure that any new notes aren't inside overlapping notes
#then we see if the user clicks on something and it is double notes or what not we will 



# move onto the dashed white -- different logic
#for the white notes changed direction maybe do something where it like does changed direction but can't go change again!
#eventuallydo the thing where if the note is inside the notes then likes it's bad

from process_line import process_line

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

# Threshold for line to be considered as an initial staff line #
threshold = 0.6

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
def sort_notes(notes):
    sorted_notes = []
    for row in notes:
        sorted_row = sorted(row, key=lambda note: note[1][0][0])
        sorted_notes.append(sorted_row)
    return sorted_notes

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

#the issue is how it is processing it it is doing thE NON LINE ONES GODDAMN
def extract_highlighted_lines_and_columns_from_image_took_out(image_path, threshold=2/3):
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

    for row_index, row in enumerate(img_array):
        # Count non-white (in grayscale, white is 255) pixels in the row
        non_white_pixels = np.sum(row != 255)
        # Highlight the row if the count exceeds the threshold
        if non_white_pixels > (threshold * width):
            img_array[row_index: row_index + 1, 0: width] = 255
            if start_line == -1:
                start_line = row_index
        else:
            # If a line was started previously, add it to the list
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
    notes = []
    for group in invisible_lines:
        for [current_loop_y, new_y] in group:
            row_notes = []
            # Process the lines and get the notes
            current_dashed_whites, current_black_notes, current_white_notes = process_line(
                current_loop_y, img_array, width, difference_between_lines_for_line_drawing, 
                difference_between_lines, line_height, image_path
            )
            new_dashed_whites, new_black_notes, new_white_notes = process_line(
                new_y, img_array, width, difference_between_lines_for_line_drawing, 
                difference_between_lines, line_height, image_path
            )

            all_blacks_in_line = sorted(current_black_notes + new_black_notes, key=lambda note: note[0][0])
            all_whites_in_line = sorted(current_white_notes + new_white_notes, key=lambda note: note[0][0])
            all_dashed_whites_in_line = sorted(current_dashed_whites + new_dashed_whites, key=lambda note: note[0][0])

            index = 0

            while index < len(all_blacks_in_line):
                black_note = all_blacks_in_line[index]
                if index == len(all_blacks_in_line) - 1:
                    row_notes.append(['black', black_note])
                    break
                next_note = all_blacks_in_line[index + 1]
                
                if next_note[0][0] - black_note[0][0] < difference_between_lines:
                    #compare which ones y is greater it doesn't matter the x
                    if next_note[0][1] < black_note[0][1]:
                        row_notes.append(['black', black_note])
                    else:
                        row_notes.append(['black', next_note])
                    index += 1
                else:
                    row_notes.append(['black', black_note])
                index += 1
            
            index = 0

            while index < len(all_whites_in_line):
                white_note = all_whites_in_line[index]
                if index == len(all_whites_in_line) - 1:
                    row_notes.append(['white', white_note])
                    break
                next_note = all_whites_in_line[index + 1]
                if next_note[0][0] - white_note[0][0] < difference_between_lines:
                    if next_note[0][1] < white_note[0][1]:
                        row_notes.append(['white', white_note])
                    else:
                        row_notes.append(['white', next_note])
                    index += 1
                else:
                    row_notes.append(['white', white_note])
                index += 1

            index = 0

            while index < len(all_dashed_whites_in_line):
                dashed_white = all_dashed_whites_in_line[index]
                if index == len(all_dashed_whites_in_line) - 1:
                    row_notes.append(['dashed_white', dashed_white])
                    break
                next_note = all_dashed_whites_in_line[index + 1]
                if next_note[0][0] - dashed_white[0][0] < difference_between_lines:
                    if next_note[0][1] < dashed_white[0][1]:
                        row_notes.append(['dashed_white', dashed_white])
                    else:
                        row_notes.append(['dashed_white', next_note])
                    index += 1
                else:
                    row_notes.append(['dashed_white', dashed_white])
                index += 1
            notes.append(row_notes)

    past_notes = []
    
    for index, row in enumerate(notes):
        if index != 0:
            for index2, note in enumerate(row):
                note = note[1]
                for index3, past_note in enumerate(past_notes):
                    past_note = past_note[1]
                    #this is an example of a specific usecase when removing!
                    if abs(past_note[0][0] - note[0][0]) <= difference_between_lines:
                        if past_notes[index3][0] == 'black' and row[index2][0] != 'black':
                            notes[index - 1].pop(index3)
                            break
                        else:
                            notes[index].pop(index2)
                            break
        past_notes = row

    sorted_middles = sort_pairs(invisible_lines)

    notes = sort_notes(notes)
    new_notes = []
    for row in notes:
        past_note = -1
        for note in row:
            note = note[1]
            #sometimes they like encompass each other thats y abs like it could start before end later
            if past_note != -1 and abs(note[1][0] - past_note) < (difference_between_lines * 2 / 3):
                continue
            new_notes.append(note)
            past_note = note[1][0] 

    img = Image.fromarray(img_array)
    img.save(image_path)

    lines.append(image_path)
    all_rows.append(lines)

    #only return the extra stuff here bc this looks at everything so it feels better
    return new_notes, sorted_middles, difference_between_lines_for_line_drawing
    
def extract_highlighted_lines_and_columns_from_image_kept_in(image_path, threshold=2/3):
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
        non_white_pixels = np.sum(row != 255)
        # Highlight the row if the count exceeds the threshold
        if non_white_pixels > (threshold * width):
            if start_line == -1:
                start_line = row_index
        else:
            # If a line was started previously, add it to the list
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

    notes = []
    for group in invisible_lines:

        for [current_loop_y, new_y] in group:
            #i think it's not going all the way
            row_notes = []
            # Process the lines and get the notes
            current_dashed_whites, current_black_notes, current_white_notes = process_line(
                current_loop_y, img_array, width, difference_between_lines_for_line_drawing, 
                difference_between_lines, line_height, image_path
            )
            new_dashed_whites, new_black_notes, new_white_notes = process_line(
                new_y, img_array, width, difference_between_lines_for_line_drawing, 
                difference_between_lines, line_height, image_path
            )

            all_blacks_in_line = sorted(current_black_notes + new_black_notes, key=lambda note: note[0][0])
            all_whites_in_line = sorted(current_white_notes + new_white_notes, key=lambda note: note[0][0])
            all_dashed_whites_in_line = sorted(current_dashed_whites + new_dashed_whites, key=lambda note: note[0][0])

            index = 0

            while index < len(all_blacks_in_line):
                black_note = all_blacks_in_line[index]
                if index == len(all_blacks_in_line) - 1:
                    row_notes.append(['black', black_note])
                    break
                next_note = all_blacks_in_line[index + 1]
                
                if next_note[0][0] - black_note[0][0] < difference_between_lines:
                    #compare which ones y is greater it doesn't matter the x
                    if next_note[0][1] < black_note[0][1]:
                        row_notes.append(['black', black_note])
                    else:
                        row_notes.append(['black', next_note])
                    index += 1
                else:
                    row_notes.append(['black', black_note])
                index += 1
            
            index = 0

            while index < len(all_whites_in_line):
                white_note = all_whites_in_line[index]
                if index == len(all_whites_in_line) - 1:
                    row_notes.append(['white', white_note])
                    break
                next_note = all_whites_in_line[index + 1]
                if next_note[0][0] - white_note[0][0] < difference_between_lines:
                    if next_note[0][1] < white_note[0][1]:
                        row_notes.append(['white', white_note])
                    else:
                        row_notes.append(['white', next_note])
                    index += 1
                else:
                    row_notes.append(['white', white_note])
                index += 1

            index = 0

            while index < len(all_dashed_whites_in_line):
                dashed_white = all_dashed_whites_in_line[index]
                if index == len(all_dashed_whites_in_line) - 1:
                    row_notes.append(['dashed_white', dashed_white])
                    break
                next_note = all_dashed_whites_in_line[index + 1]
                if next_note[0][0] - dashed_white[0][0] < difference_between_lines:
                    if next_note[0][1] < dashed_white[0][1]:
                        row_notes.append(['dashed_white', dashed_white])
                    else:
                        row_notes.append(['dashed_white', next_note])
                    index += 1
                else:
                    row_notes.append(['dashed_white', dashed_white])
                index += 1
            notes.append(row_notes)

    past_notes = []
    
    for index, row in enumerate(notes):
        if index != 0:
            for index2, note in enumerate(row):
                note = note[1]
                for index3, past_note in enumerate(past_notes):
                    past_note = past_note[1]
                    #this is an example of a specific usecase when removing!
                    if abs(past_note[0][0] - note[0][0]) <= difference_between_lines:
                        if past_notes[index3][0] == 'black' and row[index2][0] != 'black':
                            notes[index - 1].pop(index3)
                            break
                        else:
                            notes[index].pop(index2)
                            break
        past_notes = row

    notes = sort_notes(notes)
    new_notes = []
    for row in notes:
        past_note = -1
        for note in row:
            note = note[1]
            #sometimes they like encompass each other thats y abs like it could start before end later
            if past_note != -1 and abs(note[1][0] - past_note) < (difference_between_lines * 2 / 3):
                continue
            new_notes.append(note)
            past_note = note[1][0] 

    img = Image.fromarray(img_array)
    img.save(image_path)

    lines.append(image_path)
    all_rows.append(lines)

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

#use this to find the new shit

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
pdf_path = "hello.pdf"
input_folder = "input"
new_input = 'new_input'

#to debug this we can try to see it proces both pages seperately from some old commits but literally it is showing it has everything there i think it is a probelm with combine
for filename in os.listdir(input_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        try:

            image_path = os.path.join(input_folder, filename)
            new_image_path = os.path.join(new_input, filename)
            # Load the image
            img = Image.open(image_path).convert("L")  # Convert to grayscale

            # Convert the PIL Image to a NumPy array
            img_array = np.array(img)

            return_extract_highlighted_lines_and_columns_from_image_took_out, sorted_middles, difference_between_lines_for_line_drawing = extract_highlighted_lines_and_columns_from_image_took_out(image_path)

            notes = find_and_combine_extra(return_extract_highlighted_lines_and_columns_from_image_took_out, extract_highlighted_lines_and_columns_from_image_kept_in(image_path))
            
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
                
            #img array might be regenerating idk some stupid shit is happening right here
            img = Image.fromarray(img_array)
            img.save(new_image_path)
        except IndexError as e:
            print(e) 