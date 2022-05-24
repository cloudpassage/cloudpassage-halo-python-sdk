"""ServerGroup class"""

from .utility import Utility as utility
import cloudpassage.sanity as sanity
from .http_helper import HttpHelper
from .halo_endpoint import HaloEndpoint


class ServerGroup(HaloEndpoint):
    """Initializing the ServerGroup class:


    Filters for ServerGroup queries can be found in the API documentation.
    See here: https://api-doc.cloudpassage.com/help#object-representation-1
    for more information.

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    object_name = "group"
    objects_name = "groups"
    default_endpoint_version = 1

    def endpoint(self):
        """Return endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)

    @classmethod
    def pagination_key(cls):
        """Defines the pagination key for parsing paged results"""
        return ServerGroup.objects_name

    @classmethod
    def object_key(cls):
        """Defines the key used to pull the policy from the json document"""
        return ServerGroup.object_name

    def list_members(self, group_id):
        """Returns a list of all member servers of a group_id

        Args:
            group_id (str): ID of group_id

        Returns:
            list: List of dictionary objects describing member servers

        """
        sanity.validate_object_id(group_id)
        # endpoint = "/v1/groups/{}/servers".format(group_id) # Invalid Endpoint
        endpoint = "/v1/servers?group_id={}".format(group_id)
        request = HttpHelper(self.session)
        return request.get(endpoint)["servers"]

    def create(self, group_name, **kwargs):
        """Creates a ServerGroup.

        Args:
            group_name (str): Name for the new group

        Keyword Args:
            firewall_policy_id (str): ID of firewall policy to be assigned to
                the group (deprecated- use linux_firewall_policy_id)
            linux_firewall_policy_id (str): ID of linux firewall policy to
                associate with the new group
            windows_firewall_policy_id (str): ID of Windows firewall policy
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
        endpoint = self.endpoint()
        group_data = {"name": group_name, "policy_ids": [], "tag": None}
        body = {"group": utility.merge_dicts(group_data, kwargs)}
        request = HttpHelper(self.session)
        response = request.post(endpoint, body)
        return response["group"]["id"]

    def update(self, group_id, **kwargs):
        """Updates a ServerGroup.

        Args:
            group_id (str): ID of group to be altered

        Keyword Args:
            name (str): Override name for group
            linux_firewall_policy_id (str): Override Linux firewall policy ID.
            windows_firewall_policy_id (str): Override Windows firewall policy
                ID.
            policy_ids (list): Override Linux configuration policies
            windows_policy_ids (list): Override Windows firewall policies
            linux_fim_policy_ids (list): Override Linux firewall policies
            windows_fim_policy_ids (list): Override Windows FIM policies
            lids_policy_ids (list): Override LIDS policy IDs
            tag (str): Override server group tag
            special_events_policy (str): Override server events policy.  Note
                the difference in naming from the
                :meth:`cloudpassage.ServerGroup.create()` method
            alert_profiles (list): List of alert profiles

        Returns:
            True if successful, throws exception otherwise.

        """
        sanity.validate_object_id(group_id)
        endpoint = "{}/{}".format(self.endpoint(), group_id)
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
            force (bool): If set to True, the member servers from this group
                will be moved to the parent group.

        Returns:
            None if successful, exceptions otherwise.

        """

        sanity.validate_object_id(group_id)
        endpoint = "{}/{}".format(self.endpoint(), group_id)
        request = HttpHelper(self.session)
        if ("force" in kwargs) and (kwargs["force"] is True):
            params = {"move_to_parent": "true"}
            request.delete(endpoint, params=params)
        else:
            request.delete(endpoint)
        return None

    def migrate_servers(self, grp_id, server_ids, srv_state=None):
        """Migrate servers in server_ids into the group identified by group_id.

        Args:
            grp_id (str): ID of group to merge
            server_ids (list): A list of server_id
            srv_state (str): A comma-separated string containing filters to
                be applied to the list of servers to be migrated. Valid filters
                are `active`, `missing`, `deactivated`, and `retired`

        Returns:
            server ids (list): A list of all server_id in the identified server
            group.

        """
        if not srv_state:
            srv_state = "active,missing,deactivated,retired"

        srv_ids = []
        body = {
            "server": {
                "group_id": grp_id
            }
        }
        sanity.validate_object_id(grp_id)
        for server_id in server_ids:
            sanity.validate_object_id(server_id)
            endpoint = "/v1/servers/{}".format(server_id)
            request = HttpHelper(self.session)
            request.put(endpoint, body)

        sgrp_endpoint = "/v1/groups/{}/servers".format(grp_id)
        params = {"state": srv_state}
        response = request.get(sgrp_endpoint, params=params)
        srv_list = response["servers"]
        for srv in srv_list:
            srv_ids.append(srv["id"])
        return srv_ids

    def list_connections(self, group_id, **kwargs):
        """Return all recently detected connections in the server group.

        Args:
            server_id (str): Group ID

        Returns:
            list: List of all recently detected connections in the server group

        """
        endpoint = "/v1/groups/{}/connections".format(group_id)
        params = utility.sanitize_url_params(kwargs)
        request = HttpHelper(self.session)
        response = request.get(endpoint, params=params)
        connections = response["connections"]
        return connections
