import os
import unittest

from data import read_csv
from data import point


class PointTypeTest(unittest.TestCase):
  
  def testStr(self):
    point_type = point.PointType(
        city_tours=None,
        landmarks=None,
        nature=None,
        museums=None,
        shopping=None,
        dining=None)
    self.assertEqual('No point type', '%s' % point_type)

    point_type = point.PointType(
        city_tours=None,
        landmarks=30,
        nature=None,
        museums=None,
        shopping=50,
        dining=50)
    self.assertEqual('Dining (50), Shopping (50), Landmarks (30)',
                     '%s' % point_type)

class AgeGroupTest(unittest.TestCase):

  def testStr(self):
    age_group = point.AgeGroup(
        senior=None,
        adult=None,
        junior=None,
        child=None,
        toddlers=None)
    self.assertEqual('No age group', '%s' % age_group)

    age_group = point.AgeGroup(
        senior=50,
        adult=50,
        junior=30,
        child=None,
        toddlers=None)
    self.assertEqual('Adult (50), Senior (50), Junior (30)',
                     '%s' % age_group)


class PointTest(unittest.TestCase):

  def testStr(self):
    points = read_csv.ReadCSVToDict(os.path.join('data', 'test_sf_1.csv'))

    ferry_building_str_actual = '%s' % points['Ferry Building']
    ferry_building_str_expected = """Name: "Ferry Building"
Coordinates Starts: 37.7955:-122.3937
Coordinates Ends: 37.7955:-122.3937
Operating Hours: 09:00:00 - 18:00:00
Duration: 1.00
Popularity: 80
Point type: Landmarks (100)
Age group: Adult (90), Senior (90), Child (70), Junior (40)
Price: 0.00
Parking: 0
Eating: 100
"""
    self.assertEqual(ferry_building_str_expected, ferry_building_str_actual)
    
    golden_gate_bridge_str_actual = '%s' % points['Golden Gate Bridge']
    ferry_building_str_expected = """Name: "Golden Gate Bridge"
Coordinates Starts: 37.8197:-122.4786
Coordinates Ends: 37.8197:-122.4786
Operating Hours: 24/7
Duration: 0.50
Popularity: 100
Point type: Landmarks (100), City Tours (50)
Age group: Adult (90), Child (70), Junior (70), Senior (70)
Price: 0.00
Parking: 50
Eating: 0
"""
    self.assertEqual(ferry_building_str_expected, golden_gate_bridge_str_actual)


if __name__ == '__main__':
    unittest.main()

