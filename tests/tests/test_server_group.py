import cloudpassage
import json
import os
import pytest

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
ro_key_id = os.environ.get('RO_HALO_KEY_ID')
ro_secret_key = os.environ.get('RO_HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestServerGroup:
    def create_server_group_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return(cloudpassage.ServerGroup(session))

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.ServerGroup(session)

    def test_list_all(self):
        s_grp = self.create_server_group_object()
        groups = s_grp.list_all()
        assert "id" in groups[0]

    def test_describe(self):
        s_grp = self.create_server_group_object()
        groups = s_grp.list_all()
        target_group_id = groups[0]["id"]
        target_group_object = s_grp.describe(target_group_id)
        assert "id" in target_group_object

    def test_list_members(self):
        # Rolls through all server groups, confirms active server IDs
        confirmed = False
        s_grp = self.create_server_group_object()
        groups = s_grp.list_all()
        num_members = 0
        for g in groups:
            target_group_id = g["id"]
            num_members = g["server_counts"]["active"]
            if num_members > 0:
                members = s_grp.list_members(target_group_id)
                assert members[0]["id"]
                confirmed = True
        # Confirm that we actually have a populated server group
        assert confirmed

    def test_create_delete_server_group(self):
        s_grp = self.create_server_group_object()
        new_grp_id = s_grp.create("TEN_FOUR_GOOD_BUDDY")
        delete_return = s_grp.delete(new_grp_id)
        assert delete_return is None
