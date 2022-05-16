from typing import Type
import numpy as np
import math
import re


def ask_if_to_trim_points():
    ans = input("Do you want to trim distant points? \n[y/n]: ")
    return ans

def ask_about_ratio_to_trim_points():
    while True:
        ans = input("How much distant points do you want to remove? \n[Legend: 0.2-close, 1-very distant, default=0.3]: ")
        if ans =="":
            return ans
        if re.match(r'^-?\d+(?:\.\d+)$', ans) is None:
            while True:
                next = input(f"Invalid input, do you want to re-enter the value? If no value will be set to default\nYes - y\nNo -n\n")
                if next == 'n' or next == 'y':
                    break
            if next == 'n':
                return ""
        else:
            break
    return ans


def set_default_ratio():
    ratio = 0.3
    return ratio


def check_if_ratio_is_correct(ratio):
    if ratio > 0.2 and ratio <= 1:
        return ratio
    ratio = set_default_ratio()
    return ratio


def get_entered_ratio(ratio):
    try:
        ratio = float(ratio)
        check_if_ratio_is_correct(ratio)
    except:
        ratio = set_default_ratio()
    return ratio


def set_ratio():
    ans = ask_if_to_trim_points()
    if ans in ['Y', 'y']:
        ratio_ans = ask_about_ratio_to_trim_points()
        ratio = get_entered_ratio(ratio_ans)
    else:
        ratio = set_default_ratio()
    return ratio


def calculate_dist_between_two_points(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def get_max_distance(points, other):
    max_dist = max(calculate_dist_between_two_points(coord[0], coord[1], other[0], other[1]) for coord in points)
    return max_dist


def trim_distant_points(points, other, ratio):
    points_to_del = []
    max_dist = get_max_distance(points, other)
    # print(f"Max distance: {max_dist}")
    for i, coord in enumerate(points):
        if(calculate_dist_between_two_points(coord[0], coord[1], other[0], other[1]) > ratio * max_dist):
            points_to_del.append(i)
    points = np.delete(points, points_to_del, 0)
    return points


def trim_points(points_bef, ratio):
    other = [0, 0]
    points_after = trim_distant_points(points=points_bef, other=other, ratio=ratio)
    return points_after

