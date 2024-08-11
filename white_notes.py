    
def findWhiteNotes (input_y, img_array, width, difference_between_lines_for_line_drawing, difference_between_lines, line_height):
    white_notes = []
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

    return white_notes