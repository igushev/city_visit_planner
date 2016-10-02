from Yusi.YuPoint.point import Coordinates
from Yusi.YuRanker.runner import GetPointsKeys, FilterAndSortByKeys,\
  GetPointsInput
from Yusi.YuRouter.runner import GetDayVisitParameterss, CityVisitRouterRunner


def main():
  points_dict = GetPointsInput('YuPoint', 'test_nyc_1.csv')
  points_keys = GetPointsKeys('YuRouter', 'test_points_nyc.txt')
  points_input = FilterAndSortByKeys(points_dict, points_keys)

  # 746 Ninth Ave, New York, NY 10019.
  start_end_coordinates = Coordinates(40.763582, -73.988470)
  first_day, last_day = 13, 16
  day_visit_parameterss = (
      GetDayVisitParameterss(start_end_coordinates, first_day, last_day))
  city_visit_router_runner = CityVisitRouterRunner()
  city_visit_router_runner.Run(
      points_input, day_visit_parameterss)


if __name__ == '__main__':
  main()
