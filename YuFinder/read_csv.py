from collections import OrderedDict
import datetime
import time

import numpy as np
import pandas as pd

from Yusi.YuFinder.point import Coordinates, OperatingHours, Point


lat_long_delimeter = ','


def __IsNone(input_):
  if not input_:
    return True
  if isinstance(input_, str):  # and input_
    return False
  if np.isnan(input_):
    return True
  return False


def ExtractString(input_str):
  if __IsNone(input_str):
    return None
  return input_str.strip()


def ExtractFloat(input_str):
  input_str = ExtractString(input_str)
  if __IsNone(input_str):
    return None
  return float(input_str)


def __CoordinateStrToFloat(input_str, pos_suffix, neg_suffix):
  sign = 1
  if input_str.endswith(pos_suffix):
    input_str = input_str[:-len(pos_suffix)]
  elif input_str.endswith(neg_suffix):
    sign = -1
    input_str = input_str[:-len(neg_suffix)]
  return sign * float(input_str)
  

def ExtractCoordinates(coordinates_str):
  coordinates_str = ExtractString(coordinates_str)
  if __IsNone(coordinates_str):
    return None
  latitude_str, longitude_str = coordinates_str.split(lat_long_delimeter)
  latitude_str = ExtractString(latitude_str)
  longitude_str = ExtractString(longitude_str)
  if __IsNone(latitude_str) or __IsNone(longitude_str):
    return None
  latitude = __CoordinateStrToFloat(latitude_str, 'N', 'S')
  longitude = __CoordinateStrToFloat(longitude_str, 'E', 'W')
  return Coordinates(latitude, longitude)
  

def __HoursStrToTime(input_str):
  input_time_struct = time.strptime(input_str, '%H:%M:%S')
  return datetime.time(input_time_struct.tm_hour, input_time_struct.tm_min, input_time_struct.tm_sec)


def ExtractOperatingHours(opens_str, closes_str):
  opens_str = ExtractString(opens_str)
  closes_str = ExtractString(closes_str)
  if __IsNone(opens_str) or __IsNone(closes_str):
    return None
  opens = __HoursStrToTime(opens_str)
  closes = __HoursStrToTime(closes_str)
  return OperatingHours(opens, closes)


def ReadCSV(csv_filepath):
  points_df = pd.DataFrame.from_csv(csv_filepath)
  points = []
  for index, point_series in points_df.iterrows():
    points.append(Point(
      ExtractString(point_series['Name']),
      ExtractCoordinates(point_series['CoordinatesStarts']),
      ExtractCoordinates(point_series['CoordinatesEnds']),
      ExtractOperatingHours(point_series['OperatingHoursOpens'], point_series['OperatingHoursCloses']),
      float(point_series['Duration'])))
  return points


def ReadCSVToDict(csv_filepath):
  points = ReadCSV(csv_filepath)
  points_dict = OrderedDict()
  for point in points:
    points_dict[point.name] = point
  return points_dict
