"""
Unit tests for the mapping class
"""

import mapping
import unittest

class TestMapping(unittest.TestCase):

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


        assert mapper.locate_label("best") == None
        with self.assertRaises(TypeError):
            mapper.remove_widget(1)
        with self.assertRaises(TypeError):
            mapper.remove_widget(1.0)

        mapper.remove_widget("test")
        with self.assertRaises(TypeError):
            mapper.get_keys_coordinates(1)
        with self.assertRaises(TypeError):
            mapper.get_keys_coordinates(1.0)
        assert mapper.gui_map == {}

    def test_add_invalid_coordinate(self):
        mapper = mapping.ScreenMap()
        print("Adding Coordinate:")
        with self.assertRaises(TypeError):
            mapper.add_widget(1, 1, 2)
        with self.assertRaises(TypeError):
            mapper.add_widget(1.0, 1, 2)
        with self.assertRaises(TypeError):
            mapper.add_widget([1], 1, 2)
        with self.assertRaises(TypeError):
            mapper.add_widget(["test","best"], 1, 2)
        with self.assertRaises(TypeError):
            mapper.add_widget("test", "test", "test")
        with self.assertRaises(TypeError):
            mapper.add_widget("test", 1.0, 2)
        with self.assertRaises(TypeError):
            mapper.add_widget("test", [1, 2], [])
        assert mapper.gui_map == {}
        with self.assertRaises(TypeError):
            mapper.locate_label(1)


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

        assert mapper.if_widget_exists("test") == True
        with self.assertRaises(TypeError):
            mapper.if_widget_exists(1)
        with self.assertRaises(TypeError):
            mapper.if_widget_exists(1.0)


    def test_update_coordinate(self):
        mapper = mapping.ScreenMap()
        print("Adding Coordinate:")
        mapper.add_widget("test", 1, 2)
        print("Updating Values of Key-> test:")
        mapper.update_coordinate("test", -3, -4)
        assert mapper.gui_map == {'test': {'x': -3, 'y': -4}}

        with self.assertRaises(TypeError):
            mapper.update_coordinate("test", "test", "test")
        with self.assertRaises(TypeError):
            mapper.update_coordinate("test", 1.0, 2)

