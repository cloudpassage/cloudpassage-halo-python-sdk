"""Server class"""

import re
import cloudpassage.sanity as sanity
import cloudpassage.utility as utility
from cloudpassage.exceptions import CloudPassageValidation
from cloudpassage.http_helper import HttpHelper


class Server(object):
    """Initializing the Server class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        self.valid_server_states = ["active",
                                    "deactivated",
                                    "missing"]
        self.cve_validator = re.compile(r"^CVE-\d+-\d{4,}$")
        self.kb_validator = re.compile(r"^kb\d+$")
        self.platform_validator = re.compile(r"^[a-z]+$")
        self.supported_search_fields = ["state",
                                        "platform",
                                        "cve",
                                        "kb",
                                        "missing_kb"]
        return None

    def list_all(self, **kwargs):
        """Returns a list of all servers.

        This query is limited to 50 pages of 10 items,
        totaling 500 servers.

        Default filter returns only servers in the 'active' state.

        Keyword Args:
            state (list or str): A list or comma-separated string containing \
            any of these: active, missing, deactivated
            platform (list or str): A list or comma-separated string \
            containing any of these: \
            windows, debian, ubuntu, centos, oracle, rhel, etc...
            cve (str): CVE ID.  Example: CVE-2015-1234
            kb (str): Search for presence of KB.  Example: kb="KB2485376"
            missing_kb (str): Search for absence of KB.  \
            Example: mising_kb="KB2485376"

        Returns:
            list: List of dictionary objects describing servers

        """

        endpoint = "/v1/servers"
        key = "servers"
        max_pages = 50
        request = HttpHelper(self.session)
        criteria_valid = self.validate_server_search_criteria(kwargs)
        if criteria_valid is False:
            error_text = "Unsupported arguments in " + str(kwargs)
            raise CloudPassageValidation(error_text)
        params = utility.assemble_search_criteria(self.supported_search_fields,
                                                  kwargs)
        response = request.get_paginated(endpoint, key,
                                         max_pages, params=params)
        return response

    def assign_group(self, server_id, group_id):
        """Moves server to another group.

        Args:
            server_id (str): Target server's ID
            group_id (str): ID of group to move server to.

        Returns:
            True if successful, throws exceptions if it fails.

        """

        sanity.validate_object_id(server_id)
        endpoint = "/v1/servers/%s" % server_id
        request_body = {"server": {"group_id": group_id}}
        request = HttpHelper(self.session)
        request.put(endpoint, request_body)
        # Exception will throw if the prior line fails.
        return True

    def delete(self, server_id):
        """Deletes server indicated by server_id.

        Remember, deletion causes the removal of accociated security
        events and scan information.

        Args:
            server_id (str): ID of server to be deleted

        Returns:
            True if successful, throws exceptions otherwise.

        """

        sanity.validate_object_id(server_id)
        endpoint = "/v1/servers/%s" % server_id
        request = HttpHelper(self.session)
        request.delete(endpoint)
        # If no exception from request, we're successful
        return True

    def describe(self, server_id):
        """Get server details by server ID

        Args:
            server_id (str): Server ID

        Returns:
            dict: Dictionary object describing server

        """

        endpoint = "/v1/servers/%s" % server_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        server_details = response["server"]
        return server_details

    def retire(self, server_id):
        """This method retires a server

        Args:
            server_id (str): ID of server to be retired

        Returns:
            True if successful, throws exception on failure

        """

        sanity.validate_object_id(server_id)
        endpoint = "/v1/servers/%s" % server_id
        body = {"server":
                {"retire": True}}
        request = HttpHelper(self.session)
        request.put(endpoint, body)
        # Exceptions fire deeper if this fails.  Otherwise, return True.
        return True

    def firewall_logs(self, server_id):
        """This method retrieves the detail of a server firewall log. 

        Args:
            server_id (str): ID of server

        Returns:
            list: firewall log of the server
        """

        sanity.validate_object_id(server_id)
        endpoint = "/v1/servers/%s/firewall_logs" % server_id

        request = HttpHelper(self.session)
        response = request.get(endpoint)
        firewall_log_details = response["agent_firewall_logs"]
        return firewall_log_details

    def command_details(self, server_id, command_id):
        """This method retrieves the details and status of a server command.

        Args:
            server_id (str): ID of server runnung command
            command_id (str): ID of command running on server

        Returns:
            dict: Command status as a dictionary object.

        Example:

        ::

            {
              "name": "",
              "status: "",
              "created_at": "",
              "updated_at": "",
              "result": ""
             }


        For server account creation and server account password resets, \
        the password will be contained in the result field, as a dictionary:


        ::

            {
              "name": "",
              "status: "",
              "created_at": "",
              "updated_at": "",
              "result": {
                         "password": ""
                         }
            }


        """

        endpoint = "/v1/servers/%s/commands/%s" % (server_id, command_id)
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        command_status = response["command"]
        return command_status

    def validate_server_search_criteria(self, criteria):
        """Validate arguments for Server query"""
        arguments_valid = True
        if "state" in criteria:
            if not self.validate_server_state(criteria["state"]):
                arguments_valid = False
        if "platform" in criteria:
            if not self.validate_platform(criteria["platform"]):
                arguments_valid = False
        if "cve" in criteria:
            if not self.validate_cve_id(criteria["cve"]):
                arguments_valid = False
        if "kb" in criteria:
            if not self.validate_kb_id(criteria["kb"]):
                arguments_valid = False
        if "missing_kb" in criteria:
            if not self.validate_kb_id(criteria["missing_kb"]):
                arguments_valid = False
        return arguments_valid

    def validate_server_state(self, states):
        """Ensure that server state in query is valid"""
        if isinstance(states, list):
            for state in states:
                if state not in self.valid_server_states:
                    return False
        else:
            if states not in self.valid_server_states:
                return False
        return True

    def validate_platform(self, platforms):
        """Validate platform in query is valid"""
        if isinstance(platforms, list):
            for platform in platforms:
                if not self.platform_validator.match(platform):
                    return False
        else:
            if not self.platform_validator.match(platforms):
                return False
        return True

    def validate_cve_id(self, cve_ids):
        """Validate CVE ID designation"""
        if isinstance(cve_ids, list):
            for cve_id in cve_ids:
                if not self.cve_validator.match(cve_id):
                    return False
        else:
            if not self.cve_validator.match(cve_ids):
                return False
        return True

    def validate_kb_id(self, kb_ids):
        """Validate KB ID is valid"""
        if isinstance(kb_ids, list):
            for kb_id in kb_ids:
                if not self.kb_validator.match(kb_id):
                    return False
        else:
            if not self.kb_validator.match(kb_ids):
                return False
        return True
