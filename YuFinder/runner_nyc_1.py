from Yusi.YuFinder.runner import MockDatabaseConnection, CityVisitFinderRunner
from Yusi.YuPoint.point import Coordinates
from Yusi.YuRanker.runner import GetPointsInput, GetCityVisitParameters
from Yusi.YuRouter.runner import GetDayVisitParameterss


def main():
  points_input = GetPointsInput('YuPoint', 'test_nyc_1.csv').values()
  database_connection = MockDatabaseConnection(points_input)

  # 746 Ninth Ave, New York, NY 10019.
  start_end_coordinates = Coordinates(40.763582, -73.988470)
  first_day, last_day = 13, 16
  day_visit_parameterss = (
      GetDayVisitParameterss(start_end_coordinates, first_day, last_day))
  city_visit_parameters = GetCityVisitParameters(day_visit_parameterss)
  
  city_visit_finder_runner = CityVisitFinderRunner(database_connection)
  city_visit_finder_runner.Run(city_visit_parameters)


if __name__ == '__main__':
  main()
