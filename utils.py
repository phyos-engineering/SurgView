# !/usr/bin/env python
# title           :utils.py
# description     :Enter Description Here
# author          :Juan Maldonado
# date            :5/25/2021
# version         :0.0
# usage           :SEE README.md
# python_version  :3.7.10
# conda_version   :4.9.2
# ========================================================================================================


def clean_string(string: str) -> str:
    """
    Remove spaces and non-alpha numeric characters from string and makes all characters lowercase
    :param string: Dirty string
    :return: cleaned string
    """
    return ''.join(c for c in string if c.isalnum()).lower()
