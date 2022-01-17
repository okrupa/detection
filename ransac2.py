import random
import numpy as np
from sympy import Point
import pyransac3d as pyrsc

def if_collinear(points):
    '''
    Czy punkty definiują płaszczyznę
    '''
    p1, p2, p3 = Point(points[0]), Point(points[1]), Point(points[2])
    return Point.is_collinear(p1, p2, p3)

def choose_points(points):
    '''
    Wybierz w sposób losowy trzy punkty spośród punktów zawartych w chmurze.
    Jeśli wybrane punkty nie definiują w sposób jednoznaczny płaszczyzny (tzn.
    są współliniowe), wybierz inne trzy punkty. 
    '''
    collinear = True
    while collinear:
        chosen_points = random.choices(points, k=3)
        for i in range(len(chosen_points)):
            chosen_points[i] = np.array(chosen_points[i])
        collinear = if_collinear(chosen_points)
    chosen_points = np.array(chosen_points)
    return chosen_points

def ransac_algorithim(points):
    plane = pyrsc.Plane()
    min_points_amount = len(points) * 0.3
    while min_points_amount < len(points):
        chosen_points = choose_points(points)
        '''
        Oblicz równanie płaszczyzny pasującej do wybranych punktów, tzn. wyznacz
        współczynniki a, b, c, d występujące w równaniu ax + by + cd + d = 0. 
        '''
        plane_abcd, inliers = plane.fit(chosen_points, thresh = 0.01, maxIteration = 100)
        if plane_abcd:
            a, b, c, d = plane_abcd
            points_to_del = []
            for i, coord in enumerate(points):
                '''
                Policz liczbę punktów pasujących do znalezionego modelu. Punkt jest uznawany
                za pasujący (ang. inlier), jeśli jego odległość od płaszczyzny nie przekracza
                określonej wcześniej wartości tolerancji δ. 
                '''
                dist = np.abs(a*coord[0]+b*coord[1]+c*coord[2]+d) / np.sqrt(a**2+b**2+c**2)
                if dist < 0.01:
                    points_to_del.append(i)
        points = np.delete(points, points_to_del, 0)
    return points


def delete_algorithim(points):

    points_to_del = []
    for i, coord in enumerate(points):
        if coord[1] > 0:
             points_to_del.append(i)
        if coord[0] > 0:
             points_to_del.append(i)
    points = np.delete(points, points_to_del, 0)
    return points
