"""ContainerPackage class"""

from .halo_endpoint import HaloEndpoint


class ContainerPackage(HaloEndpoint):
    """Initializing the ContainerPackage class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    # object_name = "software_package" # deprecated
    # objects_name = "software_packages" # deprecated
    # default_endpoint_version = 1 # deprecated
    object_name = "package"
    objects_name = "packages"
    default_endpoint_version = 2

    def endpoint(self, image_id):
        """Return endpoint for API requests."""
        return "/v{}/container_images/{}/{}".format(self.endpoint_version, image_id, self.objects_name)

    def pagination_key(self):
        """Return the pagination key for parsing paged results."""
        return self.objects_name

    def object_key(self):
        """Return the object key for parsing detailed results."""
        return self.object_name

    def describe(self):
        """Not implemented for this object."""
        raise NotImplementedError

    def create(self):
        """Not implemented for this object."""
        raise NotImplementedError

    def delete(self):
        """Not implemented for this object."""
        raise NotImplementedError

    def update(self):
        """Not implemented for this object."""
        raise NotImplementedError
