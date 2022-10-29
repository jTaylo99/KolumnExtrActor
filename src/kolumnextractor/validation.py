import logging
import datetime as dt

from abc import ABC, abstractmethod
from inflection import camelize
from kolumnextractor.transformers import normalise

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def to_number(str):
    """
        to_number(str)

    Converts string from input into a number.

    Args:
        str: the string to be converted

    Returns:
        The string as an Int if it is an Int, a Float if it is a Float,
        or returns a ValueError if it is neither.
    """
    try:
        return int(str)
    except ValueError:
        try:
            return float(str)
        except ValueError:
            return ValueError


class Validator(ABC):
    def __init__(self):
        self.name = None

    def set_name(self, name):
        self.name = f'{name}'

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):
    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        value = to_number(value)
        if not isinstance(value, (int, float)):
            msg = f'Expected {value!r} to be an int or float'
            logging.error(msg)
            raise TypeError(msg)
        if self.minvalue is not None and value < self.minvalue:
            msg = f'Expected {value!r} to be at least {self.minvalue!r}'
            logging.error(msg)
            raise ValueError(msg)
        if self.maxvalue is not None and value > self.maxvalue:
            msg = f'Expected {value!r} to be no more than {self.maxvalue!r}'
            logging.error(msg)
            raise ValueError(msg)


class String(Validator):
    def __init__(self, case=None):
        self.case = case

    def validate(self, value):
        if not isinstance(value, (str)):
            msg = f"Expected {value!r} to be a String"
            logging.error(msg)
            raise TypeError(msg)
        match self.case:
            case "lower":
                if value.lower() != value:
                    msg = f"Expected {value!r} to be all lower case."
                    logging.error(msg)
                    raise TypeError(msg)
            case "upper":
                if value.upper() != value:
                    msg = f"Expected {value!r} to be all upper case."
                    logging.error(msg)
                    raise TypeError(msg)
            case "camel":
                if camelize(value, False) != value:
                    msg = f"Expected {value!r} to be camel case."
                    logging.error(msg)
                    raise TypeError(msg)
            case "normalised":
                if normalise(value) != value:
                    msg = f"Expected {value!r} to be a normalised string."
                    logging.error(msg)
                    raise TypeError(msg)

class Date(Validator):
    def __init__(self, earliest_date=None, latest_date=None, first_of_month=False):
        self.earliest_date = earliest_date
        self.latest_date = latest_date
        self.first_of_month = first_of_month

    def validate(self, value):
        if not isinstance(value, (dt.date)):
            msg = f'Expected {value} to be an int or float'
            logging.error(msg)
            raise TypeError(msg)
        if self.earliest_date is not None and value < self.earliest_date:
            msg = f'Expected {value} to be at least {self.earliest_date!r}'
            logging.error(msg)
            raise ValueError(msg)
        if self.latest_date is not None and value > self.latest_date:
            msg = f'Expected {value} to be no more than {self.latest_date}'
            logging.error(msg)
            raise ValueError(msg)
        if self.first_of_month and value.day != 1:
            msg = f'Expected {value} to be first day of the month'
            logging.error(msg)
            raise ValueError(msg)
