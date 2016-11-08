import os

import Yusi
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuPoint.database_connection import DatabaseConnectionInterface


def GetPointsInput(csv_dirpath, csv_filename):
  points_dict = ReadCSVToDict(
      os.path.join(Yusi.GetYusiDir(), csv_dirpath, csv_filename))
  return points_dict


def GetPointsKeys(keys_dirpath, keys_filename):
  test_points_filepath = os.path.join(
      Yusi.GetYusiDir(), keys_dirpath, keys_filename)
  lines = open(test_points_filepath).readlines()
  lines = [line.strip() for line in lines]
  keys = [line for line in lines if line and not line.startswith('#')]
  return keys


def FilterAndSortByKeys(points_dict, keys):
  return [points_dict[key] for key in keys]


class MockDatabaseConnection(DatabaseConnectionInterface):

  def __init__(self):
    self.points_dict_dict = {
        'New York City': GetPointsInput('YuPoint', 'test_nyc_1.csv'),
        'San Francisco': GetPointsInput('YuPoint', 'test_sf_1.csv')}

  def GetPoints(self, visit_location):
    return self.points_dict_dict[visit_location.city_name].values()

  def GetPoint(self, visit_location, point_name):
    return self.points_dict_dict[visit_location.city_name][point_name]
