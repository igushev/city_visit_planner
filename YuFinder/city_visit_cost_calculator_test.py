import unittest

from Yusi.YuFinder.city_visit_test_utils import CityVisitTestExample
from Yusi.YuFinder.city_visit_cost_calculator import CityVisitCostCalculator
from Yusi.YuFinder.cost_accumulator import FactorCostAccumulatorGenerator


class CityVisitCostCalculatorTest(CityVisitTestExample):

  def setUp(self):
    self.no_point_visit_factor = 0
    self.no_point_visit_const = 1000
    cost_accumulator_generator=FactorCostAccumulatorGenerator(
        no_point_visit_factor=self.no_point_visit_factor,
        no_point_visit_const=self.no_point_visit_const)
    self.city_visit_cost_calculator = CityVisitCostCalculator(
        cost_accumulator_generator=cost_accumulator_generator)
    super(CityVisitCostCalculatorTest, self).setUp()

  def testCalculateCityVisitCostGeneral(self):
    # No points left.
    cost = self.city_visit_cost_calculator.CalculateCityVisitCost(
       [self.day_visit_1, self.day_visit_2], [])
    self.assertEqual(8.25, cost)

    # One points left.
    cost = self.city_visit_cost_calculator.CalculateCityVisitCost(
       [self.day_visit_1, self.day_visit_2],
       [self.points['Union Square']])
    self.assertEqual(8.25 + self.no_point_visit_const, cost)

    # Two points left.
    cost = self.city_visit_cost_calculator.CalculateCityVisitCost(
       [self.day_visit_1, self.day_visit_2],
       [self.points['Union Square'], self.points['Lombard Street']])
    self.assertEqual(8.25 + 2 * self.no_point_visit_const, cost)

    # No day Visits and no points left.
    cost = self.city_visit_cost_calculator.CalculateCityVisitCost([], [])
    self.assertEqual(0., cost)

    # No day visits and one point left.
    cost = self.city_visit_cost_calculator.CalculateCityVisitCost(
       [], [self.points['Union Square']])
    self.assertEqual(self.no_point_visit_const, cost)

    # No day visits and two points left.
    cost = self.city_visit_cost_calculator.CalculateCityVisitCost(
       [], [self.points['Union Square'], self.points['Lombard Street']])
    self.assertEqual(2 * self.no_point_visit_const, cost)
    

if __name__ == '__main__':
    unittest.main()
  