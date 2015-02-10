import os
import unittest

import Yusi
from Yusi.YuFinder.read_csv import ReadCSV


class PointTest(unittest.TestCase):

  def testStr(self):
    points = ReadCSV(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    point_0_str_actual = '%s' % points[0]
    point_0_str_expected = """Name "Ferry Building"
Coordinates Starts 37.7955:-122.3937
Coordinates Ends 37.7955:-122.3937
Operating Hours 09:00:00 - 18:00:00
Duration 1.00
"""
    self.assertEqual(point_0_str_expected, point_0_str_actual)


if __name__ == '__main__':
    unittest.main()

