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
    if not (re.match("\d+", user_defined_longitude)
            or re.match("\d+.\d*", user_defined_longitude)):
        user_defined_longitude = None
    user_defined_latitude = input("Долгота : ")
    if not (re.match("\d+", user_defined_latitude)
            or re.match("\d+.\d*", user_defined_latitude)):
        user_defined_latitude = None
    return user_defined_longitude, user_defined_latitude


def get_pretty_output(output_template_form, bar, distance=None):
    generic_output_template = (
        "бар: {}"
        "\nКоторый расположен по адресу: {}"
    )
    bar_name = bar["properties"]["Attributes"]["Name"]
    bar_address = bar["properties"]["Attributes"]["Address"]
    if output_template_form == "biggest":
        output_template = " ".join(
            [
                "Самый большой",
                generic_output_template
            ]
        )
        output_text = output_template.format(bar_name, bar_address)
    if output_template_form == "smallest":
        output_template = " ".join(
            [
                "Самый маленький",
                generic_output_template
            ]
        )
        output_text = output_template.format(bar_name, bar_address)
    if output_template_form == "closest":
        output_template = " ".join(
            [
                "Ближайший",
                generic_output_template,
                "\nНаходится на расстоянии: {} километров"
            ]
        )
        output_text = output_template.format(
            bar_name,
            bar_address,
            str(int(distance/1000))
        )
    print(output_text)


if __name__ == "__main__":
    json_filepath = sys.argv[1]
    if not os.path.exists(json_filepath):
        print("Такой файл не существует")
    else:
        bars_list = load_data(json_filepath)
        user_defined_longitude, user_defined_latitude = (
            request_user_defined_coordinates()
        )
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
        get_pretty_output("biggest", biggest_bar)
        get_pretty_output("smallest", smallest_bar)
        get_pretty_output("closest", closest_bar, distance)
