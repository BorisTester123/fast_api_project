from enum import Enum

class GlobalMessageErrors(Enum):
    WRONG_STATUS_CODE = 'Received status code is not equal to expected.'
    WRONG_ELEMENT_COUNT = 'Number of items is not equal to expected.'

class LanguageCode(Enum):
    RU = "RU"
    US = "US"
    FR = "FR"