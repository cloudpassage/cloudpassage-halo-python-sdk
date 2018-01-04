"""CveException Class"""

import cloudpassage.sanity as sanity
from cloudpassage.http_helper import HttpHelper


class CveExceptions(object):
    """Initializing the CveException class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """This method will retreive all defined software exceptions
           from the Halo database.

        This is represented as a list of dictionaries

        This will only return a maximum of 20 pages, which amounts to
        200 cve exceptions. If you have more than that, you should consider
        using the SDK within a multi-threaded application.

        """

        endpoint = "/v1/cve_exceptions"
        key = "cve_exceptions"
        max_pages = 20
        request = HttpHelper(self.session)
        response = request.get_paginated(endpoint, key,
                                         max_pages)

        return response

    def describe(self, exception_id):
        """This method will retrieves the software exception
           specified by exception ID.

        Args:
            exception_id (str): Identifier for this CVE exception.

        Returns:
            dict: Dictionary object describing CVE exceptions.
        """

        endpoint = "/v1/cve_exceptions/%s" % exception_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        cve_exception = response["cve_exception"]
        return cve_exception

    def create(self, **kwargs):
        """This method allows user to create CVE exceptions.

        Required Keyword Args:
            package_name (str): The name of the vulnerable
                                package to be excepted.
            package_version (str): The version number of the
                                   vulnerable package.
            scope (str): Possible values are server, group and all.
            If you pass the value server in this field,
            the request JSON must also include a server ID
            in the server_id field. If you pass the value
            group in this field, the request JSON must
            also include a group ID in the group_id field.
            If you pass all, the exception applies to
            all servers across your entire Halo account.

        Returns:
            str: ID of the newly-created cve exception
        """

        endpoint = "/v1/cve_exceptions"
        sanity.validate_cve_exception_cbody(kwargs)
        body = {"cve_exception": kwargs}
        request = HttpHelper(self.session)
        response = request.post(endpoint, body)
        return response["cve_exception"]["id"]

    def update(self, exception_id, **kwargs):
        """ Update CVE Exceptions.

        Args:
            exception_id (str): Identifier for the CVE exception.

        Keyword Args:
            scope (str): Possible values are server, group and all.
            group_id (str): The ID of the server group containing the
            server to which this exception applies.
            server_id (str): The ID of the server to which
            this exception applies.
            cve_entries : List of CVEs

        Returns:
            True if successful, throws exception otherwise.
        """

        endpoint = "/v1/cve_exceptions/%s" % exception_id
        body = {"cve_exception": kwargs}
        request = HttpHelper(self.session)
        response = request.put(endpoint, body)
        return response

    def delete(self, exception_id):
        """ Delete a CVE Exception.

        Args:
            exception_id (str): Identifier for the CVE exception.

        Returns:
            None if successful, exceptions otherwise.

        """

        endpoint = "/v1/cve_exceptions/%s" % exception_id
        request = HttpHelper(self.session)
        request.delete(endpoint)
        return None
