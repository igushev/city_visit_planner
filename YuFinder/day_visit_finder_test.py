import datetime
import unittest

import Yusi
from Yusi.YuFinder.cost_accumulator import SimpleCostAccumulatorGenerator
from Yusi.YuFinder.day_visit_finder import FindDayVisit
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuFinder import test_utils
from Yusi.YuFinder import city_visit


def ExtractPointsNames(points):
  return [point.name for point in points]


class DayVisitFinderTest(unittest.TestCase):

  def testTwoFitTwoLeft(self):
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_parameters = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))
    day_visit_cost_calculator_generator = DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=SimpleCostAccumulatorGenerator())

    points = test_utils.MockPoints()

    points_left, day_visit_best = FindDayVisit(
        [points['Ferry Biulding'],
         points['Pier 39'],
         points['Golden Gate Bridge'],
         points['Twin Peaks']],
        day_visit_parameters,
        day_visit_cost_calculator_generator)

    self.assertEqual([points['Pier 39'], points['Golden Gate Bridge']],
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
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_parameters = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))
    day_visit_cost_calculator_generator = DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=SimpleCostAccumulatorGenerator())

    points = test_utils.MockPoints()

    points_left, day_visit_best = FindDayVisit(
        [points['Ferry Biulding'],
         points['Pier 39']],
        day_visit_parameters,
        day_visit_cost_calculator_generator)

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
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_parameters = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 10, 30, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))
    day_visit_cost_calculator_generator = DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=SimpleCostAccumulatorGenerator())

    points = test_utils.MockPoints()

    points_left, day_visit_best = FindDayVisit(
        [points['Ferry Biulding'],
         points['Pier 39'],
         points['Golden Gate Bridge'],
         points['Twin Peaks']],
        day_visit_parameters,
        day_visit_cost_calculator_generator)

    self.assertEqual(
        [points['Ferry Biulding'],
         points['Pier 39'],
         points['Golden Gate Bridge'],
         points['Twin Peaks']],
        points_left)
    day_visit_best_str_expected = """Date: 2014-09-01
Cost: 1.00
Walking from Hotel to Restaurant from 09:00:00 to 10:00:00"""
    self.assertEqual(day_visit_best_str_expected, str(day_visit_best))


if __name__ == '__main__':
    unittest.main()
