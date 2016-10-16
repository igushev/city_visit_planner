import os
import unittest

import Yusi
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuRouter.points_queue import OneByOnePointsQueueGenerator
from Yusi.YuRouter.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface


class MockDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  def __init__(self):
    pass


class OneByOnePointsQueueTest(unittest.TestCase):
  
  def setUp(self):
    self.points = ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))

  def testGeneral(self):
    points = [self.points['Golden Gate Bridge'],
              self.points['Ferry Building'],
              self.points['Pier 39'],
              self.points['Union Square'],
              self.points['Twin Peaks']]
    day_visit_parameterss = [MockDayVisitCostCalculator()]

    points_queue = OneByOnePointsQueueGenerator().Generate(points)
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual([self.points['Golden Gate Bridge'],
                      self.points['Ferry Building'],
                      self.points['Pier 39'],
                      self.points['Union Square'],
                      self.points['Twin Peaks']],
                     points_queue.GetPointsLeft())
    
    self.assertEqual([self.points['Golden Gate Bridge']],
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual([self.points['Ferry Building'],
                      self.points['Pier 39'],
                      self.points['Union Square'],
                      self.points['Twin Peaks']],
                     points_queue.GetPointsLeft())

    self.assertEqual([self.points['Ferry Building']],
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual([self.points['Pier 39'],
                      self.points['Union Square'],
                      self.points['Twin Peaks']],
                     points_queue.GetPointsLeft())

    self.assertEqual([self.points['Pier 39']],
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual([self.points['Union Square'],
                      self.points['Twin Peaks']],
                     points_queue.GetPointsLeft())
    
    points_queue.AddBackToQueue([self.points['Ferry Building'],
                                 self.points['Pier 39']])
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual([self.points['Ferry Building'],
                      self.points['Pier 39'],
                      self.points['Union Square'],
                      self.points['Twin Peaks']],
                     points_queue.GetPointsLeft())

    self.assertEqual([self.points['Ferry Building']],
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual([self.points['Pier 39'],
                      self.points['Union Square'],
                      self.points['Twin Peaks']],
                     points_queue.GetPointsLeft())

    points_queue.GetPushPoints(day_visit_parameterss)
    points_queue.GetPushPoints(day_visit_parameterss)
    self.assertEqual([self.points['Twin Peaks']],
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertFalse(points_queue.HasPoints())
    self.assertEqual([], points_queue.GetPointsLeft())


if __name__ == '__main__':
    unittest.main()

