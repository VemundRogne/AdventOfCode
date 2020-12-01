def read_input(path=str):
    with open(path, 'r') as f:
        return [int(line) for line in f]


def find_solution_brute(numbers):
    for number_1 in numbers:
        for number_2 in numbers:
            if number_1 + number_2 == 2020:
                return (number_1, number_2)


def verify_solution(number_1, number_2):
    assert number_1 + number_2 == 2020
    return number_1 * number_2


def test_brute_solution():
    number_1, number_2 = find_solution_brute(
        read_input(
            "day_1_input.txt"
        )
    )

    solution = verify_solution(number_1, number_2)
    assert solution == 888331
    print("Solution:", solution)