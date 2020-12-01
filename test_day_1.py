def read_input(path=str):
    with open(path, 'r') as f:
        return [int(line) for line in f]


def find_solution_brute(numbers):
    for number_1 in numbers:
        for number_2 in numbers:
            if number_1 + number_2 == 2020:
                return (number_1, number_2)


def verify_solution(numbers):
    assert sum(numbers) == 2020

    running_product = 1
    for number in numbers:
        running_product = running_product * number
    return running_product


def test_brute_solution():
    solution = find_solution_brute(
        read_input(
            "day_1_input.txt"
        )
    )

    solution = verify_solution(solution)
    assert solution == 888331
    print("Solution:", solution)