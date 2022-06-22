"""LidsPolicy class"""


from .halo_endpoint import HaloEndpoint
from .http_helper import HttpHelper
from .utility import Utility as utility


class LidsPolicy(HaloEndpoint):
    """Initializing the LidsPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    # object_name = "lids_policy" # deprecated
    # objects_name = "lids_policies" # deprecated
    # default_endpoint_version = 1 # deprecated
    object_name = "policy"
    objects_name = "policies"
    module_name = "lids"
    default_endpoint_version = 2

    def endpoint(self):
        """Return endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)
    
    def lids_endpoint(self):
        """Return endpoint for API requests."""
        return "/v{}/{}?module={}".format(self.endpoint_version, self.objects_name, self.module_name)

    @classmethod
    def pagination_key(cls):
        """Return the pagination key for parsing paged results"""
        return cls.objects_name

    @classmethod
    def object_key(cls):
        """Defines the key used to pull the object from the json document"""
        return cls.object_name
    
    def list_all(self, **kwargs):
        """Lists all policies of module lids.

        Returns:
            list: List all policies of module lids (represented as dictionary-type objects)

        Note:
            This method supports query parameters via keyword arguments.

        """

        request = HttpHelper(self.session)
        params = utility.sanitize_url_params(kwargs)
        response = request.get_paginated(self.lids_endpoint(),
                                         self.pagination_key(), self.max_pages,
                                         params=params)
        return response
