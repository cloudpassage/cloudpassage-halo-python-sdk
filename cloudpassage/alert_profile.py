"""AlertProfile class"""

import cloudpassage.sanity as sanity
from cloudpassage.policy import Policy
from cloudpassage.http_helper import HttpHelper
import cloudpassage.utility as utility


class AlertProfile(Policy):
    """Initializing the AlertProfile class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "alert_profile"
    policies = "alert_profiles"

    @classmethod
    def endpoint(cls):
        """Defines endpoint for API requests"""
        return "/v1/%s" % AlertProfile.policies

    @classmethod
    def policy_key(cls):
        return AlertProfile.policy

    @classmethod
    def pagination_key(cls):
        """Defines the pagination key for parsing paged results"""
        return AlertProfile.policies

    def create(self, policy_body):
        """Creates a policy from JSON document.

        Returns the ID of the new policy
        """

        request = HttpHelper(self.session)
        request_body = utility.policy_to_dict(policy_body)
        return request.post(self.endpoint(),
                            request_body)["id"]

    def delete(self, policy_id):
        """Delete a policy by ID.  Success returns None"""
        sanity.validate_object_id(policy_id)
        request = HttpHelper(self.session)
        delete_endpoint = "%s/%s" % (self.endpoint(), policy_id)
        request.delete(delete_endpoint)
        return None

    def update(self, policy_body):
        """Update a policy.  Success returns None"""

        request = HttpHelper(self.session)
        request_body = utility.policy_to_dict(policy_body)
        policy_id = request_body[self.policy_key()]["id"]
        sanity.validate_object_id(policy_id)
        update_endpoint = "%s/%s" % (self.endpoint(), policy_id)
        request.put(update_endpoint, request_body)
        return None
