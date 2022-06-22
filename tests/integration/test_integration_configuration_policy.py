import cloudpassage
import json
import os
import pytest
from cloudpassage.utility import Utility as utility

config_file_name = "portal.yaml.local"
policy_file_name = "cis-benchmark-for-centos-7-v1.policy.json"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_file = os.path.join(tests_dir, 'policies/', policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


class TestIntegrationConfigurationPolicy:
    def build_config_policy_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        return_obj = cloudpassage.ConfigurationPolicy(session)
        return(return_obj)

    def remove_policy_by_name(self, policy_name):
        config_policy_obj = self.build_config_policy_object()
        policy_list = config_policy_obj.list_all()
        for policy in policy_list:
            if policy["name"] == policy_name:
                config_policy_obj.delete(policy["id"])

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.ConfigurationPolicy(session)

    def test_list_all(self):
        """This test gets a list of configuration policies from the Halo API.
        If you have no configuration policies in your account, it will fail
        """
        request = self.build_config_policy_object()
        response = request.list_all()
        assert "id" in response[0]

    def test_get_details(self):
        """This test gets the details of a configuration policy in your
        Halo account.  If you don't have any policies configured,
        it will fail.
        """
        request = self.build_config_policy_object()
        policy_list = request.list_all()
        target_policy_id = policy_list[0]["id"]
        target_policy_body = request.describe(target_policy_id)
        assert "id" in target_policy_body

    def test_configuration_policy_create_delete(self):
        """This test attempts to create and delete a configuration
        policy.
        """
        request = self.build_config_policy_object()
        # newname = "Functional Test Name Change"
        with open(policy_file, 'r') as policy_file_object:
            policy_body = policy_file_object.read()
        pol_meta = utility.determine_policy_metadata(policy_body)
        self.remove_policy_by_name(pol_meta["policy_name"])
        pol_dict = json.loads(policy_body)
        pol_dict["policy"]["name"] = "tm_testpolicy_11"
        policy_id = request.create(json.dumps(pol_dict))
        request.delete(policy_id)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            request.describe(policy_id)
        assert policy_id in str(e)

    def test_configuration_policy_create_update_delete(self):
        """This test attempts to create, update, then delete a configuration
        policy.
        """
        request = self.build_config_policy_object()
        newname = "Functional Test Name Change"
        self.remove_policy_by_name(newname)
        with open(policy_file, 'r') as policy_file_object:
            policy_body = policy_file_object.read()
        policy_id = request.create(policy_body)
        policy_update = json.loads(policy_body)
        policy_update["policy"]["name"] = newname
        policy_update["policy"]["id"] = policy_id
        request.update(policy_update)
        request.delete(policy_id)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            request.describe(policy_id)
        assert policy_id in str(e)
