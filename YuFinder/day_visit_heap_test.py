import unittest

import Yusi
from Yusi.YuFinder.day_visit_heap import PointsCalculator, DayVisitHeap
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface


class MockPoints(object):
  def __init__(self, size):
    self.size = size
  
  def __len__(self):
    return self.size


class MockDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  def __init__(self, cost):
    self.cost = cost
  
  def FinalizedCost(self):
    return self.cost


class DayVisitHeapTest(unittest.TestCase):
  
  def testGeneral(self):
    day_visit_heap = DayVisitHeap(2)
    self.assertEqual(0, day_visit_heap.Size())
    self.assertEqual([], day_visit_heap.GetPointsCalculatorList())

    visit_a = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator(1))    
    day_visit_heap.Append(visit_a)
    self.assertEqual(1, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    visit_b = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator(9))
    day_visit_heap.Append(visit_b)
    self.assertEqual(2, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    # Should evict visit_b.
    visit_c = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator(5))
    day_visit_heap.Append(visit_c)
    self.assertEqual(3, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)
    
    day_visit_heap.Shrink()
    self.assertEqual(2, day_visit_heap.Size())
    self.assertEqual([visit_a, visit_c],
                     day_visit_heap.GetPointsCalculatorList())
    
    # Should evict visit_c
    visit_d = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator(3))
    day_visit_heap.Append(visit_d)
    self.assertEqual(3, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    visit_e = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator(7))
    day_visit_heap.Append(visit_e)
    self.assertEqual(4, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    day_visit_heap.Shrink()
    self.assertEqual(2, day_visit_heap.Size())
    self.assertEqual([visit_a, visit_d],
                     day_visit_heap.GetPointsCalculatorList())

    # Number of points in inconsistent.
    visit_f = PointsCalculator(MockPoints(3), MockDayVisitCostCalculator(1))
    self.assertRaises(AssertionError, day_visit_heap.Append, visit_f)
    self.assertEqual(2, day_visit_heap.Size())
    self.assertEqual([visit_a, visit_d],
                     day_visit_heap.GetPointsCalculatorList())

    day_visit_heap.Clear()
    self.assertEqual(0, day_visit_heap.Size())
    self.assertEqual([], day_visit_heap.GetPointsCalculatorList())
    


if __name__ == '__main__':
    unittest.main()
  