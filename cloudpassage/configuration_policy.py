"""ConfigurationPolicy class"""

from .halo_endpoint import HaloEndpoint
from .http_helper import HttpHelper
from .utility import Utility as utility

class ConfigurationPolicy(HaloEndpoint):
    """ConfigurationPolicy class:

    The list_all() method allows filtering by using keyword arguments. An
    exhaustive list of keyword arguments can be found at
    https://api-doc.cloudpassage.com/help#list-configuration-policies


    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    object_name = "policy"
    objects_name = "policies"
    module_name = "csm"
    # default_endpoint_version = 1 # deprecated
    default_endpoint_version = 2

    def endpoint(self):
        """Return the endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)
    
    def csm_endpoint(self):
        """Return the endpoint for API requests."""
        return "/v{}/{}?module={}".format(self.endpoint_version, self.objects_name, self.module_name)

    @classmethod
    def object_key(cls):
        """Return the key used to pull the policy from the json document."""
        return ConfigurationPolicy.object_name

    @classmethod
    def pagination_key(cls):
        """Return the pagination key for parsing paged results."""
        return ConfigurationPolicy.objects_name
    
    def list_all(self, **kwargs):
        """Lists all policies of module csm.

        Returns:
            list: List all policies of module csm (represented as dictionary-type objects)

        Note:
            This method supports query parameters via keyword arguments.

        """

        request = HttpHelper(self.session)
        params = utility.sanitize_url_params(kwargs)
        response = request.get_paginated(self.csm_endpoint(),
                                         self.pagination_key(), self.max_pages,
                                         params=params)
        return response
