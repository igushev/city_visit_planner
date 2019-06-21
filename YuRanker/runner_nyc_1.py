from YuPoint import test_util as point_test_util
from YuRanker import runner as ranker_runner
from YuRanker import test_util as ranker_test_util


def main():
  points_input = list(point_test_util.GetPointsInput('YuPoint', 'test_nyc_1.csv').values())
  points_ranker_runner = ranker_runner.PointsRankerRunner()
  city_visit_parameters = (
      ranker_runner.GetCityVisitParameters(ranker_test_util.MockVisitLocation(),
                                           [ranker_test_util.MockDayVisitParameters()]))
  points_ranker_runner.Run(points_input, city_visit_parameters)


if __name__ == '__main__':
  main()
