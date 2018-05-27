from YuPoint import test_utils as point_test_utils
from YuRanker import runner as ranker_runner
from YuRanker import test_utils as ranker_test_utils


def main():
  points_input = list(point_test_utils.GetPointsInput('YuPoint', 'test_sf_1.csv').values())
  points_ranker_runner = ranker_runner.PointsRankerRunner()
  city_visit_parameters = (
      ranker_runner.GetCityVisitParameters(ranker_test_utils.MockVisitLocation(),
                                           [ranker_test_utils.MockDayVisitParameters()]))
  points_ranker_runner.Run(points_input, city_visit_parameters)


if __name__ == '__main__':
  main()
