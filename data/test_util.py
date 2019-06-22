import os

from data import database_connection
from data import read_csv


def GetPointsInput(csv_dirpath, csv_filename):
  points_dict = read_csv.ReadCSVToDict(os.path.join(csv_dirpath, csv_filename))
  return points_dict


def GetPointsKeys(keys_dirpath, keys_filename):
  test_points_filepath = os.path.join(keys_dirpath, keys_filename)
  lines = open(test_points_filepath).readlines()
  lines = [line.strip() for line in lines]
  keys = [line for line in lines if line and not line.startswith('#')]
  return keys


def FilterAndSortByKeys(points_dict, keys):
  return [points_dict[key] for key in keys]
