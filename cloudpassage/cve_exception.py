"""CveException Class"""
import cloudpassage.sanity as sanity
from .halo_endpoint import HaloEndpoint
from .http_helper import HttpHelper


class CveExceptions(HaloEndpoint):
    """Initializing the CveException class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    # object_name = "cve_exception" # deprecated
    # objects_name = "cve_exceptions"  # deprecated
    # default_endpoint_version = 1 # deprecated
    object_name = "exception"
    objects_name = "exceptions"
    default_endpoint_version = 2

    def endpoint(self):
        """Return the endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)

    @classmethod
    def object_key(cls):
        """Return the key used to pull the object from the json document."""
        return cls.object_name

    @classmethod
    def pagination_key(cls):
        """Return the pagination key for parsing paged results."""
        return cls.objects_name

    # deprecated
    '''
    def create(self, package_name, package_version, scope="all", scope_id=''):
        """This method allows user to create CVE exceptions.
        Args:
            package_name (str): The name of the vulnerable
                                package to be excepted.
            package_version (str): The version number of the
                                   vulnerable package.
            scope (str): Possible values are server, group and all.
            scope_id (str): If you pass the value server as scope, this field
                will include server ID. If you pass the value group as scope,
                this field will include group ID.
        Returns:
            str: ID of the newly-created cve exception
        """
        body_ref = {
            "server": "server_id",
            "group": "group_id"
        }

        params = {
            "package_name": package_name,
            "package_version": package_version,
            "scope": scope
        }

        endpoint = self.endpoint()

        if scope != "all":
            sanity.validate_cve_exception_scope_id(scope_id)
            scope_key = body_ref[scope]
            params[scope_key] = scope_id

        body = {"cve_exception": params}
        request = HttpHelper(self.session)
        response = request.post(endpoint, body)
        return response["cve_exception"]["id"]
    '''

    def create(self, package_name, package_version, target_type):
        """This method allows user to create CVE exceptions.

        Args:
            package_name (str): The name of the vulnerable
                                package to be excepted.
            package_version (str): The version number of the
                                   vulnerable package.
            target_type (str): Possible values are server, container_image.
            

        Returns:
            str: ID of the newly-created cve exception
        """

        params = {
            "target_type": target_type,
            "status": "active",
            "definition": {
                "package_name": package_name,
                "package_version": package_version,
            }
            
        }

        endpoint = self.endpoint()
        
        body = {"exception": params}
        request = HttpHelper(self.session)
        response = request.post(endpoint, body)
        return response["exception"]["id"]
    
    def update(self, exception_id, **kwargs):
        """ Update CVE Exceptions.

        Args:
            exception_id (str): Identifier for the CVE exception.

        Keyword Args:
            scope (str): Possible values are server, group and all.
            group_id (str): The ID of the server group containing the server to
                which this exception applies.
            server_id (str): The ID of the server to which this exception
                applies.
            cve_entries : List of CVEs

        Returns:
            True if successful, throws exception otherwise.
        """

        endpoint = "{}/{}".format(self.endpoint(), exception_id)
        # body = {"cve_exception": kwargs} # deprecated
        body = {"exception": kwargs}
        request = HttpHelper(self.session)
        response = request.put(endpoint, body)
        return response


# The following class needs to live on only in name, and should absorb the
# functionality of the current CveExceptions class.

class CveException(HaloEndpoint):
    """Initializing the CveException class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    """

    # object_name = "cve_exception" # deprecated
    # objects_name = "cve_exceptions" # deprecated
    # default_endpoint_version = 1 # deprecated
    object_name = "exception"
    objects_name = "exceptions"
    default_endpoint_version = 2

    def endpoint(self):
        """Return the endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)

    @classmethod
    def object_key(cls):
        """Return the key used to pull the object from the json document."""
        return cls.object_name

    @classmethod
    def pagination_key(cls):
        """Return the pagination key for parsing paged results."""
        return cls.objects_name
