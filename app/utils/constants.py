from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Gender(str, ExtendedEnum):
    MALE = "MALE"
    FEMALE = "MALE"
    UNKNOWN = "UNKNOWN"


class Role(str, ExtendedEnum):
    ADMIN = "ADMIN"
    CANDIDATE = "CANDIDATE"


class ImageSize(str, ExtendedEnum):
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"

    @classmethod
    def get_size(cls, size):
        if size == cls.XS:
            return "30:30"
        elif size == cls.SM:
            return "100:100"
        elif size == cls.MD:
            return "300:300"
        elif size == cls.LG:
            return "0:0"

        raise ValueError("{} is not a valid size".format(size))
