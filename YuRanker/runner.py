import datetime
import os

import Yusi
from Yusi.YuPoint.city_visit import CityVisitParameters
from Yusi.YuPoint.point import PointType, AgeGroup
from Yusi.YuConfig.config import GetConfig, GetPointsRanker


def GetCityVisitParameters(visit_location, day_visit_parameterss):
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
      visit_location=visit_location,
      day_visit_parameterss=day_visit_parameterss,
      point_type=parameters_point_types,
      age_group=parameters_age_groups)


class PointsRankerRunner(object):
  
  def __init__(self):
    config = (
        GetConfig(os.path.join(
            Yusi.GetYusiDir(), 'YuConfig', 'runner.config')))
    self.points_ranker = GetPointsRanker(config)
    
  def Run(self, points_input, city_visit_parameters):
    start = datetime.datetime.now()

    points_ranked = (
        self.points_ranker.RankPoints(points_input, city_visit_parameters))

    print('Input points: %s' %
          ', '.join(point.name for point in points_input))
    print('Points ranked: %s' %
          ', '.join(point_left.name for point_left in points_ranked))
    print('Elapsed time %s' % (datetime.datetime.now() - start))
