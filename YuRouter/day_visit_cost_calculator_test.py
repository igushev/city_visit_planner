import datetime
import unittest

from YuPoint import city_visit
from YuRouter import cost_accumulator
from YuRouter import point_fit as point_fit_
from YuRouter import day_visit_cost_calculator as day_visit_cost_calculator_
from YuRouter import test_utils


class DayVisitCostCalculatorTest(unittest.TestCase):

  @staticmethod
  def GetDayVisitParameters(start_datetime, end_datetime, lunch_start_datetime):
    return city_visit.DayVisitParameters(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        lunch_start_datetime=lunch_start_datetime,
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))

  def setUp(self):
    self.no_point_visit_factor = 0.
    self.no_point_visit_const = 1000.
    self.unused_time_factor = 0.01
    self.points = test_utils.MockPoints()
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = point_fit_.SimplePointFit()
    cost_accumulator_generator=cost_accumulator.FactorCostAccumulatorGenerator(
        no_point_visit_factor=self.no_point_visit_factor,
        no_point_visit_const=self.no_point_visit_const,
        unused_time_factor=self.unused_time_factor)
    self.day_visit_cost_calculator_generator = day_visit_cost_calculator_.DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=cost_accumulator_generator)
    super(DayVisitCostCalculatorTest, self).setUp()

  def testCannotAddPoint(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 15, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 14, 0, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Ferry Building.
    # Move: 9:00 - 10:00.
    # Point: 10:00 - 11:00.
    self.assertTrue(
        day_visit_cost_calculator.PushPoint(self.points['Ferry Building']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 11, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Ferry Building'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(2, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(8.95, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    # Pier 39.
    # Move: 11:00 - 12:00.
    # Point: 12:00 - 15:00.
    # Lunch: 15:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.75, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Pier 39 from 11:00:00 to 12:00:00
Visiting point "Pier 39" from 12:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Cost: 11.75
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

    # Twin Peaks.
    # Move: 16:00 - 21:00.
    # Cannot push point.
    # State should not have been changed, but cost should have been increased.
    self.assertFalse(
        day_visit_cost_calculator.PushPoint(self.points['Twin Peaks']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7 + self.no_point_visit_const,
                     day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.75 + self.no_point_visit_const,
                     day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([self.points['Twin Peaks']],
                     day_visit_cost_calculator.GetPointsLeft())

  def testCannotAddMove(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 20, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 11, 45, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Ferry Building.
    # Move: 9:00 - 10:00.
    # Point: 10:00 - 11:00.
    self.assertTrue(
        day_visit_cost_calculator.PushPoint(self.points['Ferry Building']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 11, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Ferry Building'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(2, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(8.6, day_visit_cost_calculator.FinalizedCost())  # Lunch.
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    # Pier 39.
    # Move: 11:00 - 12:00.
    # Lunch: 12:00 - 13:00.
    # Point: 13:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Cost: 11.00
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

    # Twin Peaks.
    # Cannot push move.
    # State should not have been changed, but cost should have been increased.
    self.assertFalse(
        day_visit_cost_calculator.PushPoint(self.points['Twin Peaks']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7 + self.no_point_visit_const,
                     day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11 + self.no_point_visit_const,
                     day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([self.points['Twin Peaks']],
                     day_visit_cost_calculator.GetPointsLeft())

  def testPointDoesNotFit(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 10, 30, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 30, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 9, 30, 0))  # out of time range.
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 10:30 - 13:30.
    # Point: 13:30 - 16:30.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.2, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Pier 39 from 10:30:00 to 13:30:00
Visiting point "Pier 39" from 13:30:00 to 16:30:00
Walking from Pier 39 to Restaurant from 16:30:00 to 20:30:00
Cost: 11.20
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))
    
    # Ferry Building.
    # Move: 16:30 - 17:30.
    # Point does not fit.
    # State should not have been changed, but cost should have been increased.
    self.assertFalse(
        day_visit_cost_calculator.PushPoint(self.points['Ferry Building']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6 + self.no_point_visit_const,
                     day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.2 + self.no_point_visit_const,
                     day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([self.points['Ferry Building']],
                     day_visit_cost_calculator.GetPointsLeft())

  def testCannotFinalize(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 18, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 12, 30, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Ferry Building.
    # Move: 9:00 - 10:00.
    # Point: 10:00 - 11:00.
    self.assertTrue(
        day_visit_cost_calculator.PushPoint(self.points['Ferry Building']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 11, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Ferry Building'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(2, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(7.4, day_visit_cost_calculator.FinalizedCost())  # Lunch.
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Restaurant from 11:00:00 to 13:00:00
Having lunch from 13:00:00 to 14:00:00
Cost: 7.40
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

    # Pier 39.
    # Move: 11:00 - 12:00.
    # Point: 12:00 - 15:00.
    # Lunch: 15:00 - 16:00.
    # Cannot finalize.
    # State should not have been changed, but cost should have been increased.
    self.assertFalse(
        day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 11, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Ferry Building'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(2 + self.no_point_visit_const,
                     day_visit_cost_calculator.CurrentCost())
    self.assertEqual(7.4 + self.no_point_visit_const,
                     day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([self.points['Pier 39']],
                     day_visit_cost_calculator.GetPointsLeft())

  def testLunchBeforeMove(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 10, 0, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Lunch: 09:00 - 10:00.
    # Move: 10:00 - 13:00.
    # Point: 13:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.6, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Having lunch from 09:00:00 to 10:00:00
Walking from Hotel to Pier 39 from 10:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Cost: 11.60
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

  def testLunchAfterMove(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 11, 0, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 09:00 - 12:00.
    # Lunch: 12:00 - 13:00.
    # Point: 13:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.6, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Pier 39 from 09:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Cost: 11.60
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

  def testLunchBeforePoint(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 09:00 - 12:00.
    # Lunch: 12:00 - 13:00.
    # Point: 13:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.6, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Pier 39 from 09:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Cost: 11.60
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

  def testLunchAfterPoint(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 14, 0, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 09:00 - 12:00.
    # Point: 12:00 - 15:00.
    # Lunch: 15:00 - 16:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(7, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.6, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Pier 39 from 09:00:00 to 12:00:00
Visiting point "Pier 39" from 12:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Cost: 11.60
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

  def testLunchBeforeFinalization(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 16, 0, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 09:00 - 12:00.
    # Point: 12:00 - 15:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 15, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.6, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Pier 39 from 09:00:00 to 12:00:00
Visiting point "Pier 39" from 12:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Cost: 11.60
Price: 0.00"""
    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

  def testLunchAfterFinalization(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 18, 0, 0))
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 09:00 - 12:00.
    # Point: 12:00 - 15:00.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 15, 0, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.6, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    day_visit_str_expected = """Date: 2014-09-01
Walking from Hotel to Pier 39 from 09:00:00 to 12:00:00
Visiting point "Pier 39" from 12:00:00 to 15:00:00
Walking from Pier 39 to Restaurant from 15:00:00 to 19:00:00
Having lunch from 19:00:00 to 20:00:00
Cost: 11.60
Price: 0.00"""

    self.assertEqual(day_visit_str_expected,
                     str(day_visit_cost_calculator.FinalizedDayVisit()))

  def testCannotPushPointAfterFail(self):
    day_visit_parameters = DayVisitCostCalculatorTest.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 10, 30, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 22, 30, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 9, 30, 0))  # out of time range.

    # Test that Union Square can be pushed by time.
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 10:30 - 13:30.
    # Point: 13:30 - 16:30.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.2, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    # Union Square.
    # Move: 16:30 - 18:30
    # Point: 18:30 - 19:30
    self.assertTrue(
        day_visit_cost_calculator.PushPoint(self.points['Union Square']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 19, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Union Square'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(9, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.2, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    # Test that Union Square can be pushed by time, but should not be since
    # previous step failed.
    day_visit_cost_calculator = (
        self.day_visit_cost_calculator_generator.Generate(
            day_visit_parameters))

    # Pier 39.
    # Move: 10:30 - 13:30.
    # Point: 13:30 - 16:30.
    self.assertTrue(day_visit_cost_calculator.PushPoint(self.points['Pier 39']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6, day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.2, day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([], day_visit_cost_calculator.GetPointsLeft())

    # Ferry Building.
    # Move: 16:30 - 17:30.
    # Point does not fit.
    # State should not have been changed, but cost should have been increased.
    self.assertFalse(
        day_visit_cost_calculator.PushPoint(self.points['Ferry Building']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6 + self.no_point_visit_const,
                     day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.2 + self.no_point_visit_const,
                     day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([self.points['Ferry Building']],
                     day_visit_cost_calculator.GetPointsLeft())

    # Union Square.
    # Point can be pushed by time, but should not be since previous step
    # failed.
    # State should not have been changed, but cost should have been increased.
    self.assertFalse(
        day_visit_cost_calculator.PushPoint(self.points['Union Square']))
    self.assertEqual(datetime.datetime(2014, 9, 1, 16, 30, 0),
                     day_visit_cost_calculator.CurrentTime())
    self.assertEqual(test_utils.MockCoordinates('Pier 39'),
                     day_visit_cost_calculator.CurrentCoordinates())
    self.assertEqual(6 + self.no_point_visit_const * 2,
                     day_visit_cost_calculator.CurrentCost())
    self.assertEqual(11.2 + self.no_point_visit_const * 2,
                     day_visit_cost_calculator.FinalizedCost())
    self.assertEqual([self.points['Ferry Building'], self.points['Union Square']],
                     day_visit_cost_calculator.GetPointsLeft())


if __name__ == '__main__':
    unittest.main()
