"""ServerGroup class"""

import cloudpassage.utility as utility
import cloudpassage.sanity as sanity
from cloudpassage.http_helper import HttpHelper


class ServerGroup(object):
    """Initializing the ServerGroup class:

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
        """Returns a list of all groups for an account

        This is represented as a list of dictionaries

        This will only return a maximum of 20 pages, which amounts to
        200 groups.  If you have more than that, you should consider
        using the SDK within a multi-threaded application so you don't
        spend the rest of your life waiting on a list of groups.
        """

        session = self.session
        max_pages = 20
        key = "groups"
        endpoint = "/v1/groups"
        request = HttpHelper(session)
        groups = request.get_paginated(endpoint, key, max_pages)
        return groups

    def list_members(self, group_id):
        """Returns a list of all member servers of a group_id

        Args:
            group_id (str): ID of group_id

        Returns:
            list: List of dictionary objects describing member servers

        """

        endpoint = "/v1/groups/%s/servers" % group_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        servers = response["servers"]
        return servers

    def create(self, group_name, **kwargs):
        """Creates a ServerGroup.

        Args:
            group_name (str): Name for the new group

        Keyword Args:
            firewall_policy_id (str): ID of firewall policy to be assigned to \
            the group (deprecated- use linux_firewall_policy_id)
            linux_firewall_policy_id (str): ID of linux firewall policy to \
            associate with the new group
            windows_firewall_policy_id (str): ID of Windows firewall policy \
            to associate with the new group
            policy_ids (list): List of Linux configuration policy IDs
            windows_policy_ids (list): List of Windows configuration policy IDs
            fim_policy_ids (list): List of Linux FIM policies
            linux_fim_policy_ids (list): List of Linux FIM policies
            windows_fim_policy_ids (list): List of Windows FIM policies
            lids_policy_ids (list): List of LIDS policy IDs
            tag (str): Server group tag-used for auto-assignment of group.
            server_events_policy (str): Special events policy IDs
            alert_profiles (list): List of alert profile IDs

        Returns:
            str: ID of newly-created group.

        """

        endpoint = "/v1/groups"
        group_data = {"name": group_name, "policy_ids": [], "tag": None}
        body = {"group": utility.merge_dicts(group_data, kwargs)}
        request = HttpHelper(self.session)
        response = request.post(endpoint, body)
        return response["group"]["id"]

    def describe(self, group_id):
        """Describe a ServerGroup.  In detail.

        Args:
            group_id (str): ID of group

        Returns:
            dict: Dictionary object describing group.  In detail.

        """

        endpoint = "/v1/groups/%s" % group_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        group = response["group"]
        return group

    def update(self, group_id, **kwargs):
        """Updates a ServerGroup.

        Args:
            group_id (str): ID of group to be altered

        Keyword Args:
            name (str): Override name for group
            linux_firewall_policy_id (str): Override Linux firewall policy ID.
            windows_firewall_policy_id (str): Override Windows firewall \
            policy ID.
            policy_ids (list): Override Linux configuration policies
            windows_policy_ids (list): Override Windows firewall policies
            linux_fim_policy_ids (list): Override Linux firewall policies
            windows_fim_policy_ids (list): Override Windows FIM policies
            lids_policy_ids (list): Override LIDS policy IDs
            tag (str): Override server group tag
            special_events_policy (str): Override server events policy.  Note\
            the difference in naming from the \
            :meth:`cloudpassage.ServerGroup.create()` \
            method
            alert_profiles (list): List of alert profiles

        Returns:
            True if successful, throws exception otherwise.

        """

        sanity.validate_object_id(group_id)
        endpoint = "/v1/groups/%s" % group_id
        response = None
        group_data = {}
        body = {"group": utility.merge_dicts(group_data, kwargs)}
        request = HttpHelper(self.session)
        response = request.put(endpoint, body)
        return response

    def delete(self, group_id, **kwargs):
        """ Delete a server group.

        Args:
            group_id (str): ID of group to delete

        Keyword Args:
            force (bool): If set to True, the member servers from this group \
            will be moved to the parent group.

        Returns:
            None if successful, exceptions otherwise.

        """

        sanity.validate_object_id(group_id)
        endpoint = "/v1/groups/%s" % group_id
        request = HttpHelper(self.session)
        if ("force" in kwargs) and (kwargs["force"] is True):
            params = {"move_to_parent": "true"}
            request.delete(endpoint, params=params)
        else:
            request.delete(endpoint)
        return None
