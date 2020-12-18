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


def check_passport_validity(passport, validata_data=False):
    passport_keys = set(passport.keys())

    required_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    optional_keys = {'cid'}

    if (passport_keys & required_keys) == required_keys:
        if validata_data == True:
            # Check birth-year
            byr = int(passport['byr'])
            if byr < 1920 or byr > 2002:
                print("Invalid byr", byr)
                return False
            
            # Check issue-year
            iyr = int(passport['iyr'])
            if iyr < 2010 or iyr > 2020:
                print(" invalid iyr", iyr)
                return False
            
            # Check expiration-year
            eyr = int(passport['eyr'])
            if eyr < 2020 or eyr > 2030:
                return False
            
            # Check height (This is kinda ugly, but whatever)
            unit = passport['hgt'][-2:]
            height = int(passport['hgt'][:-2])
            if unit == 'cm':
                if height < 150 or height > 193:
                    print("Invalid height: cm", height)
                    return False
            elif unit == 'in':
                if height < 59 or height > 76:
                    print("Invalid height: in", height)
                    return False
            else:
                return False

            # Check hair-color
            if passport['hcl'][0] != "#":
                return False
            colors = set(passport['hcl'][1:])
            if len(colors) != 6:
                return False
            valid_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}
            if (colors & valid_chars) != colors:
                return False
            
            # Check eye-color
            ecl = passport['ecl']
            if ecl not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
                print("Invalid eye color", ecl)
                return False
            
            pid = passport['pid']
            if len(pid) != 9:
                return False
            print(pid)
            
            return True

        return True
    else:
        return False


def get_valid_passports(passports, validata_data=False):
    _check_passport_validity = lambda passport: check_passport_validity(passport, validata_data)
    return list(filter(_check_passport_validity, passports))


def test_solve_day4_part1():
    passports = load_passports()
    valid_passports = get_valid_passports(passports)
    print("Valid passports:", len(valid_passports), end=' ')
    assert len(valid_passports) == 250  # Known solution

def test_solve_day4_part2():
    passports = load_passports()
    valid_passports = get_valid_passports(passports, validata_data=True)
    print("Valid passports:", len(valid_passports), end=' ')