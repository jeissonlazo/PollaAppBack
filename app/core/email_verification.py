import random


def generate_verification_code():
    return str(
        random.randint(
            10000,
            99999
        )
    )