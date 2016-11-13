import unittest

from Yusi.YuFinder.runner import CityVisitFinderRunner
from Yusi.YuRanker.runner import GetCityVisitParameters
from Yusi.YuRouter.runner import GetDayVisitParameterss
from Yusi.YuPoint.city_visit import VisitLocation
from Yusi.YuPoint.test_utils import MockDatabaseConnection


class CityVisitFinderRunnerTest(unittest.TestCase):
  
  def testGeneral(self):
    city_visit_finder_runner = CityVisitFinderRunner()
    visit_location = VisitLocation('San Francisco')
    start_end_coordinates = (
        city_visit_finder_runner.city_visit_finder.database_connection.
        GetPoint(visit_location, 'Union Square').coordinates_starts)
    first_day, last_day = 1, 2
    day_visit_parameterss = (
        GetDayVisitParameterss(start_end_coordinates, first_day, last_day))
    city_visit_parameters = (
        GetCityVisitParameters(visit_location, day_visit_parameterss))
  
    city_visit_finder_runner.Run(city_visit_parameters)


if __name__ == '__main__':
    unittest.main()
  