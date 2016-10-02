import unittest

from Yusi.YuRanker.runner import GetPointsKeys, FilterAndSortByKeys,\
  GetPointsInput
from Yusi.YuRouter.runner import GetDayVisitParameterss, CityVisitRouterRunner


class CityVisitRouterRunnerTest(unittest.TestCase):
  
  def testGeneral(self):
    points_dict = GetPointsInput('YuPoint', 'test_sf_1.csv')
    points_keys = GetPointsKeys('YuRouter', 'test_points_sf.txt')
    points_input = FilterAndSortByKeys(points_dict, points_keys)
  
    start_end_coordinates = points_dict['Union Square'].coordinates_starts
    first_day, last_day = 1, 2
    day_visit_parameterss = (
        GetDayVisitParameterss(start_end_coordinates, first_day, last_day))
    
    city_visit_router_runner = CityVisitRouterRunner()
    city_visit_router_runner.Run(points_input, day_visit_parameterss)


if __name__ == '__main__':
    unittest.main()
