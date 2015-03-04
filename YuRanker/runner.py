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


class Runner(object):
  
  def __init__(self):
    points = ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))

    self.points_to_visit = points.values()

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

    city_visit_parameters = CityVisitParameters(
        day_visit_parameterss=[MockDayVisitParameters()],
        point_type=parameters_point_types,
        age_group=parameters_age_groups)

    rank_adjusters = [PopularityRankAdjuster(),
                      PointTypeRankAdjuster(),
                      AgeGroupRankAdjuster()]
    
    points_ranker = PointsRanker(rank_adjusters)
    
    self.points_ranked = points_ranker.RankPoints(
        self.points_to_visit, city_visit_parameters)


def main():
  start = datetime.datetime.now()
  runner = Runner()
  print('Input points: %s' %
        ', '.join(point.name for point in runner.points_to_visit))
  print('Points ranked: %s' %
        ', '.join(point_left.name for point_left in runner.points_ranked))
  print('Elapsed time %s' % (datetime.datetime.now() - start))


if __name__ == '__main__':
  main()
