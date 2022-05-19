"""HaloEndpoint class"""

import cloudpassage.sanity as sanity
from .utility import Utility as utility
from .http_helper import HttpHelper


class HaloEndpoint(object):
    """Base class inherited by other specific HaloEndpoint classes."""

    # default_endpoint_version = 1 # deprecated
    default_endpoint_version = 2

    def __init__(self, session, **kwargs):
        self.session = session
        self.max_pages = 100
        self.set_endpoint_version(kwargs)

    def set_endpoint_version(self, kwargs):
        """Validate and set the endpoint version."""
        if "endpoint_version" in kwargs:
            version = kwargs["endpoint_version"]
            if isinstance(version, int):
                self.endpoint_version = version
            else:
                raise TypeError("Bad endpoint version {}".format(version))
        else:
            self.endpoint_version = self.default_endpoint_version

    @classmethod
    def endpoint(cls):
        """Not implemented at this level.  Raises exception."""
        raise NotImplementedError

    @classmethod
    def pagination_key(cls):
        """Not implemented at this level.  Raises exception."""
        raise NotImplementedError

    @classmethod
    def object_key(cls):
        """Not implemented at this level.  Raises exception."""
        raise NotImplementedError

    def list_all(self, **kwargs):
        """Lists all objects of this type.

        Returns:
            list: List of objects (represented as dictionary-type objects)

        Note:
            This method supports query parameters via keyword arguments.

        """

        request = HttpHelper(self.session)
        params = utility.sanitize_url_params(kwargs)
        response = request.get_paginated(self.endpoint(),
                                         self.pagination_key(), self.max_pages,
                                         params=params)
        return response

    def describe(self, object_id):
        """Get the detailed configuration by ID

        Args:
            object_id (str): ID to retrieve detailed configuration information
                for

        Returns:
            dict: dictionary object representing the entire object.

        """

        request = HttpHelper(self.session)
        describe_endpoint = "%s/%s" % (self.endpoint(), object_id)
        return request.get(describe_endpoint)[self.object_key()]

    def create(self, object_body):
        """Create from JSON document.

        Returns the ID of the new object
        """

        request = HttpHelper(self.session)
        request_body = utility.policy_to_dict(object_body)
        return request.post(self.endpoint(),
                            request_body)[self.object_key()]["id"]

    def delete(self, object_id):
        """Delete by ID.  Success returns None"""
        sanity.validate_object_id(object_id)
        request = HttpHelper(self.session)
        delete_endpoint = "%s/%s" % (self.endpoint(), object_id)
        request.delete(delete_endpoint)
        return None

    def update(self, object_body):
        """Update.  Success returns None"""
        request = HttpHelper(self.session)
        request_body = utility.policy_to_dict(object_body)
        object_id = request_body[self.object_key()]["id"]
        sanity.validate_object_id(object_id)
        update_endpoint = "%s/%s" % (self.endpoint(), object_id)
        request.put(update_endpoint, request_body)
        return None
