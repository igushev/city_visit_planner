import datetime
import unittest

import Yusi
from Yusi.YuFinder import test_utils
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.cost_accumulator import SimpleCostAccumulatorGenerator
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder.day_visit_cost_calculator import DayVisitCostCalculatorGenerator


class DayVisitCostCalculatorTest(unittest.TestCase):

  def testLunchDuringPointCannotPushPoint(self):
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_parameters = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 15, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))
    day_visit_cost_calculator = (
            DayVisitCostCalculatorGenerator(
                move_calculator=move_calculator,
                point_fit=point_fit,
                cost_accumulator_generator=SimpleCostAccumulatorGenerator()).
            Generate(day_visit_parameters))

    points = test_utils.MockPoints()

    # Ferry Biulding.
    # Move: 9:00 - 10:00.
    # Point: 10:00 - 11:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(points['Ferry Biulding']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 11, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Ferry Biulding'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(2, day_visit_cost_calculator.CurrentCost())
    self.assertTrue(day_visit_cost_calculator.CanFinalize())
    self.assertEqual(4, day_visit_cost_calculator.FinalizedCost())

    # Pier 39.
    # Move: 11:00 - 12:00.
    # Point: 12:00 - 15:00.
    # Lunch: 15:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertTrue(day_visit_cost_calculator.CanFinalize())
    self.assertEqual(11, day_visit_cost_calculator.FinalizedCost())

    day_visit_str_expected = """Date: 2014-09-01
Cost: 11.00
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Walking from Ferry Biulding to Pier 39 from 11:00:00 to 12:00:00
Visiting point "Pier 39" from 12:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

    # Twin Peaks.
    # Move: 16:00 - 21:00.
    # Cannot push point.
    self.assertFalse(day_visit_cost_calculator.PushPoint(points['Twin Peaks']))
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentTime)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentCoordinates)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentCost)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CanFinalize)
    self.assertRaises(AssertionError, day_visit_cost_calculator.FinalizedCost)

  def testLunchDuringMoveCannotPushMove(self):
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_parameters = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 20, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 11, 30, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))
    day_visit_cost_calculator = (
            DayVisitCostCalculatorGenerator(
                move_calculator=move_calculator,
                point_fit=point_fit,
                cost_accumulator_generator=SimpleCostAccumulatorGenerator()).
            Generate(day_visit_parameters))

    points = test_utils.MockPoints()

    # Ferry Biulding.
    # Move: 9:00 - 10:00.
    # Point: 10:00 - 11:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(points['Ferry Biulding']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 11, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Ferry Biulding'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(2, day_visit_cost_calculator.CurrentCost())
    self.assertTrue(day_visit_cost_calculator.CanFinalize())
    self.assertEqual(4, day_visit_cost_calculator.FinalizedCost())

    # Pier 39.
    # Move: 11:00 - 12:00.
    # Lunch: 12:00 - 13:00.
    # Point: 13:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertTrue(day_visit_cost_calculator.CanFinalize())
    self.assertEqual(11, day_visit_cost_calculator.FinalizedCost())

    day_visit_str_expected = """Date: 2014-09-01
Cost: 11.00
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Walking from Ferry Biulding to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

    # Twin Peaks.
    # Cannot push move.
    self.assertFalse(day_visit_cost_calculator.PushPoint(points['Twin Peaks']))
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentTime)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentCoordinates)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentCost)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CanFinalize)
    self.assertRaises(AssertionError, day_visit_cost_calculator.FinalizedCost)

  def testPointDoesNotFit(self):
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_parameters = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 10, 30, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 30, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 9, 30, 0),  # out of time range.
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))
    day_visit_cost_calculator = (
        DayVisitCostCalculatorGenerator(
            move_calculator=move_calculator,
            point_fit=point_fit,
            cost_accumulator_generator=SimpleCostAccumulatorGenerator()).
        Generate(day_visit_parameters))

    points = test_utils.MockPoints()

    # Pier 39.
    # Move: 10:30 - 13:30.
    # Point: 13:30 - 16:30.
    self.assertTrue(day_visit_cost_calculator.PushPoint(points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6, day_visit_cost_calculator.CurrentCost())
    self.assertTrue(day_visit_cost_calculator.CanFinalize())
    self.assertEqual(10, day_visit_cost_calculator.FinalizedCost())

    day_visit_str_expected = """Date: 2014-09-01
Cost: 10.00
Walking from Hotel to Pier 39 from 10:30:00 to 13:30:00
Visiting point "Pier 39" from 13:30:00 to 16:30:00
Walking from Pier 39 to Restaurant from 16:30:00 to 20:30:00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))
    
    # Ferry Biulding.
    # Move: 16:30 - 17:30.
    # Point does not fit.
    self.assertFalse(day_visit_cost_calculator.PushPoint(points['Ferry Biulding']))
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentTime)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentCoordinates)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CurrentCost)
    self.assertRaises(AssertionError, day_visit_cost_calculator.CanFinalize)
    self.assertRaises(AssertionError, day_visit_cost_calculator.FinalizedCost)

  def testCannotFinalize(self):
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    day_visit_parameters = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 18, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))
    day_visit_cost_calculator = (
        DayVisitCostCalculatorGenerator(
            move_calculator=move_calculator,
            point_fit=point_fit,
            cost_accumulator_generator=SimpleCostAccumulatorGenerator()).
        Generate(day_visit_parameters))

    points = test_utils.MockPoints()

    # Ferry Biulding.
    # Move: 9:00 - 10:00.
    # Point: 10:00 - 11:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(points['Ferry Biulding']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 11, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Ferry Biulding'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(2, day_visit_cost_calculator.CurrentCost())
    self.assertTrue(day_visit_cost_calculator.CanFinalize())
    self.assertEqual(4, day_visit_cost_calculator.FinalizedCost())

    # Pier 39.
    # Move: 11:00 - 12:00.
    # Point: 12:00 - 15:00.
    # Lunch: 15:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertFalse(day_visit_cost_calculator.CanFinalize())
    self.assertRaises(AssertionError, day_visit_cost_calculator.FinalizedCost)


if __name__ == '__main__':
    unittest.main()
