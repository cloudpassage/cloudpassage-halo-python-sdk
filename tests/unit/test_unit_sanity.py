import cloudpassage

sanity = cloudpassage.sanity


class TestUnitSanity:
    def test_valid_object_id(self):
        sample_object_id = "951ffd865e4f11e59ba055477bd3e868"
        assert sanity.validate_object_id(sample_object_id)

    def test_valid_object_id_list(self):
        sample_object_id = ["951ffd865e4f11e59ba055477bd3e868",
                            "951ffd865e4f11e59ba055477bd3e999"]
        assert sanity.validate_object_id(sample_object_id)

    def test_invalid_object_id_list(self):
        rejected = False
        sample_object_id = ["951ffd865e4f11e59ba055477bd3e868",
                            "../../servers/951ffd865e4f11e59ba055477bd3e999"]
        try:
            sanity.validate_object_id(sample_object_id)
        except:
            rejected = True
        assert rejected

    def test_invalid_object_id(self):
        rejected = False
        sample_object_id = "../../servers/951ffd865e4f11e59ba055477bd3e868"
        try:
            sanity.validate_object_id(sample_object_id)
        except:
            rejected = True
        assert rejected

    def test_invalid_object_type(self):
        rejected = False
        sample_object_id = ("Tuple", "of", ["Things", "AndStuff"])
        try:
            sanity.validate_object_id(sample_object_id)
        except:
            rejected = True
        assert rejected

    def test_validate_hostname_mtg(self):
        sane = sanity.validate_api_hostname("api.cloudpassage.com")
        assert sane

    def test_validate_hostname_nonexist_vpg(self):
        sane = sanity.validate_api_hostname("api.vpg-noexist.cloudpassage.com")
        assert sane

    def test_validate_hostname_not_cp(self):
        sane = sanity.validate_api_hostname("api.example.com")
        assert sane is False

    def test_validate_borky(self):
        sane = sanity.validate_api_hostname("api.cloudpassage.com/v1/s")
        assert sane is False
