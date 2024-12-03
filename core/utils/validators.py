from string import digits , ascii_lowercase , ascii_uppercase

validate_characters = digits + ascii_lowercase + ascii_uppercase + ' ' + '_' + '-'


def validate_str(string:str) -> bool:
    for i in string:
        if i not in validate_characters:
            return False
    return True