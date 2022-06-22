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


class TestIntegrationIssue:
    def build_issue_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        issue_object = cloudpassage.Issue(session)
        return(issue_object)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.Issue(session)

    def test_get_issue_list(self):
        """This test requires at least one active issue in your Halo
        account.  If you have no active issues, this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all()
        assert issue_list is not None

    def test_get_issue_details(self):
        """This test requires at least one active issue in your Halo
        account.  If you have no active issues, this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all()
        assert issue_list is not None
        target_issue_id = issue_list[0]["id"]
        issue_details = i.describe(target_issue_id)
        assert issue_details["issue"]["id"] == target_issue_id

    def test_get_issue_details_404(self):
        request = self.build_issue_object()
        bad_issue_id = "91ea293e36dc11e9805c3d99d1900b44"
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            request.describe(bad_issue_id)
        assert bad_issue_id in str(e)

    def test_issue_list_actives(self):
        """This test requires at least one active issue in your Halo
        account.  If you have no active issues, this test will fail.
        """
        status = "active"
        i = self.build_issue_object()
        result = i.list_all(status=status)
        assert result is not None
        for issue in result:
            assert issue["status"] == "active"

    def test_issue_list_resolved(self):
        """This test requires at least one resolved issue in your Halo
        account.  If you have no resolved issues, this test will fail.
        """
        status = "resolved"
        i = self.build_issue_object()
        result = i.list_all(status=status)
        assert result is not None
        for issue in result:
            assert issue["status"] == "resolved"
    
    # Deprecated method
    '''
    def test_get_issue_by_agent_id(self):
        """This test requires at least one active issue in your Halo
        account.  If you have no active issues, this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all()
        assert issue_list is not None

        target_agent_id = issue_list[0]["agent_id"]
        issues = i.list_all(agent_id=target_agent_id)
        assert issues is not None

        for issue in issues:
            assert issue["agent_id"] == target_agent_id
    '''

    def test_get_issue_by_id(self):
        """This test requires at least one active issue in your Halo
        account.  If you have no active issues, this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all()
        assert issue_list is not None

        target_id = issue_list[0]["id"]
        issues = i.list_all(id=target_id)
        assert issues is not None

        for issue in issues:
            assert issue["id"] == target_id

    def test_get_issue_by_group_id(self):
        """This test requires at least one active issue in your Halo
        account.  If you have no active issues, this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all()
        assert issue_list is not None

        target_group_id = issue_list[0]["group_id"]
        issues = i.list_all(group_id=target_group_id)
        assert issues is not None

        for issue in issues:
            assert issue["group_id"] == target_group_id

    def test_get_issue_by_critical(self):
        """This test requires at least one active critical issue in your Halo
        account.  If you have no active critical issues, this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all(critical=True)
        assert issue_list is not None

        for issue in issue_list:
            assert issue["critical"]

    def test_get_issue_by_noncritical(self):
        """This test requires at least one active non-critical issue in your
        Halo account.  If you have no non-critical issues, this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all(critical=False)
        assert issue_list is not None

        for issue in issue_list:
            assert issue["critical"] is False

    def test_get_issue_by_policy_id(self):
        """This test requires at least one active issue with a policy id in
        your Halo account else this test will fail.
        """
        i = self.build_issue_object()
        issue_list = i.list_all(critical=False)
        assert issue_list
        for issue in issue_list:
            print(issue["policy_id"])
            if issue["policy_id"] != "null_value":
                policy_id = issue["policy_id"]
                break
        assert policy_id

        issue_list_by_policy = i.list_all(policy_id=policy_id)
        assert issue_list_by_policy is not None

        for issue in issue_list_by_policy:
            assert issue["policy_id"] == policy_id
