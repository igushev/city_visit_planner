import datetime
import os

import Yusi
from Yusi.YuPoint.city_visit import CityVisitParameters
from Yusi.YuPoint.point import PointType, AgeGroup
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuRanker.age_group_rank_adjuster import AgeGroupRankAdjuster
from Yusi.YuRanker.point_type_rank_adjuster import PointTypeRankAdjuster
from Yusi.YuRanker.points_ranker import PointsRanker
from Yusi.YuRanker.popularity_rank_adjuster import PopularityRankAdjuster


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


def GetCityVisitParameters(day_visit_parameterss):
  parameters_point_types = PointType(
      city_tours=90,
      landmarks=90,
      nature=10,
      museums=10,
      shopping=50,
      dining=50)

  parameters_age_groups = AgeGroup(
      senior=None,
      adult=90,
      junior=None,
      child=None,
      toddlers=10)

  return CityVisitParameters(
      day_visit_parameterss=day_visit_parameterss,
      point_type=parameters_point_types,
      age_group=parameters_age_groups)


class PointsRankerRunner(object):
  
  def __init__(self):
    rank_adjusters = [PopularityRankAdjuster(),
                      PointTypeRankAdjuster(),
                      AgeGroupRankAdjuster()]
    
    self.points_ranker = PointsRanker(rank_adjusters)
    
  def Run(self, points_input, city_visit_parameters):
    start = datetime.datetime.now()

    points_ranked = (
        self.points_ranker.RankPoints(points_input, city_visit_parameters))

    print('Input points: %s' %
          ', '.join(point.name for point in points_input))
    print('Points ranked: %s' %
          ', '.join(point_left.name for point_left in points_ranked))
    print('Elapsed time %s' % (datetime.datetime.now() - start))
