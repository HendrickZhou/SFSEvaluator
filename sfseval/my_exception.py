class WrongFormatError(Exception):
    """data in wrong/unsupported format"""
    pass

class InvalidResourceError(Exception):
    """file/data etc. not found"""
    pass

class IllegalTypeError(Exception):
    """illegal type for the standard format in dataset/codebase descriptor"""
    pass