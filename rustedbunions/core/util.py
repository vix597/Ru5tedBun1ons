from enum import Enum
from uuid import uuid4

from flags import MAX_FLAG_LENGTH

class DataType(Enum):
    ARBITRARY_USER_DATA = 1
    FLAG = 2
    OID = 3
    SHORT_NAME = 4
    PASSWORD = 5
    PIN = 6
    USER_SPECIFIED_MAX_LENGTH = 7
    USER_SPECIFIED_EXACT_LENGTH = 8

def ObjectId():
    return str(uuid4()).replace('-', '')

# The length an object ID should be
OID_LENGTH = len(ObjectId())

# The maximum length of user input we accept without error
MAX_DATA_LENGTH = 1000

# The max length for a username field that isn't vulnerable to SQLi
MAX_SHORT_NAME_LENGTH = 50

# The max length for a password field that isn't vulnerable to SQLi
MAX_PASSWORD_LENGTH = 128

# Max length for a PIN
MAX_PIN_LENGTH = 4

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_user_data_valid(data, data_type=DataType.ARBITRARY_USER_DATA, length=0):
    if not hasattr(data, '__len__'):
        return True

    if data_type == DataType.ARBITRARY_USER_DATA:
        return len(data) <= MAX_DATA_LENGTH
    elif data_type == DataType.FLAG:
        return len(data) <= MAX_FLAG_LENGTH
    elif data_type == DataType.OID:
        return len(data) == OID_LENGTH
    elif data_type == DataType.SHORT_NAME:
        return len(data) <= MAX_SHORT_NAME_LENGTH
    elif data_type == DataType.PASSWORD:
        return len(data) <= MAX_PASSWORD_LENGTH
    elif data_type == DataType.PIN:
        return len(data) <= MAX_PIN_LENGTH
    elif data_type == DataType.USER_SPECIFIED_MAX_LENGTH:
        return len(data) <= length
    elif data_type == DataType.USER_SPECIFIED_EXACT_LENGTH:
        return len(data) == length
    return False
