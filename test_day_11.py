from enum import Enum

import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug


def cut_list(list_to_cut, center_coordinate, width = 1):
    """ Zero indexed function to cut a list """
    lower = center_coordinate - width
    if lower < 0:
        lower = 0
    
    upper = center_coordinate + width + 1
    if upper > len(list_to_cut):
        upper = len(list_to_cut)

    return list_to_cut[lower : upper]


def cut_square(nested_list, x_center, y_center):
    y_lists = cut_list(nested_list, y_center)
    return [cut_list(y_list, x_center) for y_list in y_lists]


def flatten_list(nested_list):
    """ Takes a nested list of depth 1 and returns a flat list 
    
    [[1, 2, 3], [4, 5, 6]] -> [1, 2, 3, 4, 5, 6]
    """
    return [item for sublist in nested_list for item in sublist]


def dictionary_count(input_list):
    counter_dict = {}
    for item in input_list:
        if item not in counter_dict:
            counter_dict[item] = 0
        
        counter_dict[item] += 1
    return counter_dict


class seat(Enum):
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'


def read_input(path):
    with open(path, 'r') as f:
        seating_map = [line.strip() for line in f]
    return seating_map


def test_cut_list():
    A = [0, 1, 2, 3]

    testcut_0 = cut_list(A, 0)
    assert testcut_0 == [0, 1]

    testcut_1 = cut_list(A, 1)
    assert testcut_1 == [0, 1, 2]

    testcut_2 = cut_list(A, 2)
    assert testcut_2 == [1, 2, 3]

    testcut_3 = cut_list(A, 3)
    assert testcut_3 == [2, 3]


def test_cut_square():
    A = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    square = cut_square(A, 1, 2)
    assert square == [[4, 5, 6], [8, 9, 10], [12, 13, 14]]


def test_flatten_list():
    A = [[1, 2, 3], [4, 5, 6]]
    assert flatten_list(A) == [1, 2, 3, 4, 5, 6]


def test_counter_dict():
    A = ["1", "2", "1", "3", 1]
    count = dictionary_count(A)
    assert count["1"] == 2
    assert count["2"] == 1
    assert count["3"] == 1
    assert count[1] == 1


def seating_model(seating_square, center_seat_type):
    """ Takes a seating square, either a 3x3, 3x2 or 2x2 (edeges lead to non-squares)

    Returns what the seat should become
    """
    seating_square = flatten_list(seating_square)
    seating_count = dictionary_count(seating_square)

    # If a seat is empty and there are no occupied seats adjacent to it, the seat becomes occupied
    if center_seat_type == seat.EMPTY and seat.OCCUPIED not in seating_count:
        return seat.OCCUPIED

    # If a seat is occupied and four or more seats adjacent to it are also occupied
    # the seat becomes empty
    elif center_seat_type == seat.OCCUPIED and seating_count[seat.OCCUPIED] > 4:
        return seat.EMPTY
    
    else:
        return center_seat_type


def step_seating_sim(seating_map):
    """ Run a single step of the seating simulator """
    x_length = len(seating_map[0])
    y_length = len(seating_map)

    new_seating_map = []
    n_changes = 0

    # We must first run through the rows, because of the nested_list
    for y_coord, row in enumerate(seating_map):
        new_row = []
        for x_coord, center_seat in enumerate(row):
            center_seat = seat(center_seat)

            if center_seat == seat.FLOOR.value:
                new_row.append(seat.FLOOR)

            else:
                center_seat_square = cut_square(seating_map, x_coord, y_coord)
                updated_center_seat = seating_model(center_seat_square, center_seat)
                new_row.append(updated_center_seat)

                if updated_center_seat != center_seat:
                    n_changes += 1

        new_seating_map.append(new_row)
    return n_changes, new_seating_map


def run_seating_sim(seating_map):
    """ Runs the seating model until seats don't change anymore """
    n_steps = 0
    while True:
        n_changes, seating_map = step_seating_sim(seating_map)
        if n_changes == 0:
            break
        n_steps += 1
    return n_steps, seating_map


def count_occupied_seats(seating_map):
    seating_list = flatten_list(seating_map)
    seating_count = dictionary_count(seating_list)
    return seating_count[seat.OCCUPIED]


def test_step_seating_sim():
    seating_map = read_input("inputs/d11_test.input")
    n_changes, seating_map = step_seating_sim(seating_map)
    n_changes, seating_map = step_seating_sim(seating_map)


def test_run_seating_sim_on_test_input():
    seating_map = read_input("inputs/d11_test.input")
    n_steps, seating_map = run_seating_sim(seating_map)
    assert n_steps == 5
    assert count_occupied_seats(seating_map) == 37


def test_seating_model():
    A = [[seat.FLOOR, seat.OCCUPIED, seat.OCCUPIED],
         [seat.FLOOR, seat.OCCUPIED, seat.EMPTY],
         [seat.EMPTY, seat.FLOOR, seat.EMPTY]]

    assert seating_model(A, seat.OCCUPIED) == seat.OCCUPIED

    A = [[seat.FLOOR, seat.OCCUPIED, seat.OCCUPIED],
         [seat.FLOOR, seat.OCCUPIED, seat.EMPTY],
         [seat.OCCUPIED, seat.FLOOR, seat.OCCUPIED]]

    assert seating_model(A, seat.OCCUPIED) == seat.EMPTY

    A = [[seat.FLOOR, seat.EMPTY, seat.EMPTY],
         [seat.FLOOR, seat.EMPTY, seat.EMPTY],
         [seat.FLOOR, seat.FLOOR, seat.EMPTY]]

    assert seating_model(A, seat.EMPTY) == seat.OCCUPIED


def test_solve_day_11_part_1():
    seating_map = read_input("inputs/d11.input")
    n_steps, seating_map = run_seating_sim(seating_map)
    n_occupied = count_occupied_seats(seating_map)
    print(f"Solution = {n_occupied} in {n_steps} steps")