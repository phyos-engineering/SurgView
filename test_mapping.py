"""
Unit tests for the mapping class
"""

import mapping


class TestMapping:

    def test_add_and_remove_coordinate(self):
        mapper = mapping.ScreenMap()
        print("Adding Coordinate:")
        mapper.add_widget("test", 1, 2)
        assert mapper.gui_map == {'test': {'x': 1, 'y': 2}}
        assert mapper.get_map != {'test': {'x': 1, 'y': 2}}
        # get map returns the address of a map object, which may not be what you want
        mapper.add_widget("best", 1, 2)
        assert mapper.gui_map == {'best': {'x': 1, 'y': 2}, 'test': {'x': 1, 'y': 2}}
        assert mapper.locate_label("test") == ('test', {'x': 1, 'y': 2})
        assert mapper.locate_label("best") == ('best', {'x': 1, 'y': 2})
        assert mapper.locate_label("test") != ('best', {'x': 1, 'y': 2})
        mapper.remove_widget("best")
        assert mapper.gui_map == {'test': {'x': 1, 'y': 2}}
        assert mapper.locate_label("best") is None
        mapper.remove_widget("test")
        assert mapper.gui_map == {}

    def test_key_exists(self):
        mapper = mapping.ScreenMap()
        print("Checking if Key -> test exists:")
        assert mapper.if_widget_exists("test") is False
        print("Adding Coordinate:")
        mapper.add_widget("best", 1, 2)
        print("Checking if Key -> test exists:")
        assert mapper.if_widget_exists("test") is False
        print("Adding Coordinate:")
        mapper.add_widget("test", 1, 2)
        print("Checking if Key -> test exists:")
        assert mapper.if_widget_exists("test") is True

    def test_update_coordinate(self):
        mapper = mapping.ScreenMap()
        print("Adding Coordinate:")
        mapper.add_widget("test", 1, 2)
        print("Updating Values of Key-> test:")
        mapper.update_coordinate("test", -3, -4)
        assert mapper.gui_map == {'test': {'x': -3, 'y': -4}}
