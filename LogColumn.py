from enum import Enum


class LogColumn(Enum):
    """
    Enumeration of all available columns in a log file and their appropriate order
    """
    TIME = 0
    ID = 1
    EVENT_TYPE = 2
    ADDITIONAL_INFO = 3
