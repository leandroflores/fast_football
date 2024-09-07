import random
import string


def update_object(
    obj: object, new_data: dict, custom_fields: dict = {}
) -> object:
    for key, value in new_data.items():
        if key in custom_fields:
            setattr(obj, key, custom_fields[key])
            continue
        setattr(obj, key, value)
    return obj


def random_str(size: int = 10) -> str:
    chars: str = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(size))


def random_int(
    start: int = 1000,
    end: int = 100000,
) -> int:
    return random.randint(start, end)
