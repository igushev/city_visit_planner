from Yusi.YuRanker.runner import PointsRankerRunner, GetPointsInput,\
  GetCityVisitParameters
from Yusi.YuRanker.test_utils import MockDayVisitParameters


def main():
  points_input = GetPointsInput('YuPoint', 'test_sf_1.csv').values()
  points_ranker_runner = PointsRankerRunner()
  city_visit_parameters = GetCityVisitParameters([MockDayVisitParameters()])
  points_ranker_runner.Run(points_input, city_visit_parameters)


if __name__ == '__main__':
  main()
