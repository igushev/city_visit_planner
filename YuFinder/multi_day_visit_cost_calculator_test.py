import unittest

import Yusi
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface,\
  DayVisitCostCalculatorGeneratorInterface
from Yusi.YuFinder.multi_day_visit_cost_calculator import MultiDayVisitCostCalculatorGenerator


class MockPoint():
  pass


class MockDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  
  def __init__(self, costs, finalization_cost, max_cost):
    self.costs = costs
    self.finalization_cost = finalization_cost
    self.max_cost = max_cost
    self.cost = 0
    self.pos = 0
    self._invariant = True
    
  def PushPoint(self, point):
    assert isinstance(point, MockPoint)
    assert self.pos <= len(self.costs)
    assert self._invariant
    self.cost += self.costs[self.pos]
    self.pos += 1
    if self.cost > self.max_cost:
      self._invariant = False
      return False
    return True
    
  def CanFinalize(self):
    assert self.pos <= len(self.costs)
    assert self._invariant
    if self.cost + self.finalization_cost > self.max_cost:
      return False
    return True
  
  def FinalizedCost(self):
    assert self.CanFinalize()
    return self.cost + self.finalization_cost

  def FinalizedDayVisit(self):
    assert self.CanFinalize()
    return self

  def Pos(self):
    assert self.pos <= len(self.costs)
    assert self._invariant
    return self.pos


class MockDayVisitCostCalculatorGenerator(DayVisitCostCalculatorGeneratorInterface):
  
  def __init__(self, costs, finalization_cost, max_cost):
    self.costs = costs
    self.finalization_cost = finalization_cost
    self.max_cost = max_cost

  def Generate(self):
    return MockDayVisitCostCalculator(
        self.costs, self.finalization_cost, self.max_cost)


class MultiDayVisitCostCalculatorTest(unittest.TestCase):
  
  def testBothFinalized(self):
    calculator_generator_1 = (
        MockDayVisitCostCalculatorGenerator([3, 4], 1, 9))
    calculator_generator_2 = (
        MockDayVisitCostCalculatorGenerator([1, 6], 2, 10))
    calculator = (
        MultiDayVisitCostCalculatorGenerator(
            [calculator_generator_1, calculator_generator_2]).
        Generate())
    calculator_1, calculator_2 = calculator.calculators

    # Empty calculator.
    # First one is better.
    self.assertEqual(0, calculator_1.Pos())
    self.assertEqual(0, calculator_2.Pos())
    self.assertEqual(2, calculator.Count())
    self.assertTrue(calculator_1.CanFinalize())
    self.assertTrue(calculator_2.CanFinalize())
    self.assertTrue(calculator.CanFinalize())
    self.assertEqual(1, calculator_1.FinalizedCost())
    self.assertEqual(2, calculator_2.FinalizedCost())
    self.assertEqual(1, calculator.FinalizedCost())
    self.assertIs(calculator_1, calculator.FinalizedDayVisit())

    # Pushing first point.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))
    self.assertEqual(1, calculator_1.Pos())
    self.assertEqual(1, calculator_2.Pos())
    self.assertEqual(2, calculator.Count())
    self.assertTrue(calculator_1.CanFinalize())
    self.assertTrue(calculator_2.CanFinalize())
    self.assertTrue(calculator.CanFinalize())
    self.assertEqual(4, calculator_1.FinalizedCost())
    self.assertEqual(3, calculator_2.FinalizedCost())
    self.assertEqual(3, calculator.FinalizedCost())
    self.assertIs(calculator_2, calculator.FinalizedDayVisit())

    # Pushing second point.
    # First one again better.
    self.assertTrue(calculator.PushPoint(MockPoint()))
    self.assertEqual(2, calculator_1.Pos())
    self.assertEqual(2, calculator_2.Pos())
    self.assertEqual(2, calculator.Count())
    self.assertTrue(calculator_1.CanFinalize())
    self.assertTrue(calculator_2.CanFinalize())
    self.assertTrue(calculator.CanFinalize())
    self.assertEqual(8, calculator_1.FinalizedCost())
    self.assertEqual(9, calculator_2.FinalizedCost())
    self.assertEqual(8, calculator.FinalizedCost())
    self.assertIs(calculator_1, calculator.FinalizedDayVisit())

  def testBothPushedOneFinalized(self):
    calculator_generator_1 = (
        MockDayVisitCostCalculatorGenerator([3, 4], 1, 7.5))
    calculator_generator_2 = (
        MockDayVisitCostCalculatorGenerator([1, 6], 2, 10))
    calculator = (
        MultiDayVisitCostCalculatorGenerator(
            [calculator_generator_1, calculator_generator_2]).
        Generate())
    calculator_1, calculator_2 = calculator.calculators

    # See testGeneral.
    # Empty calculator.
    # First one is better.
    # Pushing first point.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))

    # Pushing second point.
    # First one can't be finalized.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))
    self.assertEqual(2, calculator_1.Pos())
    self.assertEqual(2, calculator_2.Pos())
    self.assertEqual(2, calculator.Count())
    self.assertFalse(calculator_1.CanFinalize())
    self.assertTrue(calculator_2.CanFinalize())
    self.assertTrue(calculator.CanFinalize())
    self.assertRaises(AssertionError, calculator_1.FinalizedCost)
    self.assertEqual(9, calculator_2.FinalizedCost())
    self.assertEqual(9, calculator.FinalizedCost())
    self.assertIs(calculator_2, calculator.FinalizedDayVisit())

  def testBothPushedNoneFinalized(self):
    calculator_generator_1 = (
        MockDayVisitCostCalculatorGenerator([3, 4], 1, 7.5))
    calculator_generator_2 = (
        MockDayVisitCostCalculatorGenerator([1, 6], 2, 8))
    calculator = (
        MultiDayVisitCostCalculatorGenerator(
            [calculator_generator_1, calculator_generator_2]).
        Generate())
    calculator_1, calculator_2 = calculator.calculators

    # See testGeneral.
    # Empty calculator.
    # First one is better.
    # Pushing first point.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))

    # Pushing second point.
    # None can be finalized.
    self.assertTrue(calculator.PushPoint(MockPoint()))
    self.assertEqual(2, calculator_1.Pos())
    self.assertEqual(2, calculator_2.Pos())
    self.assertEqual(2, calculator.Count())
    self.assertFalse(calculator_1.CanFinalize())
    self.assertFalse(calculator_2.CanFinalize())
    self.assertFalse(calculator.CanFinalize())
    self.assertRaises(AssertionError, calculator_1.FinalizedCost)
    self.assertRaises(AssertionError, calculator_2.FinalizedCost)
    self.assertRaises(AssertionError, calculator.FinalizedCost)
    self.assertRaises(AssertionError, calculator.FinalizedDayVisit)

  def testOnePushedOneFinalized(self):
    calculator_generator_1 = (
        MockDayVisitCostCalculatorGenerator([3, 4], 1, 6))
    calculator_generator_2 = (
        MockDayVisitCostCalculatorGenerator([1, 6], 2, 10))
    calculator = (
        MultiDayVisitCostCalculatorGenerator(
            [calculator_generator_1, calculator_generator_2]).
        Generate())
    calculator_1, calculator_2 = calculator.calculators

    # See testGeneral.
    # Empty calculator.
    # First one is better.
    # Pushing first point.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))

    # Pushing second point.
    # First one can't be pushed.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))
    self.assertRaises(AssertionError, calculator_1.Pos)
    self.assertEqual(2, calculator_2.Pos())
    self.assertEqual(1, calculator.Count())
    self.assertRaises(AssertionError, calculator_1.CanFinalize)
    self.assertTrue(calculator_2.CanFinalize())
    self.assertTrue(calculator.CanFinalize())
    self.assertRaises(AssertionError, calculator_1.FinalizedCost)
    self.assertEqual(9, calculator_2.FinalizedCost())
    self.assertEqual(9, calculator.FinalizedCost())
    self.assertIs(calculator_2, calculator.FinalizedDayVisit())

  def testOnePushedNoneFinalized(self):
    calculator_generator_1 = (
        MockDayVisitCostCalculatorGenerator([3, 4], 1, 6))
    calculator_generator_2 = (
        MockDayVisitCostCalculatorGenerator([1, 6], 2, 8))
    calculator = (
        MultiDayVisitCostCalculatorGenerator(
            [calculator_generator_1, calculator_generator_2]).
        Generate())
    calculator_1, calculator_2 = calculator.calculators

    # See testGeneral.
    # Empty calculator.
    # First one is better.
    # Pushing first point.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))

    # Pushing second point.
    # First one can't be pushed.
    # Second cannot be finalized.
    self.assertTrue(calculator.PushPoint(MockPoint()))
    self.assertRaises(AssertionError, calculator_1.Pos)
    self.assertEqual(2, calculator_2.Pos())
    self.assertEqual(1, calculator.Count())
    self.assertRaises(AssertionError, calculator_1.CanFinalize)
    self.assertFalse(calculator_2.CanFinalize())
    self.assertFalse(calculator.CanFinalize())
    self.assertRaises(AssertionError, calculator_1.FinalizedCost)
    self.assertRaises(AssertionError, calculator_2.FinalizedCost)
    self.assertRaises(AssertionError, calculator.FinalizedCost)
    self.assertRaises(AssertionError, calculator.FinalizedDayVisit)

  def testNonePushed(self):
    calculator_generator_1 = (
        MockDayVisitCostCalculatorGenerator([3, 4], 1, 6))
    calculator_generator_2 = (
        MockDayVisitCostCalculatorGenerator([1, 6], 2, 4))
    calculator = (
        MultiDayVisitCostCalculatorGenerator(
            [calculator_generator_1, calculator_generator_2]).
        Generate())
    calculator_1, calculator_2 = calculator.calculators

    # See testGeneral.
    # Empty calculator.
    # First one is better.
    # Pushing first point.
    # Second one is better.
    self.assertTrue(calculator.PushPoint(MockPoint()))

    # Pushing second point.
    # None can't be pushed.
    self.assertFalse(calculator.PushPoint(MockPoint()))
    self.assertRaises(AssertionError, calculator_1.Pos)
    self.assertRaises(AssertionError, calculator_2.Pos)
    self.assertRaises(AssertionError, calculator.Count)
    self.assertRaises(AssertionError, calculator_1.CanFinalize)
    self.assertRaises(AssertionError, calculator_2.CanFinalize)
    self.assertRaises(AssertionError, calculator.CanFinalize)
    self.assertRaises(AssertionError, calculator_1.FinalizedCost)
    self.assertRaises(AssertionError, calculator_2.FinalizedCost)
    self.assertRaises(AssertionError, calculator.FinalizedCost)
    self.assertRaises(AssertionError, calculator.FinalizedDayVisit)


if __name__ == '__main__':
    unittest.main()
