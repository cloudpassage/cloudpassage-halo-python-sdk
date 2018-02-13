import imp
import os
import sys


module_name = 'cloudpassage'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage = imp.load_module(module_name, fp, pathname, description)


class TestUnitTimeSeries(object):
    def test_unit_time_series_build_url_list(self):
        path = "/v1/whatever"
        params = {"server": "heyhowdy"}
        count = 0
        for item in cloudpassage.TimeSeries.create_url_batch(path, 5, params):
            count += 1
            assert item[0] == path
            assert item[1]["server"] == "heyhowdy"
            assert item[1]["page"] == count
        assert count == 5

    def test_unit_time_series_sorted_items_from_pages(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"},
                    {"item_number": 4,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": [
                    {"item_number": 2,
                     "nonsort": "somesuch"},
                    {"item_number": 3,
                     "nonsort": "somesuch"}]}
        pages = [page1, page2]
        s = cloudpassage.TimeSeries.sorted_items_from_pages(pages, "whatevers",
                                                            "item_number")
        count = 0
        for item in s:
            count += 1
            assert item["item_number"] == count
        assert count == 4

    def test_unit_time_series_get_number_of_empty_pages(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"},
                    {"item_number": 4,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": []}
        pages = [page1, page2]
        pkey = "whatevers"
        expected = 1
        actual = cloudpassage.TimeSeries.get_number_of_empty_pages(pages, pkey)
        assert expected == actual

    def test_unit_time_series_get_number_of_full_pages(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"},
                    {"item_number": 4,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": []}
        pages = [page1, page2]
        pkey = "whatevers"
        expected = 1
        actual = cloudpassage.TimeSeries.get_number_of_full_pages(pages,
                                                                  2, pkey)
        assert expected == actual

    def test_unit_time_series_get_adjustment_factor_zero(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"},
                    {"item_number": 4,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": [
                    {"item_number": 2,
                     "nonsort": "somesuch"}]}
        pages = [page1, page2]
        pkey = "whatevers"
        expected = 0
        actual = cloudpassage.TimeSeries.get_adjustment_factor(pages, 2, pkey)
        assert expected == actual

    def test_unit_time_series_get_adjustment_factor_up_one(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"},
                    {"item_number": 4,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": [
                    {"item_number": 2,
                     "nonsort": "somesuch"},
                    {"item_number": 3,
                     "nonsort": "somesuch"}]}
        pages = [page1, page2]
        pkey = "whatevers"
        expected = 1
        actual = cloudpassage.TimeSeries.get_adjustment_factor(pages, 2, pkey)
        assert expected == actual

    def test_unit_time_series_get_adjustment_factor_down_one(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"},
                    {"item_number": 4,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": [
                    {"item_number": 2,
                     "nonsort": "somesuch"},
                    {"item_number": 3,
                     "nonsort": "somesuch"}]}
        page3 = {"whatevers": []}
        pages = [page1, page2, page3]
        pkey = "whatevers"
        expected = -1
        actual = cloudpassage.TimeSeries.get_adjustment_factor(pages, 2, pkey)
        assert expected == actual

    def test_unit_time_series_get_adjustment_factor_big_drop(self):
        page1 = {"whatevers": [
                    {"item_number": 1,
                     "nonsort": "somesuch"}]}
        page2 = {"whatevers": []}
        page3 = {"whatevers": []}
        pages = [page1, page2, page3]
        pkey = "whatevers"
        expected = -9
        actual = cloudpassage.TimeSeries.get_adjustment_factor(pages, 2, pkey)
        assert expected == actual
