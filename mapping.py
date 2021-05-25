# !/usr/bin/env python
# title           :mapping.py
# description     :Enter Description Here
# author          :Juan Maldonado
# date            :5/13/2021
# version         :0.0
# usage           :SEE README.md
# python_version  :3.7.10
# conda_version   :4.9.2
# ========================================================================================================

"""
Screen Mapping Class is in charge of keeping track of the location of widgets observed by UIReader.
"""


class ScreenMap:
    def __init__(self):
        self.gui_map = dict()

    def if_widget_exists(self, key: str):
        """
        Check to see if widget exists in map
        :param key: widget name
        :return: Boolean. True -> Widget Found, False -> Not Found
        """
        if key in self.gui_map:
            return True
        else:
            return False

    def locate_label(self, entity_name: str):
        """
        Locate an LUIS.ai entity within map
        :param entity_name: Name of entity
        :return: Key value pair (tuple)
        """
        for key in self.gui_map.keys():
            if entity_name in key:
                return key, self.get_keys_coordinates(key)

    def add_widget(self, key: str, x: int, y: int):
        """
        Add widget to map
        :param key: Key name of key value pair
        :param x: X coordinate of widget
        :param y: Y coordinate of widget
        """
        self.gui_map[key] = {"x": x, "y": y}

    def update_coordinate(self, key: str, new_x: int, new_y: int):
        """
        Update coordinates of a widget found map
        :param key: Key name of widget
        :param new_x: New X coordinate
        :param new_y: New Y coordinate
        """
        if self.if_widget_exists(key):
            self.gui_map[key]["x"] = new_x
            self.gui_map[key]["y"] = new_y

    def remove_widget(self, key):
        """
        Remove widget from map
        :param key: Key name of widget
        """
        if self.if_widget_exists(key):
            del self.gui_map[key]

    def get_keys_coordinates(self, key: str):
        """
        Return values of key
        :param key: key name
        :return: Key's values
        """
        return self.gui_map[key]

    def get_map(self):
        """
        Return full content of map
        """
        for key in self.gui_map:
            print(key, "->", self.gui_map[key])


def main():
    mapper = ScreenMap()
    print("Adding Coordinate:")
    mapper.add_widget("test", 1, 2)
    print(mapper.gui_map)
    print("Checking if Key -> test exists:")
    print(mapper.if_widget_exists("test"))
    print("Updating Values of Key-> test:")
    mapper.update_coordinate("test", 3, 4)
    print(mapper.gui_map)
    print("Deleting Key-> test:")
    mapper.remove_widget("test")
    print(mapper.gui_map)


if __name__ == "__main__":
    main()
