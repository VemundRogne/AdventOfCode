example_input = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc"
]


def load_input(path):
    with open(path, 'r') as f:
        return [line for line in f]


def parse_line(line):
    """Parses a single line of password policy and password

    Returns:
        A tuple of password rules and the password itself:
        (password, policy) where policy = (min, max, character)
    """
    # Splits the input into [min-max, character: password]
    split = line.strip().split(' ')
    [min, max] = [int(i) for i in split[0].split('-')]
    character = split[1][0]
    password = split[2]

    return (password, (min, max, character))


def test_parse_line():
    """ Tests our parser on the first line of the example input """
    password, policy = parse_line(example_input[0])
    assert password == "abcde"
    assert policy == (1, 3, "a")


def check_password_validity(password, policy):
    """Checks if a password is valid

    Args:
        password: The password of which we wish to check validity
        policy: The policy the password must fulfill
          (min, max, character)
    
    Returns:
        True if the password is valid, False if it is not.
    """
    y = lambda x : x == policy[2]   # Returns true if input x == policy.character
    char_x_in_pswd = list(filter(y, password))

    num_character = len(char_x_in_pswd)
    if num_character >= policy[0] and num_character <= policy[1]:
        return True
    return False


def test_check_password_validity():
    valid_password = "abcde"
    invalid_password = "aaaaabcde"  # Too many a-s
    invalid_password_2 = "bcdef"    # Too few a-s
    policy = (1, 3, "a")

    assert check_password_validity(valid_password, policy) == True
    assert check_password_validity(invalid_password, policy) == False
    assert check_password_validity(invalid_password_2, policy) == False


def count_valid_passwords(lines):
    """This function solves day2

    Arguments:
        lines: an iterable that yields lines of unparsed passwords and policies
    
    Returns:
        the number of valid passwords in the input
    """
    n_valid_passwords = 0

    for line in lines:
        password, policy = parse_line(line)

        if check_password_validity(password, policy):
            n_valid_passwords += 1
    
    return n_valid_passwords


def test_count_valid_passwords():
    assert count_valid_passwords(example_input) == 2


def test_solve_d2_p1():
    d1_input = load_input("inputs/d2.input")
    print("Solution:", count_valid_passwords(d1_input))