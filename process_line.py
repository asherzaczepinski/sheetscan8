from PIL import Image
import numpy as np

def process_line(input_y, img_array, width, difference_between_lines_for_line_drawing, difference_between_lines, line_height, image_path):
    black_notes = []
    white_notes = []
    dashed_whites = []
    black_count = 0
    difference_between_blacks = -1
    #white notes
    for x_index in range(width):
        pixel = img_array[input_y, x_index]
        if pixel != 255 and x_index != width - 1:
            black_count += 1
            if difference_between_blacks >= difference_between_lines_for_line_drawing * 0.4 and difference_between_blacks < difference_between_lines_for_line_drawing * 1.5:
                
                counter = 0
                white_note = True
                above = False
                below = False
                keep_going = True
                max_above = -1
                max_below = -1
                #quick up and down check
                while True:
                    temp_pixel_above = img_array[input_y - counter, x_index - int(difference_between_blacks / 2)]
                    temp_pixel_below = img_array[input_y + counter, x_index - int(difference_between_blacks / 2)]
                    if counter > difference_between_lines_for_line_drawing * 3 / 4:
                        #breaking around here
                        white_note = False
                        break
                    if temp_pixel_above != 255:
                        above = True
                    if temp_pixel_below != 255:
                        below = True
                    if above and below and counter < difference_between_lines_for_line_drawing * 3 / 4:
                        break
                    counter += 1
                if white_note:
                    first = -1
                    middle = -1
                    start = x_index - difference_between_blacks
                    end = x_index + 1
                    for new_x_index in range(start, end):
                        temp_y_above = input_y
                        temp_y_below = input_y
                        above_flag = False
                        below_flag = False
                        while temp_y_above > input_y - round(difference_between_lines_for_line_drawing * 3 / 4):
                            temp_pixel_above = img_array[temp_y_above, new_x_index]                                        
                            if temp_pixel_above != 255:
                                above_flag = True
                                break
                            temp_y_above -= 1
                        if above_flag == False:
                            white_note = False
                        if white_note:
                            while temp_y_below < input_y + round(difference_between_lines_for_line_drawing * 3 / 4):
                                temp_pixel_below = img_array[temp_y_below, new_x_index]                                            
                                if temp_pixel_below != 255:
                                    below_flag = True
                                    break
                                temp_y_below += 1
                            if below_flag == False:
                                white_note = False          

                    #need to now go up and down then across
                    if white_note:
                        for new_y_index in range(input_y - round(difference_between_lines_for_line_drawing / 2), input_y + round(difference_between_lines_for_line_drawing / 2)):
                            temp_x_right = x_index - int(difference_between_blacks / 2) + 1
                            temp_x_left = x_index - int(difference_between_blacks / 2) - 1
                            right_flag = False
                            left_flag = False
                            while temp_x_left > x_index - difference_between_blacks * 2:
                                temp_pixel_left = img_array[new_y_index, temp_x_left]
                                if temp_pixel_left != 255:
                                    left_flag = True
                                    break
                                temp_x_left -= 1
                            if left_flag == False:
                                white_note = False
                            if white_note:
                                while temp_x_right < x_index + difference_between_blacks:
                                    temp_pixel_right = img_array[new_y_index, temp_x_right]
                                    if temp_pixel_right != 255:
                                        right_flag = True
                                        break
                                    temp_x_right -= 1
                                if right_flag == False:
                                    white_note = False
                    #bottom left
                    continued = False
                    current_y = input_y
                    current_x = x_index - difference_between_blacks + 1
                    just_switched = False
                    if white_note:
                        while True:
                            temp_pixel = img_array[current_y, current_x]
                            if temp_pixel != 255:
                                if just_switched:
                                    break
                                continued = True
                                for new_y_index in range (input_y - difference_between_lines, input_y):
                                    if img_array[new_y_index, current_x] == 255:
                                        continued = False
                                        break
                                if not continued:
                                    for new_y_index in range (input_y, input_y + difference_between_lines):
                                        if img_array[new_y_index, current_x] == 255:
                                            continued = False
                                            break
                                        else:
                                            continued = True
                                if continued:
                                    break
                                #keep working here
                                current_y += 1
                                just_switched = True
                            else:
                                just_switched = False
                                current_x -= 1
                                if current_x < 1:
                                    white_note = False
                                    break
                    most_left = current_x
                    continued = False
                    current_y = input_y
                    current_x = x_index - 1
                    just_switched = False
                    if white_note:
                        while True:
                            temp_pixel = img_array[current_y, current_x]
                            if temp_pixel != 255:
                                if just_switched:
                                    break
                                continued = True
                                for new_y_index in range (input_y - difference_between_lines, input_y):
                                    if img_array[new_y_index, current_x] == 255:
                                        continued = False
                                        break
                                if not continued:
                                    for new_y_index in range (input_y, input_y + difference_between_lines):
                                        if img_array[new_y_index, current_x] == 255:
                                            continued = False
                                            break
                                        else:
                                            continued = True
                                if continued:
                                    break
                                #keep working here
                                current_y -= 1
                                just_switched = True
                            else:
                                just_switched = False
                                current_x += 1
                                if current_x > width - 2:
                                    white_note = False
                                    break
                    most_right = current_x
                    if most_right - most_left < difference_between_lines or most_right - most_left > difference_between_lines * 1.5:
                        white_note = False                
                    #this is just seeing the left and right at input y
                    left = -1
                    right = -1
                    left_x = x_index - difference_between_blacks - 1
                    while left_x > x_index - difference_between_blacks - 1 - difference_between_blacks:
                        temp_pixel = img_array[input_y, left_x]
                        if temp_pixel == 255:
                            left = left_x + 1
                            break
                        left_x -= 1
                    if left == -1:
                        white_note = False
                    if white_note:
                        for right_x in range (x_index + 1, x_index + difference_between_blacks):
                            temp_pixel = img_array[input_y, right_x]
                            if temp_pixel == 255:
                                right = right_x - 1
                                break
                        if right == -1:
                            white_note = False
                    if white_note:
                        went_here = False
                        past_temp_y_above = -1
                        past_temp_y_below = -1
                        #testing where it is here
                        start = x_index - difference_between_blacks + 1
                        end = x_index - 1
                        normal_white = True
                        changed_direction_above = 0
                        changed_direction_below = 0
                        
                        for new_x_index in range(start, end):
                            if not white_note:
                                break
                            temp_pixel = img_array[input_y, new_x_index]
                            if temp_pixel != 255:
                                continue
                            temp_y_above = input_y
                            temp_y_below = input_y
                            while True:
                                continued = True
                                for new_x_index2 in range(left - int(difference_between_lines / 4), right + int(difference_between_lines / 4)):
                                    if img_array[temp_y_above, new_x_index2] == 255:
                                        continued = False
                                        break
                                if continued:
                                    break
                                if temp_y_above <= input_y - round(difference_between_lines_for_line_drawing * 3 / 4):
                                    white_note = False
                                    break
                                temp_pixel_above = img_array[temp_y_above, new_x_index]       
                                if temp_pixel_above != 255:
                                    break
                                temp_y_above -= 1   
                             
                            if white_note:
                                if temp_y_above <= max_above or max_above == -1:
                                    max_above = temp_y_above
                                while True:
                                    continued = True
                                    for new_x_index2 in range(left - int(difference_between_lines / 4), right + int(difference_between_lines / 4)):
                                        if img_array[temp_y_below, new_x_index2] == 255:
                                            continued = False
                                            break
                                    if continued:
                                        break
                                    if temp_y_below >= input_y + round(difference_between_lines_for_line_drawing * 3 / 4):
                                        white_note = False
                                        break
                                    temp_pixel_below = img_array[temp_y_below, new_x_index]      
                                    if temp_pixel_below != 255:
                                        break
                                    temp_y_below += 1  
                            
                            if white_note:
                                if past_temp_y_below != -1:
                                    if past_temp_y_below - temp_y_below < 0:
                                        normal_white = False
                                if normal_white:
                                    if past_temp_y_above != -1:
                                        if past_temp_y_above - temp_y_above < 0:
                                            normal_white = False
                                #we may need to put something else here for those whole notes like that
                                if normal_white:
                                    if temp_y_below >= max_below:
                                        max_below = temp_y_below
                                    if new_x_index == start:
                                        first = round((temp_y_above + temp_y_below) / 2)
                                    elif new_x_index == round((start + end) / 2):
                                        middle = round((temp_y_above + temp_y_below) / 2)
                                        if first - middle < int(difference_between_lines / 10):
                                            white_note = False
                                            break
                                    elif new_x_index == end - 1:
                                        ending = round((temp_y_above + temp_y_below) / 2)
                                        if middle - ending < int(difference_between_lines / 10):
                                            white_note = False
                                            break        
                                    if abs((past_temp_y_above - temp_y_above) - (temp_y_below - past_temp_y_below)) < difference_between_lines / 10 and past_temp_y_above - temp_y_above >= 0 and temp_y_below - past_temp_y_below >= 0:
                                        past_temp_y_above = temp_y_above
                                        past_temp_y_below = temp_y_below
                                    elif past_temp_y_above == -1 or (abs(past_temp_y_above - temp_y_above) <= round(difference_between_lines / 5) and abs(past_temp_y_below - temp_y_below) <= round(difference_between_lines / 5)):
                                        past_temp_y_above = temp_y_above
                                        past_temp_y_below = temp_y_below
                                    else:
                                        white_note = False
                                        break
                                else:
                                    went_here = True
                                    if white_note and past_temp_y_above != -1:
                                        if changed_direction_above == 0: 
                                            #going up has to start in this way
                                            if past_temp_y_above - temp_y_above > 0:
                                                changed_direction_above = 1
                                            elif past_temp_y_above - temp_y_above != 0:
                                                white_note = False
                                        elif changed_direction_above == 1:
                                            #if it's going up make sure it starts going down
                                            if temp_y_above - past_temp_y_above > 0:
                                                changed_direction_above = 2
                                        else:
                                            if past_temp_y_above - temp_y_above > 0:
                                                white_note = False
                                    if white_note and past_temp_y_below != -1:
                                        if changed_direction_below == 0: 
                                            #<= bc of the below it can start straight too not only down
                                            if past_temp_y_below - temp_y_below <= 0:
                                                changed_direction_below = 1
                                            else:
                                                white_note = False
                                        elif changed_direction_below == 1:
                                            #if it's going down or straight make sure it starts going up
                                            if temp_y_below - past_temp_y_below < 0:
                                                changed_direction_below = 2
                                        else:
                                            if past_temp_y_below - temp_y_below < 0:
                                                white_note = False
                                    
                                    if abs((past_temp_y_above - temp_y_above) - (temp_y_below - past_temp_y_below)) < difference_between_lines / 10:
                                        past_temp_y_above = temp_y_above
                                        past_temp_y_below = temp_y_below
                                    elif past_temp_y_above == -1 or (abs(past_temp_y_above - temp_y_above) <= round(difference_between_lines / 2) and abs(past_temp_y_below - temp_y_below) <= round(difference_between_lines / 2)):
                                        past_temp_y_above = temp_y_above
                                        past_temp_y_below = temp_y_below
                                    else:
                                        white_note = False
                                        break
                                    if keep_going:




                                        #its in here
                                        middle = round((max_above + max_below) / 2)
                                        left_thickness = 0
                                        right_thickness = 0
                                        temp_x = x_index - round(difference_between_blacks / 2)
                                        started_mattering = -1
                                        while True:
                                            if temp_x < 0:
                                                white_note = False
                                                break
                                            temp_pixel = img_array[middle, temp_x]
                                            if started_mattering == -1:
                                                if temp_pixel != 255:
                                                    started_mattering = temp_x
                                            else:
                                                if temp_pixel == 255:
                                                    left_thickness = started_mattering - temp_x
                                                    break
                                            temp_x -= 1
                                        temp_x = x_index - round(difference_between_blacks / 2)
                                        started_mattering = -1
                                        while True:
                                            if temp_x > width - 1:
                                                white_note = False
                                                break
                                            temp_pixel = img_array[middle, temp_x]
                                            if started_mattering == -1:
                                                if temp_pixel != 255:
                                                    started_mattering = temp_x
                                            else:
                                                if temp_pixel == 255:
                                                    right_thickness = temp_x - started_mattering
                                                    break
                                            temp_x += 1
                                        
                                        if left_thickness < int(difference_between_lines / 4) or right_thickness < int(difference_between_lines / 4):
                                            white_note = False
                                            keep_going = False
                                        else:
                                            keep_going = False
                        if went_here:
                            white_note = False
                            if changed_direction_above == 2 or changed_direction_below == 2:
                                white_note = True
                        if white_note:
                            #in here

                            #little /5 cuz it is not all the way
                            if max_above > input_y - round(difference_between_lines / 10):
                                white_note = False
                            if white_note:
                                if max_below < input_y + round(difference_between_lines / 10):
                                    white_note = False
                            #overall height check
                            if white_note:
                                if max_below - max_above > difference_between_lines_for_line_drawing + line_height * 2:
                                    #not here
                                    white_note = False
                        if white_note:
                            top_left = [left - 5, input_y - 10]
                            bottom_right = [right + 5, input_y + 10]   
                            white_notes.append([top_left, bottom_right])
            
            difference_between_blacks = 0
        else:
            #if it's white
            if difference_between_blacks != -1:
                difference_between_blacks += 1
    
    
    black_count = 0
    #black and dashed white

    for x_index in range(width):
        pixel = img_array[input_y, x_index]
        if pixel != 255 and x_index != width - 1:
            black_count += 1
        elif black_count >= difference_between_lines_for_line_drawing * 1.15 and black_count < difference_between_lines_for_line_drawing * 5:
     
            changed_direction_above = 0
            changed_direction_below = 0

            #apply my logic to see if it is a black note
            middle_x = x_index - round(black_count / 2)
            black_note = True
            for add in range(1, round(difference_between_lines_for_line_drawing / 2) - 1 - round(line_height / 2)):
                above_pixel = img_array[input_y - add, middle_x]
                below_pixel = img_array[input_y + add, middle_x]
                if above_pixel == 255 or below_pixel == 255:
                    black_note = False
            max_above = -1
            max_below = -1

            if black_note:
                if black_count < difference_between_lines_for_line_drawing * 1.5:
                    past_temp_y_above = -1
                    past_temp_y_below = -1
                    for new_x_index in range(x_index - black_count + 1, x_index - 1):
                        temp_pixel = img_array[input_y, new_x_index]      
                        continued = True
                        for new_y_index in range (input_y - difference_between_lines, input_y):
                            if img_array[new_y_index, new_x_index] == 255:
                                continued = False
                                break
                        if not continued:
                            for new_y_index in range (input_y, input_y + difference_between_lines):
                                if img_array[new_y_index, new_x_index] == 255:
                                    continued = False
                                    break
                                else:
                                    continued = True
                        if continued:
                            continue 
                        temp_y_above = input_y
                        temp_y_below = input_y                  
                        while True:
                            continued = True
                            for new_x_index2 in range(x_index - black_count + 1 - int(difference_between_lines / 4), x_index - 1 + int(difference_between_lines / 4)):
                                if img_array[temp_y_above, new_x_index2] == 255:
                                    continued = False
                                    break
                            if continued:
                                break
                            if temp_y_above <= input_y - round(difference_between_lines_for_line_drawing * 3 / 4):
                                black_note = False
                                break
                            temp_pixel_above = img_array[temp_y_above, new_x_index]       
                            if temp_pixel_above == 255:
                                break
                            temp_y_above -= 1

                        #the black notes pass the test

                        if black_note and past_temp_y_above != -1:
                            if changed_direction_above == 0: 
                                #going up has to start in this way
                                if past_temp_y_above - temp_y_above > 0:
                                    changed_direction_above = 1
                                elif past_temp_y_above - temp_y_above != 0:
                                    black_note = False
                            elif changed_direction_above == 1:
                                #if it's going up make sure it starts going down
                                if temp_y_above - past_temp_y_above > 0:
                                    changed_direction_above = 2
                            else:
                                if past_temp_y_above - temp_y_above > 0:
                                    black_note = False

                        if black_note:
                            if temp_y_above <= max_above or max_above == -1:
                                max_above = temp_y_above
                            while True:
                                continued = True
                                for new_x_index2 in range(x_index - black_count + 1 - int(difference_between_lines / 4), x_index - 1 + int(difference_between_lines / 4)):
                                    if img_array[temp_y_below, new_x_index2] == 255:
                                        continued = False
                                        break
                                if continued:
                                    break
                                if temp_y_below >= input_y + round(difference_between_lines_for_line_drawing * 3 / 4):
                                    black_note =  False
                                    break                                
                                temp_pixel_below = img_array[temp_y_below, new_x_index]      
                                if temp_pixel_below == 255:
                                    break
                                temp_y_below += 1   

                        if black_note and past_temp_y_below != -1:
                            if changed_direction_below == 0: 
                                #<= bc of the below it can start straight too not only down
                                if past_temp_y_below - temp_y_below <= 0:
                                    changed_direction_below = 1
                                else:
                                    black_note = False
                            elif changed_direction_below == 1:
                                #if it's going down or straight make sure it starts going up
                                if temp_y_below - past_temp_y_below < 0:
                                    changed_direction_below = 2
                            else:
                                if past_temp_y_below - temp_y_below < 0:
                                    black_note = False

                        if black_note: 
                            if temp_y_below >= max_below:
                                max_below = temp_y_below                                   
                            left_zone = False
                            if not left_zone and new_x_index >= x_index - black_count + 1:
                                if new_x_index >= x_index - round(black_count / 2):
                                    left_zone = True
                                #gives exception of if it increases proportiately
                                elif abs((past_temp_y_above - temp_y_above) - (temp_y_below - past_temp_y_below)) < difference_between_lines / 10 and past_temp_y_above - temp_y_above >= 0 and temp_y_below - past_temp_y_below >= 0:
                                    past_temp_y_above = temp_y_above
                                    past_temp_y_below = temp_y_below
                                #have no past
                                elif past_temp_y_above == -1:
                                    past_temp_y_above = temp_y_above
                                    past_temp_y_below = temp_y_below
                                #slowly increasing
                                elif past_temp_y_above - temp_y_above <= round(difference_between_lines / 5) and past_temp_y_above - temp_y_above >= 0:
                                    if temp_y_below - past_temp_y_below <= round(difference_between_lines / 5) and temp_y_below - past_temp_y_below >= 0:
                                        past_temp_y_above = temp_y_above
                                        past_temp_y_below = temp_y_below
                                #not the correct note
                                else:
                                    black_note = False
                                    break
                            elif new_x_index <= x_index - 1:
                                if abs((temp_y_above - past_temp_y_above) - (past_temp_y_below - temp_y_below)) < difference_between_lines / 10 and temp_y_above - past_temp_y_above >= 0 and past_temp_y_below - temp_y_below >= 0:
                                    past_temp_y_above = temp_y_above
                                    past_temp_y_below = temp_y_below
                                elif temp_y_above - past_temp_y_above <= round(difference_between_lines / 5) and temp_y_above - past_temp_y_above >= 0:
                                    if past_temp_y_below - temp_y_below <= round(difference_between_lines / 5) and past_temp_y_below - temp_y_below >= 0:
                                        past_temp_y_above = temp_y_above
                                        past_temp_y_below = temp_y_below
                                else:
                                    black_note = False
                                    break
                    black_note = False
                    if changed_direction_above == 2 or changed_direction_below == 2:
                        black_note = True
                    if black_note:
                        if max_above > input_y - round(difference_between_lines_for_line_drawing / 2) + (line_height * 2):
                            black_note = False
                        if black_note:
                            if max_below < input_y + round(difference_between_lines_for_line_drawing / 2) - (line_height * 2):
                                black_note = False
                        if black_note:
                            if max_below - max_above > difference_between_lines_for_line_drawing + (line_height * 3):
                                black_note = False
                    if black_note:
                        top_left = [x_index - black_count, input_y - (round(difference_between_lines_for_line_drawing / 2) - 1)]
                        bottom_right = [x_index, input_y + (round(difference_between_lines_for_line_drawing / 2) - 1)]
                        black_notes.append([top_left, bottom_right])

                else:
                    #dashed black
                    changed_direction_above = 0
                    changed_direction_below = 0
                    starting_above_black = input_y 
                    starting_below_black = input_y 
                    past_temp_y_above = -1
                    past_temp_y_below = -1
                    temp_pixel_above = img_array[starting_above_black, x_index - black_count + 1]
                    temp_pixel_below = img_array[starting_below_black, x_index - black_count + 1]    
                    while temp_pixel_below != 255:
                        starting_below_black += 1
                        temp_pixel_below = img_array[starting_below_black, x_index - black_count + 1]
                    while temp_pixel_above != 255:
                        starting_above_black -= 1
                        temp_pixel_above = img_array[starting_above_black, x_index - black_count + 1]
                    start_up = -1
                    end_up = -1
                    if black_note:
                        found_black = False


                        #this change of check wouldn't be game changing tho that is the thing! it would jus make sure the start up shit was more accurate
                        for new_x_index in range(x_index - black_count + 1, x_index):
                            new_pixel = img_array[starting_above_black, new_x_index]
                            if new_pixel == 0 and not found_black:



                                #have to run a check here ot make sure it is not a column type shit

                                found_black = True
                                start_up = new_x_index
                            elif found_black:


                                
                                #also run a check here

                                #white and a black has been found
                                end_up = new_x_index - 1
                        if end_up - start_up < difference_between_lines / 5:
                            black_note = False
                    start_down = -1
                    end_down = -1
                    if black_note:
                        found_black = False
                        for new_x_index in range(x_index - black_count + 1, x_index):
                            new_pixel = img_array[starting_below_black, new_x_index]
                            if new_pixel == 0 and not found_black:


                                #same run a check here
                                found_black = True
                                start_down = new_x_index
                            elif found_black:


                                #same run a check here
                                end_down = new_x_index - 1
                        if end_down - start_down < difference_between_lines / 5:
                            black_note = False
                    max_above = -1
                    max_below = -1

                    start = max(start_up, start_down)
                    end = min(end_up, end_down)
                    
                    #testing distance!!!
                    if abs(start_up - start_down) > difference_between_lines / 4 or abs(end_up - end_down) > difference_between_lines / 4:
                        black_note = False
                    if max(end_up, end_down) - min(start_up, start_down) > difference_between_lines * 2.5:
                        black_note = False
                    if end - start <= difference_between_lines * 1.15:
                        black_note = False
                    if black_note:
                        #it meets it on edges
                        past_temp_y_above = -1
                        past_temp_y_below = -1
                        for new_x_index in range(start, end):
                            #both have to have at least one white    
                            continued = True
                            for new_y_index in range (starting_above_black - difference_between_lines, starting_above_black):
                                if img_array[new_y_index, new_x_index] == 255:
                                    continued = False
                                    break
                            if not continued:
                                for new_y_index in range (starting_below_black, starting_below_black + difference_between_lines):
                                    if img_array[new_y_index, new_x_index] == 255:
                                        continued = False
                                        break
                                    else:
                                        continued = True
                            if continued:
                                continue 
                            temp_y_above = starting_above_black
                            temp_y_below = starting_below_black   
                            while True:
                                continued = True
                                for new_x_index2 in range(x_index - black_count + 1 - int(difference_between_lines / 4), x_index - 1 + int(difference_between_lines / 4)):
                                    if img_array[temp_y_above, new_x_index2] == 255:
                                        continued = False
                                        break
                                if continued:
                                    break
                                if temp_y_above <= input_y - (round(difference_between_lines_for_line_drawing) * 3 / 4) :
                                    black_note = False
                                    break

                                #there should be a number where temp_y_above is only there for this check or another variable if it hits where a line was
                                #i think this is the issue bc it is scared of the line it cuts off once it gets a max above
                                continued = True
                                most_left = -1
                                flag = False
                                while True:
                                    if most_left == -1:
                                        most_left = x_index - black_count + 1
                                    temp_pixel = img_array[temp_y_above, most_left]
                                    if temp_pixel == 255:
                                        most_left += 1
                                        break
                                    if x_index - most_left >= round(difference_between_lines * 2):
                                        flag = True
                                        break
                                    most_left -= 1
                                if not flag:
                                    for new_x_index2 in range (most_left, most_left + round(difference_between_lines * 2)):
                                        if img_array[temp_y_above, new_x_index2] == 255:
                                            continued = False
                                            break
                                temp_pixel_above = img_array[temp_y_above, new_x_index]       
                                if temp_pixel_above == 255:
                                    break
                                temp_y_above -= 1   

                            #this would all be working if temp_y_above worked better
                            if black_note and past_temp_y_above != -1:
                                if changed_direction_above == 0: 
                                    if past_temp_y_above - temp_y_above > 0:
                                        changed_direction_above = 1
                                    elif past_temp_y_above - temp_y_above != 0:                                        
                                        black_note = False
                                elif changed_direction_above == 1:
                                    #if it's going up make sure it starts going down
                                    if temp_y_above - past_temp_y_above > 0:
                                        changed_direction_above = 2
                                else:
                                    if past_temp_y_above - temp_y_above > 0:
                                        black_note = False  

                            if black_note:
                                if temp_y_above <= max_above or max_above == -1:
                                    max_above = temp_y_above
                                while True:
                                    continued = True
                                    for new_x_index2 in range(x_index - black_count + 1 - int(difference_between_lines / 4), x_index - 1 + int(difference_between_lines / 4)):
                                        if img_array[temp_y_below, new_x_index2] == 255:
                                            continued = False
                                            break
                                    if continued:
                                        break
                                    if temp_y_below >= input_y + (round(difference_between_lines_for_line_drawing) * 3 / 4):

                                        black_note = False
                                        break
                                    continued = True
                                    most_left = -1
                                    flag = False
                                    while True:
                                        if most_left == -1:
                                            most_left = x_index - black_count + 1
                                        temp_pixel = img_array[temp_y_below, most_left]
                                        if temp_pixel == 255:
                                            most_left += 1
                                            break
                                        if x_index - most_left >= round(difference_between_lines * 2):
                                            flag = True
                                            break
                                        most_left -= 1
                                    if not flag:
                                        for new_x_index2 in range (most_left, most_left + round(difference_between_lines * 2)):
                                            if img_array[temp_y_below, new_x_index2] == 255:
                                                continued = False
                                                break
                                    temp_pixel_below = img_array[temp_y_below, new_x_index]      
                                    if temp_pixel_below == 255:
                                        break
                                    temp_y_below += 1  

                                if black_note and past_temp_y_below != -1:
                                    if changed_direction_below == 0: 
                                        #<= bc of the below it can start straight too not only down
                                        if past_temp_y_below - temp_y_below <= 0:
                                            changed_direction_below = 1
                                        else:

                                            black_note = False
                                    elif changed_direction_below == 1:
                                        #if it's going down or straight make sure it starts going up
                                        if temp_y_below - past_temp_y_below < 0:
                                            changed_direction_below = 2
                                    else:
                                        if past_temp_y_below - temp_y_below < 0:
                                            black_note = False   
                                if black_note:
                                    if temp_y_below >= max_below:
                                        max_below = temp_y_below
                                    left_zone = False
                                    if not left_zone and new_x_index >= x_index - black_count + 1:
                                        if new_x_index >= x_index - round(black_count / 2):
                                            #note here
                                            left_zone = True
                                        #gives exception of if it increases proportiately
                                        elif abs((past_temp_y_above - temp_y_above) - (temp_y_below - past_temp_y_below)) < difference_between_lines / 10 and past_temp_y_above - temp_y_above >= 0 and temp_y_below - past_temp_y_below >= 0:
                                            past_temp_y_above = temp_y_above
                                            past_temp_y_below = temp_y_below
                                        #have no past
                                        elif past_temp_y_above == -1:                                            
                                            past_temp_y_above = temp_y_above
                                            past_temp_y_below = temp_y_below
                                        #slowly increasing
                                        elif past_temp_y_above - temp_y_above <= round(difference_between_lines / 5) and past_temp_y_above - temp_y_above >= 0:
                                            if temp_y_below - past_temp_y_below <= round(difference_between_lines / 5) and temp_y_below - past_temp_y_below >= 0:
                                                past_temp_y_above = temp_y_above
                                                past_temp_y_below = temp_y_below
                                        #not the correct note
                                        else:
                                            black_note = False
                                            break
                                    elif new_x_index <= x_index - 1:
                                        if abs((temp_y_above - past_temp_y_above) - (past_temp_y_below - temp_y_below)) < difference_between_lines / 10 and temp_y_above - past_temp_y_above >= 0 and past_temp_y_below - temp_y_below >= 0:
                                            past_temp_y_above = temp_y_above
                                            past_temp_y_below = temp_y_below
                                        elif temp_y_above - past_temp_y_above <= round(difference_between_lines / 5) and temp_y_above - past_temp_y_above >= 0:
                                            if past_temp_y_below - temp_y_below <= round(difference_between_lines / 5) and past_temp_y_below - temp_y_below >= 0:
                                                past_temp_y_above = temp_y_above
                                                past_temp_y_below = temp_y_below
                                        else:
                                            black_note = False
                                            break
                    
                    black_note = False
                    if changed_direction_above == 2 or changed_direction_below == 2:
                        black_note = True
                    if black_note:
                        if max_above > input_y - round(difference_between_lines_for_line_drawing / 2) + (line_height * 2):
                            black_note = False
                        if black_note:
                            if max_below < input_y + round(difference_between_lines_for_line_drawing / 2) - (line_height * 2):
                                black_note = False   
                        if black_note:
                            if max_below - max_above > difference_between_lines_for_line_drawing + (line_height * 3):
                                black_note = False

                    if black_note:
                        top_left = [x_index - black_count, input_y - (round(difference_between_lines_for_line_drawing / 2) - 1)]
                        bottom_right = [x_index, input_y + (round(difference_between_lines_for_line_drawing / 2) - 1)]
                        black_notes.append([top_left, bottom_right])
                    black_count = 0

            else:
                white_note = True

                #dashed white notes
                max_above = -1
                max_below = -1
                starting_above_white = input_y 
                starting_below_white = input_y 
                temp_pixel_above = img_array[starting_above_white, x_index - int(black_count / 2)]
                temp_pixel_below = img_array[starting_below_white, x_index - int(black_count / 2)]    
                while temp_pixel_below != 255:
                    starting_below_white += 1
                    temp_pixel_below = img_array[starting_below_white, x_index - int(black_count / 2)]
                while temp_pixel_above != 255:
                    starting_above_white -= 1
                    temp_pixel_above = img_array[starting_above_white, x_index - int(black_count / 2)]  

                if white_note:    
                    counter = 0
                    above = False
                    below = False
                    white_note = True
                    while True:
                        temp_pixel_above = img_array[starting_above_white - counter, x_index - int(black_count / 2)]
                        temp_pixel_below = img_array[starting_below_white + counter, x_index - int(black_count / 2)]
                        if counter > int(difference_between_lines_for_line_drawing / 2):
                            white_note = False
                            break
                        if temp_pixel_above != 255:
                            above = True
                        if temp_pixel_below != 255:
                            below = True
                        if above and below:
                            break
                        counter += 1

                starting_of_space_above_outside = -1
                ending_of_space_above_outside = -1
                starting_of_space_above_inside = -1
                ending_of_space_above_inside = -1

                temporary_x = x_index - round(black_count / 2)
                #getting starting inside
                if white_note:
                    while True:
                        if temporary_x < 0: 
                            white_note = False
                            break
                        temp_pixel = img_array[starting_above_white, temporary_x]
                        if temp_pixel != 255:
                            starting_of_space_above_inside = temporary_x + 1
                            break
                        temporary_x -= 1
                if white_note:
                    while True:
                        if temporary_x < 0:
                            white_note = False
                            break
                        #think this is the right area
                        temp_pixel = img_array[starting_above_white, temporary_x]
                        if temp_pixel == 255:
                            starting_of_space_above_outside = temporary_x + 1
                            break
                        temporary_x -= 1
                #ending
                temporary_x = x_index - round(black_count / 2)
                if white_note:
                    while True:
                        if temporary_x >= width - 1: 
                            white_note = False
                            break
                        temp_pixel = img_array[starting_above_white, temporary_x]
                        if temp_pixel != 255:
                            ending_of_space_above_inside = temporary_x - 1
                            break
                        temporary_x += 1
                if white_note:
                    while True:
                        if temporary_x >= width - 1:
                            white_note = False
                            break
                        #think this is the right area
                        temp_pixel = img_array[starting_above_white, temporary_x]
                        if temp_pixel == 255:
                            ending_of_space_above_outside = temporary_x - 1
                            break
                        temporary_x += 1

                distance_above = ending_of_space_above_inside - starting_of_space_above_inside + 1

                if white_note:
                    if distance_above < (difference_between_lines / 3) or distance_above > (difference_between_lines):
                        white_note = False
                                
                starting_of_space_below_outside = -1
                ending_of_space_below_outside = -1
                starting_of_space_below_inside = -1
                ending_of_space_below_inside = -1
                
                if white_note:
                    #starting
                    temporary_x = x_index - round(black_count / 2)
                    #getting starting inside
                    while True:
                        if temporary_x < 0: 
                            white_note = False
                            break
                        temp_pixel = img_array[starting_below_white, temporary_x]
                        if temp_pixel != 255:
                            starting_of_space_below_inside = temporary_x + 1
                            break
                        temporary_x -= 1
                if white_note:
                    while True:
                        if temporary_x < 0:
                            white_note = False
                            break
                        temp_pixel = img_array[starting_below_white, temporary_x]
                        if temp_pixel == 255:
                            starting_of_space_below_outside = temporary_x + 1
                            break
                        temporary_x -= 1
                #ending
                if white_note:
                    temporary_x = x_index - round(black_count / 2)
                    while True:
                        if temporary_x >= width - 1: 
                            white_note = False
                            break
                        temp_pixel = img_array[starting_below_white, temporary_x]
                        if temp_pixel != 255:
                            ending_of_space_below_inside = temporary_x - 1
                            break
                        temporary_x += 1
                if white_note:
                    while True:
                        if temporary_x >= width - 1:
                            white_note = False
                            break
                        temp_pixel = img_array[starting_below_white, temporary_x]
                        if temp_pixel == 255:
                            ending_of_space_below_outside = temporary_x - 1
                            break
                        temporary_x += 1

                #+1 bc of how it is the inside white pixels spacing have to compensate
                distance_below = ending_of_space_below_inside - starting_of_space_below_inside + 1

                if distance_below < (difference_between_lines / 3):
                    white_note = False

                start = max(starting_of_space_above_outside, starting_of_space_below_outside)
                end = min(ending_of_space_above_outside, ending_of_space_below_outside)
                
                #testing distance!!!
                if abs(starting_of_space_above_outside - starting_of_space_below_outside) > difference_between_lines / 4 or abs(ending_of_space_above_outside - ending_of_space_below_outside) > difference_between_lines / 4:
                    white_note = False
                if max(ending_of_space_above_outside, ending_of_space_below_outside) - min(starting_of_space_above_outside, starting_of_space_below_outside) > difference_between_lines * 2.5:
                    white_note = False
                if end - start <= difference_between_lines * 1.15:
                    white_note = False

                #top part 
                if white_note:
                    past_temp_y = -1
                    for new_x_index in range(starting_of_space_above_inside, ending_of_space_above_inside):
                        temp_pixel = img_array[starting_above_white, new_x_index]
                        temp_y_above = starting_above_white
                        if white_note:
                            while True:
                                if temp_y_above <= input_y - round(difference_between_lines_for_line_drawing * 3 / 4):
                                    white_note = False
                                    break
                                temp_pixel_above = img_array[temp_y_above, new_x_index]
                                if temp_pixel_above != 255:
                                    break
                                temp_y_above -= 1
                            if temp_y_above <= max_above or max_above == -1:
                                max_above = temp_y_above
                            if past_temp_y == -1 or (abs(past_temp_y - temp_y_above) <= round(difference_between_lines / 5) and abs(past_temp_y - temp_y_above) <= round(difference_between_lines / 5)):
                                past_temp_y = temp_y_above
                            else:
                                white_note = False
                                break      

                #bottom part
                if white_note:
                    past_temp_y = -1
                    for new_x_index in range(starting_of_space_below_inside, ending_of_space_below_inside):
                        temp_pixel = img_array[starting_below_white, new_x_index]
                        temp_y_below = starting_below_white
                                
                        if white_note:
                            while True:
                                if temp_y_below >= input_y + round(difference_between_lines_for_line_drawing * 3 / 4):
                                    white_note = False
                                    break
                                temp_pixel_below = img_array[temp_y_below, new_x_index]
                                if temp_pixel_below != 255:
                                    break
                                temp_y_below += 1
                            if white_note:
                                if temp_y_below >= max_below:
                                    max_below = temp_y_below
                            if past_temp_y == -1 or (abs(past_temp_y - temp_y_below) <= round(difference_between_lines / 5) and abs(past_temp_y - temp_y_below) <= round(difference_between_lines / 5)):
                                past_temp_y = temp_y_below
                            else:
                                white_note = False
                                break
                        
                if white_note:
                    #little /5 cuz it is not all the way
                    if max_above > input_y - round(difference_between_lines / 5):
                        white_note = False
                    if white_note:
                        if max_below < input_y + round(difference_between_lines / 5):
                            white_note = False
                    #overall height check
                    if white_note:
                        if max_below - max_above > difference_between_lines + line_height:
                            white_note = False
                #put it in here
                if white_note:
                    #remove this eventually
                    top_left = [x_index - black_count, input_y - 10]
                    bottom_right = [x_index, input_y + 10]   
                    dashed_whites.append([top_left, bottom_right])

            black_count = 0       
        else:
            black_count = 0



    return dashed_whites, black_notes, white_notes
