example_string = "Greenstone Building, Floor Main, 5101 50th Avenue, Yellowknife, Northwest Territories, X1A2N8"
parsed_list = example_string.split(', ')
list_length = len(parsed_list)

print('postal code ', parsed_list[-1:])
print('address', parsed_list[:-1])
print('city', parsed_list[-3:-1])
