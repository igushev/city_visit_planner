import datetime
import unittest

import Yusi
from Yusi.YuFinder.cost_accumulator import FactorCostAccumulatorGenerator
from Yusi.YuFinder.day_visit_finder import DayVisitFinder
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuFinder.city_visit import DayVisitParameters
from Yusi.YuFinder.test_utils import MockCoordinates, MockPoints,\
  MockMoveCalculator


class DayVisitFinderTest(unittest.TestCase):

  @staticmethod
  def GetDayVisitParameters(start_datetime, end_datetime):
    return DayVisitParameters(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        lunch_start_datetime=datetime.datetime(
            start_datetime.year, start_datetime.month, start_datetime.day,
            13, 0, 0),
        lunch_hours=1.,
        start_coordinates=MockCoordinates('Hotel'),
        end_coordinates=MockCoordinates('Restaurant'))

  def setUp(self):
    no_point_visit_factor = 0
    no_point_visit_const = 1000
    day_visit_heap_size = 1000
    self.points = MockPoints()
    move_calculator = MockMoveCalculator()
    point_fit = SimplePointFit()
    cost_accumulator_generator=FactorCostAccumulatorGenerator(
        no_point_visit_factor=no_point_visit_factor,
        no_point_visit_const=no_point_visit_const)
    day_visit_cost_calculator_generator = DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=cost_accumulator_generator)
    self.day_visit_finder = DayVisitFinder(
        calculator_generator=day_visit_cost_calculator_generator,
        day_visit_heap_size=day_visit_heap_size)
    super(DayVisitFinderTest, self).setUp()
    
    
  def testTwoFitTwoLeft(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0))

    day_visit_best, points_left = self.day_visit_finder.FindDayVisit(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Twin Peaks']],
        day_visit_parameters)

    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 10.50
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Having lunch from 11:00:00 to 12:00:00
Walking from Ferry Building to Twin Peaks from 12:00:00 to 17:00:00
Visiting point "Twin Peaks" from 17:00:00 to 17:30:00
Walking from Twin Peaks to Restaurant from 17:30:00 to 19:30:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))
    self.assertEqual(
        [self.points['Pier 39'],
         self.points['Golden Gate Bridge']],
        points_left)

  def testEverythingFit(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0))

    day_visit_best, points_left = self.day_visit_finder.FindDayVisit(
        [self.points['Ferry Building'],
         self.points['Pier 39']],
        day_visit_parameters)

    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 11.00
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))
    self.assertEqual([], points_left)

  def testNothingFit(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 10, 30, 0))

    day_visit_best, points_left = self.day_visit_finder.FindDayVisit(
      [self.points['Ferry Building'],
       self.points['Pier 39'],
       self.points['Golden Gate Bridge'],
       self.points['Twin Peaks']],
      day_visit_parameters)

    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 1.00
Walking from Hotel to Restaurant from 09:00:00 to 10:00:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))
    self.assertEqual(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Twin Peaks']],
        points_left)
    
  def testNoPoints(self):
    day_visit_parameters = DayVisitFinderTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0))

    day_visit_best, points_left = self.day_visit_finder.FindDayVisit(
        [],
        day_visit_parameters)

    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 1.00
Walking from Hotel to Restaurant from 09:00:00 to 10:00:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))
    self.assertEqual([], points_left)


if __name__ == '__main__':
    unittest.main()
