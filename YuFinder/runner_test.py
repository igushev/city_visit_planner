import unittest

import Yusi
from Yusi.YuFinder.runner import GetPointsInput, MockDatabaseConnection,\
  CityVisitFinderRunner
from Yusi.YuRouter.runner import GetDayVisitParameterss
from Yusi.YuRanker.runner import GetCityVisitParameters


class CityVisitFinderRunnerTest(unittest.TestCase):
  
  def testGeneral(self):
    (CityVisitFinderRunner(
         MockDatabaseConnection(GetPointsInput())).
     Run(GetCityVisitParameters(GetDayVisitParameterss())))


if __name__ == '__main__':
    unittest.main()
  