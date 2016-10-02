from Yusi.YuFinder.runner import MockDatabaseConnection, CityVisitFinderRunner
from Yusi.YuRanker.runner import GetPointsInput, GetCityVisitParameters
from Yusi.YuRouter.runner import GetDayVisitParameterss


def main():
  points_dict = GetPointsInput('YuPoint', 'test_sf_1.csv')
  points_input = points_dict.values()
  database_connection = MockDatabaseConnection(points_input)
  
  start_end_coordinates = points_dict['Union Square'].coordinates_starts
  first_day, last_day = 1, 4
  day_visit_parameterss = (
      GetDayVisitParameterss(start_end_coordinates, first_day, last_day))
  city_visit_parameters = GetCityVisitParameters(day_visit_parameterss)

  city_visit_finder_runner = CityVisitFinderRunner(database_connection)
  city_visit_finder_runner.Run(city_visit_parameters)


if __name__ == '__main__':
  main()
