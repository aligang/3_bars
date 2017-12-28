#!/usr/bin/env python3.5
# -*- coding: utf-8 -*

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
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )
    return biggest_bar


def get_smallest_bar(object_representing_json):
    bars_list = object_representing_json["features"]
    smallest_bar = min(
        bars_list,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )
    return smallest_bar


def get_closest_bar(object_representing_json,
                    user_defined_longitude, user_defined_latitude):
    bars_list = object_representing_json["features"]
    closest_bar = min(
        bars_list,
        key=lambda bar: vincenty(
            (float(user_defined_longitude), float(user_defined_latitude)),
            tuple(bar["geometry"]["coordinates"])
        ).meters
    )
    distance = vincenty(
            (float(user_defined_longitude), float(user_defined_latitude)),
            tuple(closest_bar["geometry"]["coordinates"])
    ).meters
    return closest_bar, distance


if __name__ == '__main__':
    json_filepath = sys.argv[1]
    if not os.path.exists(json_filepath):
        print("Такой файл не существует")
    else:
        object_representing_json = load_data("bars.json")
        biggest_bar = get_biggest_bar(object_representing_json)
        smallest_bar = get_smallest_bar(object_representing_json)
        print("Самый большой бар: " +
              biggest_bar['properties']['Attributes']['Name'])
        print("Который расположен по адресу: " +
              biggest_bar['properties']['Attributes']['Address'])
        print("Самый маленький бар: " +
              smallest_bar['properties']['Attributes']['Name'])
        print("Который расположен по адресу: " +
              smallest_bar['properties']['Attributes']['Address'])
        user_defined_coordinates = input(
            "Введите GPS координаты, подыщем ближайший бар: "
        )
        if "," in user_defined_coordinates:
            user_defined_longitude, user_defined_latitude = re.split(
                "\s*,+\s*",
                user_defined_coordinates
            )
        else:
            user_defined_longitude, user_defined_latitude = re.split(
                "\s+",
                user_defined_coordinates
            )
        closest_bar, distance = get_closest_bar(
            object_representing_json,
            user_defined_longitude,
            user_defined_latitude
        )
        print("Ближайший бар : " +
              closest_bar['properties']['Attributes']['Name'])
        print("Который расположен по адресу: " +
              closest_bar['properties']['Attributes']['Address'])
        print("Находится на расстоянии " +
              str(int(distance/1000)) + " километров")
