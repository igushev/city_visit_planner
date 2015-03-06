import unittest

import Yusi
from Yusi.YuRouter.day_visit_heap import PointsCalculator, DayVisitHeap
from Yusi.YuRouter.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface
from Yusi.YuPoint.point import PointInterface


class MockPoint(PointInterface):
  pass


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

    visit_a = PointsCalculator([MockPoint(), MockPoint()],
                               MockDayVisitCostCalculator(1))    
    day_visit_heap.Append(visit_a)
    self.assertEqual(1, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    visit_b = PointsCalculator([MockPoint(), MockPoint()],
                               MockDayVisitCostCalculator(9))
    day_visit_heap.Append(visit_b)
    self.assertEqual(2, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    # Should evict visit_b.
    visit_c = PointsCalculator([MockPoint(), MockPoint()],
                               MockDayVisitCostCalculator(5))
    day_visit_heap.Append(visit_c)
    self.assertEqual(3, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)
    
    day_visit_heap.Shrink()
    self.assertEqual(2, day_visit_heap.Size())
    self.assertEqual([visit_a, visit_c],
                     day_visit_heap.GetPointsCalculatorList())
    
    # Should evict visit_c
    visit_d = PointsCalculator([MockPoint(), MockPoint()],
                               MockDayVisitCostCalculator(3))
    day_visit_heap.Append(visit_d)
    self.assertEqual(3, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    visit_e = PointsCalculator([MockPoint(), MockPoint()],
                               MockDayVisitCostCalculator(7))
    day_visit_heap.Append(visit_e)
    self.assertEqual(4, day_visit_heap.Size())
    self.assertRaises(AssertionError, day_visit_heap.GetPointsCalculatorList)

    day_visit_heap.Shrink()
    self.assertEqual(2, day_visit_heap.Size())
    self.assertEqual([visit_a, visit_d],
                     day_visit_heap.GetPointsCalculatorList())

    # Number of points in inconsistent.
    visit_f = PointsCalculator([MockPoint(), MockPoint(), MockPoint()],
                               MockDayVisitCostCalculator(1))
    self.assertRaises(AssertionError, day_visit_heap.Append, visit_f)
    self.assertEqual(2, day_visit_heap.Size())
    self.assertEqual([visit_a, visit_d],
                     day_visit_heap.GetPointsCalculatorList())

    day_visit_heap.Clear()
    self.assertEqual(0, day_visit_heap.Size())
    self.assertEqual([], day_visit_heap.GetPointsCalculatorList())
    


if __name__ == '__main__':
    unittest.main()
  