from data import city_visit
from data import runner_util
from data import test_util as point_test_util
from finder import runner as finder_runner


def main():
  points_dict = point_test_util.GetPointsInput('data', 'test_sf_1.csv')
  points_input = list(points_dict.values())
  city_visit_finder_runner = finder_runner.CityVisitFinderRunner()
  visit_location = city_visit.VisitLocation('San Francisco')
  start_end_coordinates = points_dict['Union Square'].coordinates_starts
  first_day, last_day = 1, 4
  day_visit_parameterss = runner_util.GetDayVisitParameterss(start_end_coordinates, first_day, last_day)
  city_visit_parameters = runner_util.GetCityVisitParameters(visit_location, day_visit_parameterss)

  city_visit_finder_runner.Run(points_input, city_visit_parameters)


if __name__ == '__main__':
  main()
