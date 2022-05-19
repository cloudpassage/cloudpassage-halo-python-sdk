import imp
import os
import pprint
import pytest
import sys

from datetime import datetime, timedelta
from cloudpassage.utility import Utility as utility


module_name = 'cloudpassage'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage = imp.load_module(module_name, fp, pathname, description)


class TestIntegrationTimeSeries(object):
    def get_halo_session(self):
        config_file_name = "portal.yaml.local"
        tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "../"))
        config_file = os.path.join(tests_dir, "configs/", config_file_name)
        session_info = cloudpassage.ApiKeyManager(config_file=config_file)
        key_id = session_info.key_id
        secret_key = session_info.secret_key
        api_hostname = session_info.api_hostname
        api_port = session_info.api_port
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        return session

    def test_time_series_iter_events_many_pages_fail(self):
        """Test against events endpoint."""
        session = self.get_halo_session()
        start_time = utility.datetime_to_8601((datetime.now() -
                                               timedelta(30)))
        start_url = "/v1/eventss"
        item_key = "events"
        with pytest.raises(cloudpassage.CloudPassageValidation):
            cloudpassage.TimeSeries(session, start_time,
                                    start_url, item_key)
            assert False  # Should bail and never hit this assertion.
        assert True

    def test_time_series_iter_events_many_pages(self):
        """Test against events endpoint."""
        session = self.get_halo_session()
        start_time = utility.datetime_to_8601((datetime.now() -
                                               timedelta(30)))
        start_url = "/v1/events"
        item_key = "events"
        streamer = cloudpassage.TimeSeries(session, start_time,
                                           start_url, item_key)
        dupes = []
        item_counter = 0
        item_ids = set([])
        for item in streamer:
            print("Item counter: %s Item ID: %s Item timestamp: %s" %
                  (item_counter, item["id"], item["created_at"]))
            assert "id" in item
            if item["id"] in item_ids:
                print("Duplicate ^^^")
                dupes.append(item["id"])
            item_ids.add(item["id"])
            item_counter += 1
            if item_counter > 60:
                break
        if dupes:
            print("Dupes:")
            pprint.pprint(dupes)
            assert False

    def test_time_series_iter_issues_many_pages(self):
        """Test against issues endpoint."""
        session = self.get_halo_session()
        start_time = utility.datetime_to_8601((datetime.now() -
                                               timedelta(30)))
        start_url = "/v3/issues"
        item_key = "issues"
        streamer = cloudpassage.TimeSeries(session, start_time,
                                           start_url, item_key)
        dupes = []
        item_counter = 0
        item_ids = set([])
        for item in streamer:
            print("Item counter: %s Item ID: %s Item timestamp: %s" %
                  (item_counter, item["id"], item["created_at"]))
            assert "id" in item
            if item["id"] in item_ids:
                print("Duplicate ^^^")
                dupes.append(item["id"])
            item_ids.add(item["id"])
            item_counter += 1
            if item_counter > 5:
                break
        if dupes:
            print("Dupes:")
            pprint.pprint(dupes)
            assert False

    def test_time_series_iter_scans_many_pages(self):
        """Test against scans endpoint."""
        session = self.get_halo_session()
        start_time = utility.datetime_to_8601((datetime.now() -
                                               timedelta(30)))
        start_url = "/v1/scans"
        item_key = "scans"
        streamer = cloudpassage.TimeSeries(session, start_time,
                                           start_url, item_key)
        dupes = []
        item_counter = 0
        item_ids = set([])
        for item in streamer:
            print("Item counter: %s Item ID: %s Item timestamp: %s" %
                  (item_counter, item["id"], item["created_at"]))
            assert "id" in item
            if item["id"] in item_ids:
                print("Duplicate ^^^")
                dupes.append(item["id"])
            item_ids.add(item["id"])
            item_counter += 1
            if item_counter > 5:
                break
        if dupes:
            print("Dupes:")
            pprint.pprint(dupes)
            assert False

    def test_time_series_iter_events_many_pages_internal_killswitch(self):
        """Test triggering exit w/ StopIteration in TimeSeries().__iter__()"""
        session = self.get_halo_session()
        start_time = utility.datetime_to_8601((datetime.now() -
                                               timedelta(30)))
        start_url = "/v1/events"
        item_key = "events"
        streamer = cloudpassage.TimeSeries(session, start_time,
                                           start_url, item_key)
        dupes = []
        item_counter = 0
        item_ids = set([])
        for item in streamer:
            print("Item counter: %s Item ID: %s Item timestamp: %s" %
                  (item_counter, item["id"], item["created_at"]))
            assert "id" in item
            if item["id"] in item_ids:
                print("Duplicate ^^^")
                dupes.append(item["id"])
            item_ids.add(item["id"])
            item_counter += 1
            if item_counter > 60:
                streamer.stop = True  # This triggers a StopIteration
        if dupes:
            print("Dupes:")
            pprint.pprint(dupes)
            assert False
