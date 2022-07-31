from enum import Enum


class StringEnum(Enum):
    
    def __str__(self):
        return self.name