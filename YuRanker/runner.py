import datetime
import os

import Yusi
from Yusi.YuPoint.city_visit import CityVisitParameters
from Yusi.YuPoint.point import PointType, AgeGroup
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuRanker.popularity_rank_adjuster import PopularityRankAdjuster
from Yusi.YuRanker.point_type_rank_adjuster import PointTypeRankAdjuster
from Yusi.YuRanker.age_group_rank_adjuster import AgeGroupRankAdjuster
from Yusi.YuRanker.points_ranker import PointsRanker
from Yusi.YuRanker.test_utils import MockDayVisitParameters


def GetPointsInput():
  points = ReadCSVToDict(
      os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
  return points.values()


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
    return self.points_ranker.RankPoints(points_input, city_visit_parameters)


def main():
  start = datetime.datetime.now()

  points_input = GetPointsInput()
  points_ranker_runner = PointsRankerRunner()
  city_visit_parameters = GetCityVisitParameters([MockDayVisitParameters()])
  points_ranked = points_ranker_runner.Run(points_input, city_visit_parameters)

  print('Input points: %s' %
        ', '.join(point.name for point in points_input))
  print('Points ranked: %s' %
        ', '.join(point_left.name for point_left in points_ranked))

  print('Elapsed time %s' % (datetime.datetime.now() - start))


if __name__ == '__main__':
  main()
