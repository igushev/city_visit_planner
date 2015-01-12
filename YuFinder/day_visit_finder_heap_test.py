import unittest

import Yusi
from Yusi.YuFinder.day_visit_finder_heap import EverythingDayVisitFinderHeapGenerator,\
  PointsCalculator
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface


class MockPoints(object):
  def __init__(self, size):
    self.size = size
  
  def __len__(self):
    return self.size


class MockDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  pass


class EverythingDayVisitFinderHeapTest(unittest.TestCase):
  
  def testGeneral(self):
    day_visit_finder_heap = EverythingDayVisitFinderHeapGenerator().Generate()
    self.assertEqual(0, day_visit_finder_heap.Size())
    self.assertEqual([], day_visit_finder_heap.GetPointsCalculatorList())

    a = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator())    
    day_visit_finder_heap.Append(a)
    self.assertEqual(1, day_visit_finder_heap.Size())
    self.assertRaises(AssertionError, day_visit_finder_heap.GetPointsCalculatorList)

    b = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator())
    day_visit_finder_heap.Append(b)
    self.assertEqual(2, day_visit_finder_heap.Size())
    self.assertRaises(AssertionError, day_visit_finder_heap.GetPointsCalculatorList)

    day_visit_finder_heap.Shrink()
    self.assertEqual(2, day_visit_finder_heap.Size())
    self.assertEqual([a, b], day_visit_finder_heap.GetPointsCalculatorList())
    
    c = PointsCalculator(MockPoints(2), MockDayVisitCostCalculator())
    day_visit_finder_heap.Append(c)
    self.assertEqual(3, day_visit_finder_heap.Size())
    self.assertRaises(AssertionError, day_visit_finder_heap.GetPointsCalculatorList)

    day_visit_finder_heap.Shrink()
    self.assertEqual(3, day_visit_finder_heap.Size())
    self.assertEqual([a, b, c], day_visit_finder_heap.GetPointsCalculatorList())
    
    d = PointsCalculator(MockPoints(3), MockDayVisitCostCalculator())
    self.assertRaises(AssertionError, day_visit_finder_heap.Append, d)
    self.assertEqual(3, day_visit_finder_heap.Size())
    self.assertEqual([a, b, c], day_visit_finder_heap.GetPointsCalculatorList())

    day_visit_finder_heap.Clear()
    self.assertEqual(0, day_visit_finder_heap.Size())
    self.assertEqual([], day_visit_finder_heap.GetPointsCalculatorList())
    

if __name__ == '__main__':
    unittest.main()
  