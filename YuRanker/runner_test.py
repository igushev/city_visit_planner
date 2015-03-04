import unittest

import Yusi
from Yusi.YuRanker.runner import PointsRankerRunner, GetPointsInput,\
  GetCityVisitParameters
from Yusi.YuRanker.test_utils import MockDayVisitParameters


class PointsRankerRunnerTest(unittest.TestCase):
  
  def testGeneral(self):
    PointsRankerRunner().Run(
        GetPointsInput(), GetCityVisitParameters([MockDayVisitParameters()]))


if __name__ == '__main__':
    unittest.main()
