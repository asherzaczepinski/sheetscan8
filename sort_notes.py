def sort_notes(notes):
    sorted_notes = []
    for row in notes:
        sorted_row = sorted(row, key=lambda note: note[1][0][0])
        sorted_notes.append(sorted_row)
    return sorted_notes