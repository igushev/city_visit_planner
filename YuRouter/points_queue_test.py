import datetime
import os
import unittest

from YuPoint import city_visit
from YuPoint import read_csv
from YuRouter import day_visit_cost_calculator_interface
from YuRouter import points_queue as points_queue_
from YuRouter import test_util


class MockDayVisitCostCalculator(day_visit_cost_calculator_interface.DayVisitCostCalculatorInterface):
  def __init__(self):
    pass


def GetDayVisitParameterss(first_day, last_day):
  def GetDayVisitParameters(day):
    return city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2015, 7, day, 10, 0, 0),
        end_datetime=datetime.datetime(2015, 7, day, 15, 0, 0),
        lunch_start_datetime=datetime.datetime(2015, 7, day, 14, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_util.MockCoordinates('Hotel'),
        end_coordinates=test_util.MockCoordinates('Hotel'))
  return [GetDayVisitParameters(day) for day in range(first_day, last_day)]


class OneByOnePointsQueueTest(unittest.TestCase):
  
  def setUp(self):
    self.points = read_csv.ReadCSVToDict(os.path.join('YuPoint', 'test_sf_1.csv'))

  def testGeneral(self):
    points = [self.points['Golden Gate Bridge'],
              self.points['Ferry Building'],
              self.points['Pier 39'],
              self.points['Union Square'],
              self.points['Twin Peaks']]
    day_visit_parameterss = [MockDayVisitCostCalculator()]

    points_queue = points_queue_.OneByOnePointsQueueGenerator().Generate(points)
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual(points, points_queue.GetPointsLeft())
    
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


class AllPointsQueueTest(unittest.TestCase):
  
  def setUp(self):
    self.points = read_csv.ReadCSVToDict(os.path.join('YuPoint', 'test_sf_1.csv'))

  def testGeneral(self):
    day_visit_parameterss = GetDayVisitParameterss(1, 3)
    points = [self.points['Golden Gate Bridge'],
              self.points['Ferry Building'],
              self.points['Pier 39'],
              self.points['Union Square'],
              self.points['Lombard Street'],
              self.points['Coit Tower'],
              self.points['Att Park'],
              self.points['Alcatraz Island'],
              self.points['Golden Gate Park'],
              self.points['De Young Museum']]
    
    points_queue = points_queue_.AllPointsQueueGenerator(1.2).Generate(points)
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual(points, points_queue.GetPointsLeft())

    self.assertEqual([self.points['Golden Gate Bridge'],
                      self.points['Ferry Building'],
                      self.points['Pier 39'],
                      self.points['Union Square'],
                      self.points['Lombard Street'],
                      self.points['Coit Tower'],
                      self.points['Att Park'],
                      self.points['Alcatraz Island']],
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual([self.points['Golden Gate Park'],
                      self.points['De Young Museum']],
                     points_queue.GetPointsLeft())

    self.assertEqual([self.points['Golden Gate Park'],
                      self.points['De Young Museum']],
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertFalse(points_queue.HasPoints())
    self.assertEqual([], points_queue.GetPointsLeft())

  def testLargeCutOffMultiplier(self):
    day_visit_parameterss = GetDayVisitParameterss(1, 3)
    points = [self.points['Golden Gate Bridge'],
              self.points['Ferry Building'],
              self.points['Pier 39'],
              self.points['Union Square'],
              self.points['Lombard Street'],
              self.points['Coit Tower'],
              self.points['Att Park'],
              self.points['Alcatraz Island'],
              self.points['Golden Gate Park'],
              self.points['De Young Museum']]
    
    points_queue = points_queue_.AllPointsQueueGenerator(2.0).Generate(points)
    self.assertTrue(points_queue.HasPoints())
    self.assertEqual(points, points_queue.GetPointsLeft())

    self.assertEqual(points,
                     points_queue.GetPushPoints(day_visit_parameterss))
    self.assertFalse(points_queue.HasPoints())
    self.assertEqual([], points_queue.GetPointsLeft())


if __name__ == '__main__':
    unittest.main()
