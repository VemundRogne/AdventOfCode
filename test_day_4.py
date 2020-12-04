def load_input():
    with open("inputs/d4.input", 'r') as f:
        return [line for line in f]


def string_to_dict(line, target_dict=None):
    """ Takes a string and converts it into a dictionary

    The format of the string must be that of the AoC
    """
    line = line.strip()

    if target_dict == None:
        target_dict = {}

    for key_value in line.split(" "):
        key, value = key_value.split(":")

        if key not in target_dict.keys():
            target_dict[key] = value
        else:
            raise Exception("Key already exists in the target_dictionary")
    
    return target_dict


def test_string_to_dict():
    test_string = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd"

    # Creating a dictionary from a string
    target_dict = string_to_dict(test_string)
    assert target_dict == {'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd'}

    # Extening an existing dictionary
    target_dict = string_to_dict("byr:1937", target_dict)
    assert target_dict == {'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd', 'byr': '1937'}


def load_passports():
    passports = []

    passport = None
    for line in load_input():
        if line == '\n':
            passports.append(passport)
            passport = None
        else:
            passport = string_to_dict(line, passport)
    
    if passport is not None:
        passports.append(passport)
    
    return passports


def check_passport_validity(passport):
    passport_keys = set(passport.keys())

    required_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    optional_keys = {'cid'}

    if (passport_keys & required_keys) == required_keys:
        return True
    else:
        return False


def get_valid_passports(passports):
    return list(filter(check_passport_validity, passports))


def test_solve_day4_part1():
    passports = load_passports()
    valid_passports = get_valid_passports(passports)
    print("Valid passwords:", len(valid_passports), end=' ')
    assert len(valid_passports) == 250  # Known solution