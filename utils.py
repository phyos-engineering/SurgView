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


def transform_to_int(string: str) -> str:
    words = string.split()
    new_string = []
    num_dict = {"one": "1", "two": "2"}
    for word in words:
        if word in num_dict:
            word = num_dict[word]
            new_string.append(word)
        else:
            new_string.append(word)

    return " ".join(new_string)


def clean_string(string: str) -> str:
    """
    Remove spaces and non-alpha numeric characters from string and makes all characters lowercase
    :param string: Dirty string
    :return: cleaned string
    """
    return "".join(c for c in string if c.isalnum()).lower()


def get_serial_number():
    cpu_serial = "0000000000000000"
    try:
        f = open("/proc/cpuinfo", "r")
        for line in f:
            if line[0:6] == "Serial":
                cpu_serial = line[10:26]
    except:
        cpu_serial = "ERROR000000000"

    return cpu_serial


def get_board_model():
    board_model = ""
    try:
        f = open("/proc/device-tree/model", "r")
        for line in f:
            board_model = line[::]
    except:
        board_model = "ERROR"
    return board_model


def main():
    new = transform_to_int("one dog two cats")
    print(new)


if __name__ == "__main__":
    main()
