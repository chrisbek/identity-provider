from enum import Enum


class OperationType(str, Enum):
    READ = 'r'
    WRITE = 'w'
    CREATE = 'c'
    DELETE = 'd'
    EXECUTE = 'e'
