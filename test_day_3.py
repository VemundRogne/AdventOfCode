from functools import reduce

def load_input():
    with open("inputs/d3.input", 'r') as f:
        return [line.strip() for line in f]


def traverse_map(tree_map, slope):
    collisions = 0
    for i in range(0, len(tree_map), slope[0]):
        if tree_map[i][(slope[1] * i) % len(tree_map[0])] == "#":
            collisions += 1
    return collisions


def test_solve_d3_p1():
    tree_map = load_input()
    assert 173 == traverse_map(tree_map, (1, 3))
    print("Solution:", traverse_map(tree_map, (1, 3)), end=' ')


def test_solve_d3_p2():
    tree_map = load_input()
    slopes = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
    tree_maps = [tree_map for slope in slopes]
    collisions = list(map(traverse_map, tree_maps, slopes))
    print(collisions)
    print([traverse_map(tree_map, slope) for slope in slopes])

    print("Solution:", reduce((lambda a,b : a*b), collisions), end=' ')
    assert reduce((lambda a,b : a*b), collisions) != 3336547200 # We know this is the wrong answer
