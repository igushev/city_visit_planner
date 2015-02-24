import unittest

from Yusi.YuFinder.city_visit_cost_calculator import CityVisitCostCalculatorGenerator
from Yusi.YuFinder.cost_accumulator import FactorCostAccumulatorGenerator
from Yusi.YuPoint.city_visit_test_utils import CityVisitTestExample


class CityVisitCostCalculatorTest(CityVisitTestExample):

  def setUp(self):
    self.no_point_visit_factor = 0
    self.no_point_visit_const = 1000
    cost_accumulator_generator=FactorCostAccumulatorGenerator(
        no_point_visit_factor=self.no_point_visit_factor,
        no_point_visit_const=self.no_point_visit_const)
    self.city_visit_cost_calculator_generator = (
        CityVisitCostCalculatorGenerator(
            cost_accumulator_generator=cost_accumulator_generator))
    super(CityVisitCostCalculatorTest, self).setUp()

  def testDayVisitsNoPointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate(
            [self.day_visit_1, self.day_visit_2]))
    self.assertEqual(8.25, city_visit_cost_calculator.Cost())

  def testDayVisitsOnePointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate(
            [self.day_visit_1, self.day_visit_2]))
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Union Square']])
    self.assertEqual(8.25 + self.no_point_visit_const,
                     city_visit_cost_calculator.Cost())

  def testDayVisitsTwoPointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate(
            [self.day_visit_1, self.day_visit_2]))
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Union Square'], self.points['Lombard Street']])
    self.assertEqual(8.25 + 2 * self.no_point_visit_const,
                     city_visit_cost_calculator.Cost())

  def testDayVisitsFourPointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate(
            [self.day_visit_1, self.day_visit_2]))
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Union Square'], self.points['Lombard Street']])
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Coit Tower'], self.points['Att Park']])
    self.assertEqual(8.25 + 4 * self.no_point_visit_const,
                     city_visit_cost_calculator.Cost())

  def testNoDayVisitsNoPointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate([]))
    self.assertEqual(0., city_visit_cost_calculator.Cost())

  def testNoDayVisitsOnePointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate([]))
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Union Square']])
    self.assertEqual(self.no_point_visit_const,
                     city_visit_cost_calculator.Cost())

  def testNoDayVisitsTwoPointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate([]))
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Union Square'], self.points['Lombard Street']])
    self.assertEqual(2 * self.no_point_visit_const,
                     city_visit_cost_calculator.Cost())

  def testNoDayVisitsFourPointsLeft(self):
    city_visit_cost_calculator = (
        self.city_visit_cost_calculator_generator.Generate([]))
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Union Square'], self.points['Lombard Street']])
    city_visit_cost_calculator.AddPointsLeft(
        [self.points['Coit Tower'], self.points['Att Park']])
    self.assertEqual(4 * self.no_point_visit_const,
                     city_visit_cost_calculator.Cost())
    

if __name__ == '__main__':
    unittest.main()
  