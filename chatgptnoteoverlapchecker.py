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
array1 = [
    [[1986, 663], [2015, 685]], 
    
]

array2 = [
    [[1986, 663], [2015, 685]], 
    [[1986, 663], [2035, 685]]
]

result = find_and_combine_extra(array1, array2)
print(result)
