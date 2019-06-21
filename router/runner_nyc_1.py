from data import point
from data import test_util
from router import runner as router_runner


def main():
  points_dict = test_util.GetPointsInput('data', 'test_nyc_1.csv')
  points_keys = test_util.GetPointsKeys('router', 'test_points_nyc.txt')
  points_input = test_util.FilterAndSortByKeys(points_dict, points_keys)

  # 746 Ninth Ave, New York, NY 10019.
  start_end_coordinates = point.Coordinates(40.763582, -73.988470)
  first_day, last_day = 13, 16
  day_visit_parameterss = router_runner.GetDayVisitParameterss(start_end_coordinates, first_day, last_day)
  city_visit_router_runner = router_runner.CityVisitRouterRunner()
  city_visit_router_runner.Run(points_input, day_visit_parameterss)


if __name__ == '__main__':
  main()
