"""ContainerImage class"""

from .halo_endpoint import HaloEndpoint


class ContainerImage(HaloEndpoint):
    """Initializing the ContainerImage class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    # object_name = "image" # deprecated
    # objects_name = "images" # deprecated
    # default_endpoint_version = 1 # deprecated
    
    object_name = "container_image"
    objects_name = "container_images"
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
