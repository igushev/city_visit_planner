import datetime
import os

import Yusi
from Yusi.YuFinder.city_visit_finder import CityVisitFinder
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuRanker.runner_nyc_1 import PointsRankerRunner, GetCityVisitParameters
from Yusi.YuRouter.runner_nyc_1 import CityVisitRouterRunner, GetDayVisitParameterss
from Yusi.YuFinder.database_connection import DatabaseConnectionInterface


def GetPointsInput():
  points = ReadCSVToDict(
      os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_nyc_1.csv'))
  return points.values()


class MockDatabaseConnection(DatabaseConnectionInterface):

  def __init__(self, points_input):
    self.points_input = points_input

  def GetPoints(self, city_visit_parameters):
    return self.points_input


class CityVisitFinderRunner(object):
  
  def __init__(self, database_connection):
    points_ranker_runner = PointsRankerRunner()
    city_visit_router_runner = CityVisitRouterRunner()
    self.city_visit_finder = CityVisitFinder(
        database_connection=database_connection,
        points_ranker=points_ranker_runner.points_ranker,
        city_visit_router=city_visit_router_runner.city_visit_router)

  def Run(self, city_visit_parameters):
    return self.city_visit_finder.FindCityVisit(city_visit_parameters)


def main():
  start = datetime.datetime.now()

  points_input = GetPointsInput()
  database_connection = MockDatabaseConnection(points_input)
  day_visit_parameterss = GetDayVisitParameterss()
  city_visit_parameters = GetCityVisitParameters(day_visit_parameterss)
  city_visit_finder_runner = CityVisitFinderRunner(database_connection)
  city_visit = city_visit_finder_runner.Run(city_visit_parameters)

  print('Input points: %s' %
        ', '.join(point.name for point in points_input))
  print('Your schedule:')
  print(city_visit)
  print('Elapsed time %s' % (datetime.datetime.now() - start))


if __name__ == '__main__':
  main()
