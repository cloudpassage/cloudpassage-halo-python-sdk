"""Container class"""

from .halo_endpoint import HaloEndpoint


class Container(HaloEndpoint):
    """Initializing the Container class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    object_name = "container"
    objects_name = "containers"
    # default_endpoint_version = 1 # deprecated
    default_endpoint_version = 2

    def endpoint(self):
        """Return endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)

    def pagination_key(self):
        """Return the pagination key for parsing paged results."""
        return self.objects_name

    def object_key(self):
        """Return the object key for parsing detailed results."""
        return self.object_name

    def create(self):
        """Not implemented for this object."""
        raise NotImplementedError

    def delete(self):
        """Not implemented for this object."""
        raise NotImplementedError

    def update(self):
        """Not implemented for this object."""
        raise NotImplementedError
