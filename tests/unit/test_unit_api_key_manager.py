import cloudpassage
import os
import yaml


config_file_name = "portal.yaml.local.test"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname

api_key_id = "APIKEYSAMPLE000"
api_secret_key = "APISECRETKEYSAMPLE000"
api_hostname = "api.nonexist.cloudpassage.com"


class TestUnitApiKeyManager:
    def test_keys_from_env(self):
        os.environ['HALO_API_HOSTNAME'] = api_hostname
        os.environ['HALO_API_KEY'] = api_key_id
        os.environ['HALO_API_SECRET_KEY'] = api_secret_key
        session_config = cloudpassage.ApiKeyManager()
        assert session_config.key_id == api_key_id
        assert session_config.secret_key == api_secret_key
        assert session_config.api_hostname == api_hostname

    def test_keys_from_file(self):
        session = cloudpassage.ApiKeyManager(config_file=config_file)
        with open(config_file, 'r') as config_file_obj:
            file_set_vars = yaml.load(config_file_obj)["defaults"]
        assert session.key_id == file_set_vars["key_id"]
        assert session.secret_key == file_set_vars["secret_key"]
        assert session.api_hostname == file_set_vars["api_hostname"]
