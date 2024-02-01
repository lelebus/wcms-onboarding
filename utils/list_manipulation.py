import random
import copy


def split_list(input_list, n):
    # Calculate the base size of each subset
    base_size = len(input_list) // n

    # Calculate the number of sublists that will have one extra element
    num_larger_sublists = len(input_list) % n

    sublists = []
    start = 0

    for i in range(n):
        sublist_size = base_size + (1 if i < num_larger_sublists else 0)
        sublist = input_list[start:start+sublist_size]
        sublists.append(sublist)
        start += sublist_size

    return sublists


def split_list_2(input_list, n):
    sublists = []
    for i in range(n):
        sublists.append(input_list[i:][::n])
    return sublists


def split_list_random(input_list, n):
    input_list_2 = copy.deepcopy(input_list)
    random.shuffle(input_list_2)
    return split_list_2(input_list_2, n)
