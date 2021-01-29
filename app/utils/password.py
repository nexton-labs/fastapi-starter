import random
import string
from typing import List, Union

from app.settings.globals import USER_PASSWORD_LENGTH


def generate_random() -> str:
    random_source = string.ascii_letters + string.digits
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)

    remaining_characters = (
        0
        if USER_PASSWORD_LENGTH - len(password) <= 0
        else USER_PASSWORD_LENGTH - len(password)
    )

    for _ in range(remaining_characters):
        password += random.choice(random_source)
    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = "".join(password_list)
    return password


def verify_password_policy(password: str) -> List[Union[bool, str]]:
    rules = {
        "upper": lambda s: any(x.isupper() for x in s),
        "lower": lambda s: any(x.islower() for x in s),
        "digit": lambda s: any(x.isdigit() for x in s),
        "length": lambda s: len(s) >= USER_PASSWORD_LENGTH,
    }

    return [name for (name, rule) in rules.items() if not rule(password)]
