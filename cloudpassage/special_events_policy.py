"""SpecialEventsPolicy class"""


from cloudpassage.policy import Policy


class SpecialEventsPolicy(Policy):
    """Initializing the SpecialEventsPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "special_events_policy"
    policies = "special_events_policies"

    @classmethod
    def endpoint(cls):
        """Defines endpoint for API requests"""
        return "/v1/%s" % SpecialEventsPolicy.policies

    @classmethod
    def pagination_key(cls):
        """Defines the pagination key for parsing paged results"""
        return SpecialEventsPolicy.policies

    @classmethod
    def policy_key(cls):
        return SpecialEventsPolicy.policy

    def create(self, unimportant):
        """Not implemented for this module.  Raises exception."""
        raise NotImplementedError

    def delete(self, unimportant):
        """Not implemented for this module.  Raises exception."""
        raise NotImplementedError

    def update(self, unimportant):
        """Not implemented for this module.  Raises exception."""
        raise NotImplementedError
