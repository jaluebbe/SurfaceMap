import json
import os
import logging
import time
from shapely import speedups
if speedups.available:
    speedups.enable()
from shapely.geometry import shape, Point

path = os.path.dirname(os.path.abspath(__file__))
file_name = 'countries_ne_10m.json'

def add_bounding_boxes():
    with open(os.path.join(path, file_name)) as f:
        countries = json.load(f)
    for feature in countries['features']:
        polygon = shape(feature['geometry'])
        feature['bbox'] = list(polygon.bounds)
    with open(os.path.join(path, file_name), 'w') as f:
        json.dump(countries, f)

#add_bounding_boxes()

with open(os.path.join(path, file_name)) as f:
    countries = json.load(f)

def get_country_for_position(latitude, longitude):
    point = Point(longitude, latitude)
    for feature in countries['features']:
        minx, miny, maxx, maxy = feature['bbox']
        if not (maxy >= latitude >= miny and
                maxx >= longitude >= minx):
            continue
        polygon = shape(feature['geometry'])
        if feature['geometry']['type'] == 'MultiPolygon':
            # If the country consists of multiple polygons we need to iterate over
            # each single polygon.
            multipolygon = polygon
            for polygon in multipolygon:
                if polygon.contains(point):
                    return feature['properties']
        elif polygon.contains(point):
            return feature['properties']
    logging.debug('No country found at ({}, {}).'.format(latitude, longitude))
    return {}
