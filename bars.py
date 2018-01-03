#!/usr/bin/env python3


import json
import re
import sys
import os
from geopy.distance import vincenty


def load_data(json_filepath):
    with open(json_filepath, "r") as file_contaning_json:
        object_representing_json = json.load(file_contaning_json)
    bars_list = object_representing_json["features"]
    return bars_list


def get_biggest_bar(bars_list):
    biggest_bar = max(
        bars_list,
        key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"]
    )
    return biggest_bar


def get_smallest_bar(bars_list):
    smallest_bar = min(
        bars_list,
        key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"]
    )
    return smallest_bar


def calculate_geo_distance(
        bar,
        user_defined_longitude,
        user_defined_latitude):
    distance = vincenty(
        (float(user_defined_longitude), float(user_defined_latitude)),
        bar["geometry"]["coordinates"]).meters
    return distance


def get_closest_bar(
        bars_list,
        user_defined_longitude,
        user_defined_latitude):
    closest_bar = min(
        bars_list,
        key=lambda bar: calculate_geo_distance(
            bar,
            user_defined_longitude,
            user_defined_latitude
        )
    )
    distance = calculate_geo_distance(
        closest_bar,
        user_defined_longitude,
        user_defined_latitude
    )
    return closest_bar, distance


def request_user_defined_coordinates():
    print("Введите GPS координаты подыщем ближайший бар "
          "(в формате int или float)")
    user_defined_longitude = input("Широта : ")
    if not re.match("\d+(\.\d+)?$", user_defined_longitude):
        user_defined_longitude = None
    user_defined_latitude = input("Долгота : ")
    if not re.match("\d+(\.\d+)?$", user_defined_latitude):
        user_defined_latitude = None
    return user_defined_longitude, user_defined_latitude


def print_pretty_output(bar_type, bar, distance=None):
    output_template_main = (
        "Самый {} бар: {}"
        "\nКоторый расположен по адресу: {}"
    )
    output_template_suffix = "\nНаходится на расстоянии: {} километров"
    bar_name = bar["properties"]["Attributes"]["Name"]
    bar_address = bar["properties"]["Attributes"]["Address"]
    output_main = output_template_main.format(
        bar_type,
        bar_name,
        bar_address
    )
    print(output_main)
    if distance:
        output_suffix = output_template_suffix.format(int(distance/1000))
        print(output_suffix)


if __name__ == "__main__":
    json_filepath = sys.argv[1]
    if not os.path.exists(json_filepath):
        print("Такой файл не существует")
    else:
        bars_list = load_data(json_filepath)
        user_defined_longitude, user_defined_latitude = (
            request_user_defined_coordinates()
        )
        print(user_defined_longitude, user_defined_latitude)
        if user_defined_longitude is None or user_defined_latitude is None:
            sys.exit("Некорректный формат значений GPS координат."
                     "\nПерезапустите программу и "
                     "введите аргументы в корректном формате")
        biggest_bar = get_biggest_bar(bars_list)
        smallest_bar = get_smallest_bar(bars_list)
        closest_bar, distance = get_closest_bar(
            bars_list,
            user_defined_longitude,
            user_defined_latitude
        )
        print_pretty_output("большой", biggest_bar)
        print_pretty_output("маленький", smallest_bar)
        print_pretty_output("ближайший", closest_bar, distance)
