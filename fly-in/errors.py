
class FlyInError(Exception):
    pass


class ParseError(FlyInError):
    pass


class ValidationError(FlyInError):
    pass
