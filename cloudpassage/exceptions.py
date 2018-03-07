"""CloudPassage-specific exceptions"""


def massage_error_code(error_code):
    """Massages error codes for cleaner exception handling.

    Args:
        int Error code

    Returns:
        int Error code.  If arg is not an integer, will change to 999999

    """
    if type(error_code) is not int:
        error_code = 999999
    return error_code


class CloudPassageAuthentication(Exception):
    """Exception related to authentication.

    This is thrown in response to an issue authenticating against \
    the CloudPassage Halo API

    Args:
        error_msg (str): Message describing error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg, **kwargs):
        super(CloudPassageAuthentication, self).__init__()
        if "code" in kwargs:
            self.code = massage_error_code(kwargs["code"])
            self.msg = "%d %s" % (self.code, error_msg)
        else:
            self.msg = error_msg

    def __str__(self):
        return str(self.msg)


class CloudPassageAuthorization(Exception):
    """Exception related to authorization.

    Oftentimes related to the scope of the API credentials

    Args:
        error_msg (str): Message describing the error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg, **kwargs):
        super(CloudPassageAuthorization, self).__init__()
        if "code" in kwargs:
            self.code = massage_error_code(kwargs["code"])
            self.msg = "%d %s" % (self.code, error_msg)
        else:
            self.msg = error_msg

    def __str__(self):
        return str(self.msg)


class CloudPassageValidation(Exception):
    """Exception related to request validation.

    This can be thrown as a result of invalid information being passed \
    to the API (in response to HTTP error) or as a result of failing \
    to pass the SDK's internal validation routines.

    Args:
        error_msg (str): Message describing the error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg, **kwargs):
        super(CloudPassageValidation, self).__init__()
        if "code" in kwargs:
            self.code = massage_error_code(kwargs["code"])
            self.msg = "%d %s" % (self.code, error_msg)
        else:
            self.msg = error_msg

    def __str__(self):
        return str(self.msg)


class CloudPassageCollision(Exception):
    """Exception indicates a resource collision.

    This is thrown when attempting to create a resource
    which already exists.

    Args:
        error_msg (str): Message describing the error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageCollision, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return str(self.msg)


class CloudPassageInternalError(Exception):
    """This exception indicates an error in the Analytics Engine.

    This is thrown when a HTTP response code of 500 is detected.

    Args:
        error_msg (str): Message describing the error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg, **kwargs):
        super(CloudPassageInternalError, self).__init__()
        if "code" in kwargs:
            self.code = massage_error_code(kwargs["code"])
            self.msg = "%d %s" % (self.code, error_msg)
        else:
            self.msg = error_msg

    def __str__(self):
        return str(self.msg)


class CloudPassageResourceExistence(Exception):
    """This exception indicates that you're trying to access a \
    resource that doesn't exist.

    This is oftentimes thrown in response to a 404 from the API.

    Args:
        error_msg (str): Message describing the error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg, **kwargs):
        super(CloudPassageResourceExistence, self).__init__()
        if "code" in kwargs:
            self.code = massage_error_code(kwargs["code"])
            self.msg = "%d %s " % (self.code, error_msg)
            if "url" in kwargs:
                self.msg += kwargs["url"]
        else:
            self.msg = error_msg

    def __str__(self):
        return str(self.msg)


class CloudPassageRateLimit(Exception):
    """This exception indicates that you have exceeded the allotted \
    number of api calls per minute.

    This is thrown when a HTTP response code of 429 is detected.

    Args:
        error_msg (str): Message describing the error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg, **kwargs):
        super(CloudPassageRateLimit, self).__init__()
        if "code" in kwargs:
            self.code = massage_error_code(kwargs["code"])
            self.msg = "%d %s" % (self.code, error_msg)
        else:
            self.msg = error_msg

    def __str__(self):
        return str(self.msg)


class CloudPassageGeneral(Exception):
    """This is thrown when a more specific exception type is unavailable.

    The msg attribute should have plenty of information on what went wrong.

    Args:
        error_msg (str): Message describing the error

    Keyword Args:
        code (int): Numeric ID for error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg, **kwargs):
        super(CloudPassageGeneral, self).__init__()
        if "code" in kwargs:
            self.code = massage_error_code(kwargs["code"])
            self.msg = "%d %s" % (self.code, error_msg)
        else:
            self.msg = error_msg

    def __str__(self):
        return str(self.msg)
