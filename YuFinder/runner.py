import datetime

from Yusi.YuFinder.city_visit_finder import CityVisitFinder
from Yusi.YuRanker.runner import PointsRankerRunner
from Yusi.YuRouter.runner import CityVisitRouterRunner
from Yusi.YuRouter.city_visit_accumulator import CityVisitAccumulatorGenerator


class CityVisitFinderRunner(object):
  
  def __init__(self, database_connection):
    self.database_connection = database_connection
    points_ranker_runner = PointsRankerRunner()
    city_visit_router_runner = CityVisitRouterRunner()
    self.city_visit_finder = CityVisitFinder(
        database_connection=database_connection,
        points_ranker=points_ranker_runner.points_ranker,
        city_visit_router=city_visit_router_runner.city_visit_router)
    self.city_visit_accumulator_generator = CityVisitAccumulatorGenerator()

  def Run(self, city_visit_parameters):
    start = datetime.datetime.now()

    city_visit = self.city_visit_finder.FindCityVisit(
        city_visit_parameters, self.city_visit_accumulator_generator)

    print('Input points: %s' %
          ', '.join(point.name
                    for point in self.database_connection.GetPoints(
                        city_visit_parameters.visit_location)))
    print('Your schedule:')
    print(city_visit)
    print('Elapsed time %s' % (datetime.datetime.now() - start))
