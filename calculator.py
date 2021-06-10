"""
Calculator library containing basic math operations and spit_float.
"""


def add(first_term, second_term):
    return first_term + second_term


def subtract(first_term, second_term):
    return first_term - second_term


def multiply(first_term, second_term):
    return first_term * second_term


# Switched to calc_pow to avoid confusion with math.pow
# You can enforce arg type check with <arg_name> : <data_type>
def calc_pow(first_term, second_term: int):
    return first_term ** second_term


def spit_float() -> float:
    return float(1)


def integrationCalc():
    return
