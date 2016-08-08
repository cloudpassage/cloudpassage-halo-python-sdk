"""CloudPassage-specific exceptions"""


class CloudPassageAuthentication(Exception):
    """Exception related to authentication.

    This is thrown in response to an issue authenticating against \
    the CloudPassage Halo API

    Args:
        error_msg (str): Message describing error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageAuthentication, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return repr(self.msg)

class CloudPassageAuthorization(Exception):
    """Exception related to authorization.

    Oftentimes related to the scope of the API credentials

    Args:
        error_msg (str): Message describing the error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageAuthorization, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return repr(self.msg)


class CloudPassageValidation(Exception):
    """Exception related to request validation.

    This can be thrown as a result of invalid information being passed \
    to the API (in response to HTTP error) or as a result of failing \
    to pass the SDK's internal validation routines.

    Args:
        error_msg (str): Message describing the error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageValidation, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return repr(self.msg)

class CloudPassageCollision(Exception):
    """Exception indicates a resource collision.

    This is thrown when attempting to create a resource
    which already exists.

    Args:
        error_msg (str): Message describing the error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageCollision, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return repr(self.msg)


class CloudPassageInternalError(Exception):
    """This exception indicates an error in the Analytics Engine.

    This is thrown when a HTTP response code of 500 is detected.

    Args:
        error_msg (str): Message describing the error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageInternalError, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return repr(self.msg)

class CloudPassageResourceExistence(Exception):
    """This exception indicates that you're trying to access a
       resource that doesn't exist.

    This is oftentimes thrown in response to a 404 from the API.

    Args:
        error_msg (str): Message describing the error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageResourceExistence, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return repr(self.msg)

class CloudPassageGeneral(Exception):
    """This is thrown when a more specific exception type is unavailable.

    The msg attribute should have plenty of information on what went wrong.

    Args:
        error_msg (str): Message describing the error

    Attributes:
        msg (str)

    """

    def __init__(self, error_msg):
        super(CloudPassageGeneral, self).__init__()
        self.msg = error_msg

    def __str__(self):
        return repr(self.msg)
