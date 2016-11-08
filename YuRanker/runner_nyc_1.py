from Yusi.YuRanker.runner import PointsRankerRunner, GetPointsInput,\
  GetCityVisitParameters
from Yusi.YuRanker.test_utils import MockDayVisitParameters, MockVisitLocation


def main():
  points_input = GetPointsInput('YuPoint', 'test_nyc_1.csv').values()
  points_ranker_runner = PointsRankerRunner()
  city_visit_parameters = (
      GetCityVisitParameters(MockVisitLocation(), [MockDayVisitParameters()]))
  points_ranker_runner.Run(points_input, city_visit_parameters)


if __name__ == '__main__':
  main()
