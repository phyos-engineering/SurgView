# !/usr/bin/env python
# title           :SurgView.py
# description     :Enter Description Here
# author          :Sebastian Maldonado
# date            :5/13/21
# version         :0.0
# usage           :SEE README.md
# notes           :Enter Notes Here
# python_version  :3.6.8
# conda_version   :4.8.3
# =================================================================================================================

from events import EventHandler

"""
Driver Program
"""


def main():
    event_manager = EventHandler()
    event_manager.listen()


if __name__ == "__main__":
    main()


