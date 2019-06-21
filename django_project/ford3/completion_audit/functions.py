def isPresent(value):
    if type(value) is int:
        return isPresentForInteger(value)
    elif type(value) is str:
        return isPresentForString(value)
    elif type(value) is bool:
        return True
    else:
        return False


def isPresentForInteger(value):
    return isNotNone(value) and positiveValue(value)


def isPresentForString(value):
    return isNotNone(value) and positiveLen(value)


def isNotNone(value):
    return value is not None


def positiveLen(value):
    return len(value) > 0


def positiveValue(value):
    return value > 0
