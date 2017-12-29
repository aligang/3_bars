#!/usr/bin/env python3


import json
import math
import re
import sys
import os
from geopy.distance import vincenty


def load_data(json_filepath):
    with open(json_filepath, "r") as file_contaning_json:
        object_representing_json = json.load(file_contaning_json)
    return object_representing_json


def get_biggest_bar(object_representing_json):
    bars_list = object_representing_json["features"]
    biggest_bar = max(
        bars_list,
        key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"]
    )
    return biggest_bar


def get_smallest_bar(object_representing_json):
    bars_list = object_representing_json["features"]
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
        object_representing_json,
        user_defined_longitude,
        user_defined_latitude):
    bars_list = object_representing_json["features"]
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
    user_defined_coordinates = input(
        "Введите GPS координаты (например, 77.77, 88.88), "
        "подыщем ближайший бар: "
    )
    while len(user_defined_coordinates.split(",")) != 2:
        user_defined_coordinates = input(
            "Неверно указан формат координат, укажите в формате "
            "'77.77, 88.88' : "
        )
    user_defined_longitude, \
        user_defined_latitude = user_defined_coordinates.split(",")
    return user_defined_longitude, user_defined_latitude


def get_pretty_output(biggest_bar=None, smallest_bar=None,
    closest_bar=None, distance=None):
    if biggest_bar:
        print("Самый большой бар: {}".format(
                biggest_bar["properties"]["Attributes"]["Name"]
            )
        )
        print("Который расположен по адресу: {}".format(
                biggest_bar["properties"]["Attributes"]["Address"]
            )
        )
    if smallest_bar:
        print("Самый маленький бар: {}".format(
                smallest_bar["properties"]["Attributes"]["Name"]
            )
        )
        print("Который расположен по адресу: {}".format(
                smallest_bar["properties"]["Attributes"]["Address"]
            )
        )
    if closest_bar and distance:
        print("Ближайший бар : {}".format(
                closest_bar["properties"]["Attributes"]["Name"]
            )
        )
        print("Который расположен по адресу: {}".format(
                closest_bar["properties"]["Attributes"]["Address"]
            )
        )
        print("Находится на расстоянии: {} километров".format(
                str(int(distance/1000))
            )
        )


if __name__ == "__main__":
    json_filepath = sys.argv[1]
    if not os.path.exists(json_filepath):
        print("Такой файл не существует")
    else:
        object_representing_json = load_data(json_filepath)
        user_defined_longitude,\
            user_defined_latitude = request_user_defined_coordinates()
        biggest_bar = get_biggest_bar(object_representing_json)
        smallest_bar = get_smallest_bar(object_representing_json)
        closest_bar, distance = get_closest_bar(
            object_representing_json,
            user_defined_longitude,
            user_defined_latitude
        )
        get_pretty_output(biggest_bar=biggest_bar)
        get_pretty_output(smallest_bar=smallest_bar)
        get_pretty_output(closest_bar=closest_bar, distance=distance)
