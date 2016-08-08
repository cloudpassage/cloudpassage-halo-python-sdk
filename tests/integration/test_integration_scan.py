import cloudpassage
import datetime
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


class TestIntegrationScan:
    def get_fim_scan_with_findings(self):
        scan_type = "fim"
        scan_status = "completed_clean"
        scanner = self.build_scan_object()
        report = scanner.scan_history(module=scan_type, status=scan_status)
        for item in report:
            if (item["critical_findings_count"] >= 0 or
                    item["non_critical_findings_count"] >= 0):
                return item["id"]
        return None

    def build_scan_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return_obj = cloudpassage.Scan(session)
        return(return_obj)

    def build_server_group_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return_obj = cloudpassage.ServerGroup(session)
        return(return_obj)

    def build_server_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return_obj = cloudpassage.Server(session)
        return(return_obj)

    def get_svm_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            target_group_id = g["id"]
            num_members = g["server_counts"]["active"]
            if num_members > 0:
                members = s_group.list_members(target_group_id)
                target_id = members[0]["id"]
                break
        return(target_id)

    def get_csm_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            csm_policies = g["policy_ids"]
            num_members = g["server_counts"]["active"]
            if num_members > 0 and len(csm_policies) > 0:
                members = s_group.list_members(g["id"])
                target_id = members[0]["id"]
                break
        return(target_id)

    def get_fim_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            fim_policies = g["fim_policy_ids"]
            num_members = g["server_counts"]["active"]
            if num_members > 0 and len(fim_policies) > 0:
                members = s_group.list_members(g["id"])
                target_id = members[0]["id"]
                break
        return(target_id)

    def get_sam_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            num_members = g["server_counts"]["active"]
            if num_members > 0:
                members = s_group.list_members(g["id"])
                for member in members:
                    if member["platform"] != "windows":
                        return members[0]["id"]
        return(target_id)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.Scan(session)

    def test_bad_scan_type(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        scanner = cloudpassage.Scan(session)
        s_group = cloudpassage.ServerGroup(session)
        scan_type = "barfola"
        server_id = s_group.list_all()[0]["id"]
        try:
            command = scanner.initiate_scan(server_id, scan_type)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_bad_server_id(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        scanner = cloudpassage.Scan(session)
        scan_type = "svm"
        server_id = "ABC123"
        try:
            command = scanner.initiate_scan(server_id, scan_type)
        except cloudpassage.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_sam_historical_is_unsupported(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        scanner = cloudpassage.Scan(session)
        server = cloudpassage.Server(session)
        scan_type = "sam"
        server_id = server.list_all()[0]["id"]
        try:
            command = scanner.last_scan_results(server_id, scan_type)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_scan_type_valid(self):
        valid_types = ["svm", "sva", "csm", "sca", "fim", "sam", "sv"]
        invalid_types = ["death_stare", "lids"]
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        scanner = cloudpassage.Scan(session)
        for v in valid_types:
            assert scanner.scan_type_supported(v)
        for i in invalid_types:
            assert not scanner.scan_type_supported(i)

    def test_sv_initiate(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        command = scanner.initiate_scan(target_id, "sv")
        assert command["id"]

    def test_sca_initiate(self):
        sca_aliases = ["sca", "csm"]
        scanner = self.build_scan_object()
        target_id = self.get_csm_target()
        for alias in sca_aliases:
            command = scanner.initiate_scan(target_id, alias)
            assert command["id"]

    def test_sca_retrieve(self):
        sca_aliases = ["sca", "csm"]
        scanner = self.build_scan_object()
        target_id = self.get_csm_target()
        for alias in sca_aliases:
            report = scanner.last_scan_results(target_id, alias)
            assert report["id"]

    def test_fim_initiate(self):
        scanner = self.build_scan_object()
        target_id = self.get_fim_target()
        command = scanner.initiate_scan(target_id, 'fim')
        assert command["id"]

    def test_fim_retrieve(self):
        scanner = self.build_scan_object()
        target_id = self.get_fim_target()
        report = scanner.last_scan_results(target_id, 'fim')
        assert report["id"]

    def test_svm_initiate(self):
        svm_aliases = ["svm", "sva"]
        scanner = self.build_scan_object()
        target_id = self.get_svm_target()
        for alias in svm_aliases:
            command = scanner.initiate_scan(target_id, alias)
            assert command["id"]

    def test_svm_retrieve(self):
        svm_aliases = ["svm", "sva"]
        scanner = self.build_scan_object()
        target_id = self.get_svm_target()
        for alias in svm_aliases:
            report = scanner.last_scan_results(target_id, alias)
            assert report["id"]

    def test_sam_initiate(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        command = scanner.initiate_scan(target_id, "sam")
        assert command["id"]

    def test_sam_retrieve(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.last_scan_results(target_id, "sam")
        assert report["id"]

    def test_scan_history(self):
        scanner = self.build_scan_object()
        report = scanner.scan_history()
        assert report[0]["id"]

    """
    def test_scan_history_by_serverid(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(server_id=target_id)
        assert report[0]["server_id"] == target_id
    """

    def test_scan_history_by_single_scan_type(self):
        """This test requires a completed SAM scan.  If you don't have one
        in your account, this scan will fail.
        """
        scan_type = "sam"
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(module=scan_type, max_pages=2)
        assert report[0]["module"] == scan_type

    def test_scan_history_by_multi_scan_type(self):
        """This test requires a completed SAM and SVM scan.  If your account
        doesn't have results from both of these scan types, the test will
        fail.
        """
        scan_types = ["sam", "svm"]
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(module=scan_types, max_pages=2)
        assert report[0]["module"] in scan_types

    def test_scan_history_by_single_status(self):
        """This test requires scan results in your account with a status
        of completed_clean.  If you don't have any scan results with
        this status, this test will fail.
        """
        scan_status = "completed_clean"
        scanner = self.build_scan_object()
        report = scanner.scan_history(status=scan_status, max_pages=2)
        assert report[0]["status"] == scan_status

    """
    def test_scan_history_by_multi_status(self):
        scan_status = ["completed_clean", "completed_with_errors"]
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(status=scan_status, max_pages=2)
        assert report[0]["status"] in scan_status

    def test_scan_details(self):
        scanner = self.build_scan_object()
        target_id = self.get_fim_target()
        report = scanner.scan_history(server_id=target_id)
        details = scanner.scan_details(report[0]["id"])
        assert "id" in details
    """

    def test_fim_findings_details(self):
        """This test requires a FIM scan with findings.  If you don't
        have a FIM scan with resulting findings, this test will fail.
        """
        target_fim_scan_id = self.get_fim_scan_with_findings()
        scanner = self.build_scan_object()
        details = scanner.scan_details(target_fim_scan_id)
        findings = details["findings"]
        target_finding = findings[0]["id"]
        target_findings_body = scanner.findings(target_fim_scan_id,
                                                target_finding)
        assert "id" in target_findings_body

    def test_scan_history_by_date(self):
        """This test requires scan results in your account, produced in the
        last week.  If no such records exist, this test will fail.
        """
        scan = self.build_scan_object()
        until = cloudpassage.utility.time_string_now()
        since = datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
        scan_list = scan.scan_history(max_pages=2, since=since, until=until)
        assert "id" in scan_list[0]


class TestIntegrationCveException:
    def create_cve_exception_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return_obj = cloudpassage.CveException(session)
        return(return_obj)

    def test_instantiation(self):
        assert self.create_cve_exception_object()

    def test_get_list(self):
        """Your account must have at least one CVE exception set.
        If you haven't set any CVE exceptions in your account,
        this test will fail.
        """
        cve_exc = self.create_cve_exception_object()
        list_of_exceptions = cve_exc.list_all()
        assert "id" in list_of_exceptions[0]

    def test_get_details(self):
        """Your account must have at least one CVE exception set.
        If you haven't set any CVE exceptions in your account,
        this test will fail.
        """
        cve_exc = self.create_cve_exception_object()
        list_of_exceptions = cve_exc.list_all()
        details = cve_exc.describe(list_of_exceptions[0]["id"])
        assert "id" in details
