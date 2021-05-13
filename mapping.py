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

    def if_widget_exist(self, key: str):
        if key in self.gui_map:
            return True
        else:
            return False

    def add_coordinate(self, key: str, x: int, y: int):
        self.gui_map[key] = {"x": x, "y": y}

    def update_coordinate(self, key: str, x: int, y: int):
        self.gui_map[key]["x"] = x
        self.gui_map[key]["y"] = y

    def remove_coordinate(self, key):
        if self.if_widget_exist(key):
            del self.gui_map[key]


def main():
    mapper = ScreenMapping()
    print("Adding Coordinate:")
    mapper.add_coordinate("test", 1, 2)
    print(mapper.gui_map)
    print("Checking if Key -> test exists:")
    print(mapper.if_widget_exist("test"))
    print("Updating Values of Key-> test:")
    mapper.update_coordinate("test", 3, 4)
    print(mapper.gui_map)
    print("Deleting Key-> test:")
    mapper.remove_coordinate("test")
    print(mapper.gui_map)


if __name__ == "__main__":
    main()
