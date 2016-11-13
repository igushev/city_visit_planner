from Yusi.YuFinder.runner import CityVisitFinderRunner
from Yusi.YuPoint.point import Coordinates
from Yusi.YuRanker.runner import GetCityVisitParameters
from Yusi.YuRouter.runner import GetDayVisitParameterss
from Yusi.YuPoint.city_visit import VisitLocation
from Yusi.YuPoint.test_utils import MockDatabaseConnection


def main():
  city_visit_finder_runner = CityVisitFinderRunner()

  visit_location = VisitLocation('New York City')
  # 746 Ninth Ave, New York, NY 10019.
  start_end_coordinates = Coordinates(40.763582, -73.988470)
  first_day, last_day = 13, 16
  day_visit_parameterss = (
      GetDayVisitParameterss(start_end_coordinates, first_day, last_day))
  city_visit_parameters = (
      GetCityVisitParameters(visit_location, day_visit_parameterss))
  
  city_visit_finder_runner.Run(city_visit_parameters)


if __name__ == '__main__':
  main()
