import datetime
import unittest

import Yusi
from Yusi.YuFinder.cost_accumulator import SimpleCostAccumulatorGenerator
from Yusi.YuFinder.day_visit_finder import DayVisitFinder
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuFinder import test_utils
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.day_visit_finder_heap import EverythingDayVisitFinderHeapGenerator


class DayVisitFinderTest(unittest.TestCase):

  @staticmethod
  def GetDayVisitParameters(start_datetime, end_datetime):
    return city_visit.DayVisitParameters(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        lunch_start_datetime=datetime.datetime(
            start_datetime.year, start_datetime.month, start_datetime.day,
            13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))

  def setUp(self):
    self.points = test_utils.MockPoints()
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_cost_calculator_generator = DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=SimpleCostAccumulatorGenerator())
    day_visit_finder_heap_generator = EverythingDayVisitFinderHeapGenerator()
    self.day_visit_finder = DayVisitFinder(
        day_visit_cost_calculator_generator,
        day_visit_finder_heap_generator)
    unittest.TestCase.setUp(self)
    
    
  def testTwoFitTwoLeft(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0))

    points_left, day_visit_best = self.day_visit_finder.FindDayVisit(
        [self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Twin Peaks']],
        day_visit_parameters)

    self.assertEqual([self.points['Pier 39'], self.points['Golden Gate Bridge']],
                     points_left)
    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 10.50
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Walking from Ferry Biulding to Twin Peaks from 11:00:00 to 16:00:00
Having lunch from 16:00:00 to 17:00:00
Visiting point "Twin Peaks" from 17:00:00 to 17:30:00
Walking from Twin Peaks to Restaurant from 17:30:00 to 19:30:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))

  def testEverythingFit(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0))

    points_left, day_visit_best = self.day_visit_finder.FindDayVisit(
        [self.points['Ferry Biulding'],
         self.points['Pier 39']],
        day_visit_parameters)

    self.assertEqual([], points_left)
    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 11.00
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Walking from Ferry Biulding to Pier 39 from 11:00:00 to 12:00:00
Visiting point "Pier 39" from 12:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))

  def testNothingFit(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 10, 30, 0))

    points_left, day_visit_best = self.day_visit_finder.FindDayVisit(
      [self.points['Ferry Biulding'],
       self.points['Pier 39'],
       self.points['Golden Gate Bridge'],
       self.points['Twin Peaks']],
      day_visit_parameters)

    self.assertEqual(
        [self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Twin Peaks']],
        points_left)
    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 1.00
Walking from Hotel to Restaurant from 09:00:00 to 10:00:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))
    
  def testNoPoints(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0))

    points_left, day_visit_best = self.day_visit_finder.FindDayVisit(
        [],
        day_visit_parameters)

    self.assertEqual([], points_left)
    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 1.00
Walking from Hotel to Restaurant from 09:00:00 to 10:00:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))


if __name__ == '__main__':
    unittest.main()
