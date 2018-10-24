import cloudpassage
import os
import pytest


config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


class TestIntegrationServer:
    def build_server_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        server_object = cloudpassage.Server(session)
        print(key_id)
        return(server_object)

    def build_server_group_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        server_group_object = cloudpassage.ServerGroup(session)
        return(server_group_object)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.Server(session)

    def test_get_server_details(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active servers, this test will fail.
        """
        s = self.build_server_object()
        s_group = self.build_server_group_object()
        server_group_list = s_group.list_all()
        target_group = None
        for group in server_group_list:
            if group["server_counts"]["active"] != 0:
                target_group = group["id"]
                break
        assert target_group is not None
        target_server_id = s_group.list_members(target_group)[0]["id"]
        assert "id" in s.describe(target_server_id)

    def test_get_server_details_404(self):
        request = self.build_server_object()
        bad_server_id = "123456789"
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            request.describe(bad_server_id)
        assert bad_server_id in str(e)

    def test_retire_server_404(self):
        request = self.build_server_object()
        server_id = "12345"
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            request.retire(server_id)
        assert server_id in str(e)

    def test_issues_404(self):
        rejected = False
        request = self.build_server_object()
        server_id = "12345"
        try:
            request.issues(server_id)
        except cloudpassage.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_firewall_logs_422(self):
        rejected = False
        request = self.build_server_object()
        server_id = "12345"
        try:
            request.get_firewall_logs(server_id, 10)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_command_details_404(self):
        request = self.build_server_object()
        server_id = "12345"
        command_id = "56789"
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            request.command_details(server_id, command_id)
        assert server_id in str(e)

    def test_server_list(self):
        """This test requires at least one active server in your Halo
        account.  If you don't have an active server in your account, this
        test will fail.
        """
        s = self.build_server_object()
        result = s.list_all()
        assert "id" in result[0]

    def test_get_server_by_group_name(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active servers, this test will fail.
        """
        s = self.build_server_object()
        s_group = self.build_server_group_object()
        server_group_list = s_group.list_all()
        target_group = None
        for group in server_group_list:
            if group["server_counts"]["active"] != 0:
                target_group = group["name"]
                break
        assert target_group is not None
        servers = s.list_all(group_name=target_group)
        for server in servers:
            assert server["group_name"] == target_group

    def test_server_list_inactive_test1(self):
        """This test requires at least one active or inactive server in your
        Halo account.  If you don't have a server marked active or inactive
        in your account, this test will fail.
        """
        states = ["deactivated", "active"]
        s = self.build_server_object()
        result = s.list_all(state=states)
        assert "id" in result[0]

    def test_server_list_inactive_test2(self):
        """This test requires one server in your account with a status of
        deactivated.  If no such server exists in your account, the
        test will fail.
        """
        states = ["deactivated"]
        s = self.build_server_object()
        result = s.list_all(state=states)
        assert result[0]["state"] == "deactivated"

    def test_server_local_account(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        s = self.build_server_object()
        srv = s.list_all()[0]
        result = s.list_local_accounts(server_id=srv["id"])
        assert "username" in result[0]

    def test_server_local_account_detail(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        s = self.build_server_object()
        targeted_srv = s.list_all()[0]
        srv_local_a = s.list_local_accounts(server_id=targeted_srv["id"])[0]
        result = s.describe_local_account(server_id=targeted_srv["id"],
                                          username=srv_local_a["username"])
        assert result["username"] == srv_local_a["username"]

    def test_list_connections(self):
        server = self.build_server_object()
        servers = server.list_all()
        target_srv_id = servers[0]["id"]
        connections = server.list_connections(target_srv_id)
        assert isinstance(connections, list)

    def test_list_processes(self):
        server = self.build_server_object()
        servers = server.list_all()
        target_srv_id = servers[0]["id"]
        processes = server.list_processes(target_srv_id)
        assert isinstance(processes, list)
