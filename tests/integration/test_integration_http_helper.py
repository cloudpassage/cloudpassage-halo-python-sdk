import cloudpassage
import datetime
import hashlib
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

nonexistent_url = "/v1/does_not_exist"
# This will make cleaning up easier...
content_prefix = '_SDK_test-'
d_hash = hashlib.md5(datetime.datetime.now().isoformat().encode()).hexdigest()
content_name = (content_prefix + d_hash)


class TestIntegrationGet:
    def test_get_404(self):
        endpoint = nonexistent_url
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.get(endpoint)
        assert '404' in str(e)

    def test_get_rekey(self):
        endpoint = "/v1/servers"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        json_response = req.get(endpoint)
        assert "servers" in json_response


class TestIntegrationGetPaginated:
    def test_get_paginated_404(self):
        endpoint = nonexistent_url
        key = "noexist"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.get_paginated(endpoint, key, pages)
        assert '404' in str(e)

    def test_get_paginated_rekey(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_events_99(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        req = cloudpassage.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_toomany(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 301
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            req.get_paginated(endpoint, key, pages)
        assert '300 max.' in str(e)

    def test_get_paginated_badkey(self):
        endpoint = "/v1/events"
        key = "badkey"
        pages = 2
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            req.get_paginated(endpoint, key, pages)
        assert key in str(e)

    def test_get_next_page_path(self):
        body = {u'count': 6961,
                u'issues': [],
                u'pagination': {u'next': u'https://api.cloudpassage.com/v3/issues?critical=true&page=2&per_page=100&sort_by=last_seen_at.desc&state=active%2Cinactive%2Cmissing%2Cretired&status=active%2Cresolved'}}  # NOQA
        result = cloudpassage.HttpHelper.get_next_page_path(body)
        assert result == "/v3/issues?critical=true&page=2&per_page=100&sort_by=last_seen_at.desc&state=active%2Cinactive%2Cmissing%2Cretired&status=active%2Cresolved"  # NOQA


class TestIntegrationPost:
    def test_post_404(self):
        endpoint = nonexistent_url
        post_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.post(endpoint, post_data)
        assert '404' in str(e)

    def test_post_bad_payload(self):
        endpoint = "/v1/groups"
        post_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageValidation) as e:
            req.post(endpoint, post_data)
        assert '400' in str(e)

    def test_post_rekey(self):
        endpoint = nonexistent_url
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.post(endpoint, {"nonexist": "nothing"})
        assert '404' in str(e)


class TestIntegrationPut:
    def test_put_bad_endpoint(self):
        endpoint = nonexistent_url
        put_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.put(endpoint, put_data)
        assert '404' in str(e)

    def test_post_bad_payload(self):
        endpoint = "/v1/groups"
        put_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.put(endpoint, put_data)
        assert '404' in str(e)

    def test_put_rekey(self):
        body = {"server":
                {"retire": True}}
        endpoint = "/v1/servers/1234567890"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.put(endpoint, body)
        assert '404' in str(e)


class TestIntegrationDelete:
    def test_delete_404(self):
        endpoint = nonexistent_url
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.delete(endpoint)
        assert '404' in str(e)

    def test_delete_rekey(self):
        endpoint = "/v1/servers/123455432"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            req.delete(endpoint)
        assert '404' in str(e)
