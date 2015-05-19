class WXpayException(Exception):
    '''Base Alipay Exception'''


class MissingParameter(WXpayException):
    """Raised when the create payment url process is missing some
    parameters needed to continue"""


class ParameterValueError(WXpayException):
    """Raised when parameter value is incorrect"""


class TokenAuthorizationError(WXpayException):
    '''The error occurred when getting token '''
