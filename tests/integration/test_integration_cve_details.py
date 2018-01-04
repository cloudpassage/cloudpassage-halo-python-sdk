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


class TestIntegrationCveDetail:
    def build_cve_detail_object(self):
    	session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
    	cve_detail_object = cloudpassage.CveDetails(session)
    	return(cve_detail_object)

    def test_describe_cve(self):
    	cve_id = "CVE-2015-5722"
    	cve_obj = self.build_cve_detail_object()
    	cve_detail = cve_obj.describe(cve_id)
    	assert cve_detail["CVE"] == cve_id