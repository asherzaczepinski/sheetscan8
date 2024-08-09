from process_line import process_line
from sort_notes import sort_notes

def return_notes (invisible_lines, img_array, width, difference_between_lines_for_line_drawing, difference_between_lines, line_height, image_path, Image, all_rows, lines):
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

    return new_notes, all_rows