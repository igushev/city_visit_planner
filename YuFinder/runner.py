import datetime

from Yusi.YuFinder.city_visit_finder import CityVisitFinder
from Yusi.YuFinder.database_connection import DatabaseConnectionInterface
from Yusi.YuRanker.runner import PointsRankerRunner, GetPointsInput
from Yusi.YuRouter.runner import CityVisitRouterRunner


class MockDatabaseConnection(DatabaseConnectionInterface):

  def __init__(self):
    self.points_dict_dict = {
        'New York City': GetPointsInput('YuPoint', 'test_nyc_1.csv'),
        'San Francisco': GetPointsInput('YuPoint', 'test_sf_1.csv')}

  def GetPoints(self, visit_location):
    return self.points_dict_dict[visit_location.city_name].values()

  def GetPoint(self, visit_location, point_name):
    return self.points_dict_dict[visit_location.city_name][point_name]


class CityVisitFinderRunner(object):
  
  def __init__(self, database_connection):
    self.database_connection = database_connection
    points_ranker_runner = PointsRankerRunner()
    city_visit_router_runner = CityVisitRouterRunner()
    self.city_visit_finder = CityVisitFinder(
        database_connection=database_connection,
        points_ranker=points_ranker_runner.points_ranker,
        city_visit_router=city_visit_router_runner.city_visit_router)

  def Run(self, city_visit_parameters):
    start = datetime.datetime.now()

    city_visit = self.city_visit_finder.FindCityVisit(city_visit_parameters)

    print('Input points: %s' %
          ', '.join(point.name
                    for point in self.database_connection.GetPoints(
                        city_visit_parameters.visit_location)))
    print('Your schedule:')
    print(city_visit)
    print('Elapsed time %s' % (datetime.datetime.now() - start))
