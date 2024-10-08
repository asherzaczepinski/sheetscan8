def findDashedBlackNotes(input_y, img_array, width, difference_between_lines_for_line_drawing, difference_between_lines, line_height, black_notes, x_index):
    changed_direction_above = 0
    changed_direction_below = 0
    black_count = 0
    black_note = True
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
    return black_notes