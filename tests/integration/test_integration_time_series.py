import imp
import os
import sys

from datetime import datetime, timedelta


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

    def test_time_series_iter_events_many_pages(self):
        session = self.get_halo_session()
        start_time = cloudpassage.utility.datetime_to_8601((datetime.now() -
                                                            timedelta(7)))
        start_url = "/v1/events"
        item_key = "events"
        event_streamer = cloudpassage.TimeSeries(session, start_time,
                                                 start_url, item_key)
        event_counter = 0
        event_ids = set([])
        for event in event_streamer:
            assert "id" in event
            assert event["id"] not in event_ids
            event_ids.add(event["id"])
            event_counter += 1
            if event_counter > 60:
                break
