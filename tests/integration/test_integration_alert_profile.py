import cloudpassage
import json
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


class TestIntegrationAlertProfiles:
    def create_alert_profile_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return cloudpassage.AlertProfile(session)

    def create_http_helper_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return cloudpassage.HttpHelper(session)

    def test_instantiation(self):
        assert self.create_alert_profile_obj()

    def test_list_all(self):
        """This gets a list of alert profiles from the Halo API.  It will
        fail if there are no alert profiles configured for your account."""
        profile = self.create_alert_profile_obj()
        profile_list = profile.list_all()
        assert "id" in profile_list[0]

    def test_get_details(self):
        """This test gets the details of an alert profile policy in your
        Halo account.  If you don't have any alert profile policies configured,
        it will fail.
        """
        request = self.create_alert_profile_obj()
        policy_list = request.list_all()
        target_policy_id = policy_list[0]["id"]
        target_policy_body = request.describe(target_policy_id)
        assert "id" in target_policy_body

    def test_create_delete(self):
        """This test attempts to create and delete an alert profile
        policy.
        """
        deleted = False
        profile = self.create_alert_profile_obj()
        http = self.create_http_helper_obj()
        user_id = http.get('/v2/users')['users'][0]['id']
        raw_policy_body = {
            "alert_profile": {
                "name": "CPAPI TEST Alert Profile",
                "frequency": "instant",
                "alert_profile_users": [{
                    "user_id": user_id,
                    "non_critical": "true",
                    "critical": "true"
                }]
            }
        }
        policy_body = json.dumps(raw_policy_body, indent = 2)
        policy_id = profile.create(policy_body)
        profile.delete(policy_id)
        try:
            profile.describe(policy_id)
        except cloudpassage.CloudPassageResourceExistence:
            deleted = True
        assert deleted

    def test_create_update_delete(self):
        """This test attempts to create, update, then delete an alert profile
        policy.
        """
        deleted = False
        profile = self.create_alert_profile_obj()
        http = self.create_http_helper_obj()
        newname = "Functional Test Name Change"
        user_id = http.get('/v2/users')['users'][0]['id']
        raw_policy_body = {
            "alert_profile": {
                "name": "CPAPI TEST Alert Profile Update",
                "frequency": "instant",
                "alert_profile_users": [{
                    "user_id": user_id,
                    "non_critical": "true",
                    "critical": "true"
                }]
            }
        }
        policy_body = json.dumps(raw_policy_body, indent = 2)
        policy_id = profile.create(policy_body)
        policy_endpoint = "/v1/%s/%s" % (profile.policies,policy_id)
        policy_update = http.get(policy_endpoint)
        policy_update[profile.policy]["name"] = newname
        profile.update(policy_update)
        profile.delete(policy_id)
        try:
            profile.describe(policy_id)
        except cloudpassage.CloudPassageResourceExistence:
            deleted = True
        assert deleted

