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


class TestIntegrationCveExceptions:
    def build_ce_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_hostname=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        cve_ex_obj = cloudpassage.CveExceptions(session)
        return cve_ex_obj

    def build_server_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        server_object = cloudpassage.Server(session)
        return(server_object)

    def test_instatiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.CveExceptions(session)

    def test_list_all(self):
        ce_obj = self.build_ce_object()
        cve_exs = ce_obj.list_all()
        assert "id" in cve_exs[0]

    def test_cve_exception_describe(self):
        ce_obj = self.build_ce_object()
        cve_exs = ce_obj.list_all()
        target_cve_id = cve_exs[0]["id"]
        target_cve = ce_obj.describe(target_cve_id)
        assert target_cve["id"] == target_cve_id

    def test_cve_exception_cud(self):
        ce_obj = self.build_ce_object()
        srv_obj = self.build_server_object()
        srvs = srv_obj.list_all()
        # target_srv_id = srvs[0]["id"] # deprecated
        package_name = "apport"
        package_version = "2.14.1-0ubuntu3.11"
        target_type = "server"
        # scope = "server" # deprecated
        # ce_id = ce_obj.create(package_name, package_version, target_type, target_srv_id) # deprecated
        ce_id = ce_obj.create(package_name, package_version, target_type)
        # ce_obj.update(ce_id, scope="all") # deprecated 
        ce_obj.update(ce_id, target_type="server")
        delete_return = ce_obj.delete(ce_id)
        assert delete_return is None

    # deprecated
    '''
    def test_scope_id_is_strings(self):
        request = self.build_ce_object()
        package_name = "apport"
        package_version = "2.14.1-0ubuntu3.11"
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            request.create(package_name, package_version, "server", "#$123dfe")
        assert "valid scope id" in str(e)
    '''