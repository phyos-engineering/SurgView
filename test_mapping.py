"""
Unit tests for the mapping class
"""

import mapping


class TestMapping:

    def test_add_coordinate(self):
        mapper = mapping.ScreenMap()
        print("Adding Coordinate:")
        mapper.add_widget("test", 1, 2)
        assert mapper.gui_map == {'test': {'x': 1, 'y': 2}}

    def test_key_exists(self):
        mapper = mapping.ScreenMap()
        print("Adding Coordinate:")
        mapper.add_widget("test", 1, 2)
        print("Checking if Key -> test exists:")
        assert mapper.if_widget_exists("test") == True

    def test_key_nonexists(self):
        mapper = mapping.ScreenMap()
        print("Checking if Key -> test exists:")
        assert mapper.if_widget_exists("test") == False

    def test_update_coordinate(self):
        mapper = mapping.ScreenMap()
        print("Adding Coordinate:")
        mapper.add_widget("test", 1, 2)
        print("Updating Values of Key-> test:")
        mapper.update_coordinate("test", 3, 4)
        assert mapper.gui_map == {'test': {'x': 3, 'y': 4}}
