import unittest

import Yusi
from Yusi.YuRouter.runner import CityVisitRouterRunner, GetPointsInput,\
  GetDayVisitParameterss


class CityVisitRouterRunnerTest(unittest.TestCase):
  
  def testGeneral(self):
    CityVisitRouterRunner().Run(GetPointsInput(), GetDayVisitParameterss())


if __name__ == '__main__':
    unittest.main()
