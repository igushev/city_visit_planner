import unittest

import Yusi
from Yusi.YuFinder.day_visit_finder_heap import EverythingDayVisitFinderHeapGenerator,\
  PointsCalculator
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface


class MockPoints(object):
  pass


class MockDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  pass


class EverythingDayVisitFinderHeapTest(unittest.TestCase):
  
  def testGeneral(self):
    day_visit_finder_heap = EverythingDayVisitFinderHeapGenerator().Generate()
    self.assertEqual(0, day_visit_finder_heap.Size())
    self.assertEqual([], day_visit_finder_heap.GetPointsCalculatorList())

    a = PointsCalculator(MockPoints(), MockDayVisitCostCalculator())    
    day_visit_finder_heap.Append(a)
    self.assertEqual(1, day_visit_finder_heap.Size())
    self.assertRaises(day_visit_finder_heap.GetPointsCalculatorList)

    b = PointsCalculator(MockPoints(), MockDayVisitCostCalculator())
    day_visit_finder_heap.Append(b)
    self.assertEqual(2, day_visit_finder_heap.Size())
    self.assertRaises(day_visit_finder_heap.GetPointsCalculatorList)

    day_visit_finder_heap.Shrink()
    self.assertEqual(2, day_visit_finder_heap.Size())
    self.assertEqual([a, b], day_visit_finder_heap.GetPointsCalculatorList())
    
    c = PointsCalculator(MockPoints(), MockDayVisitCostCalculator())
    day_visit_finder_heap.Append(c)
    self.assertEqual(3, day_visit_finder_heap.Size())
    self.assertRaises(day_visit_finder_heap.GetPointsCalculatorList)

    day_visit_finder_heap.Shrink()
    self.assertEqual(3, day_visit_finder_heap.Size())
    self.assertEqual([a, b, c], day_visit_finder_heap.GetPointsCalculatorList())

    day_visit_finder_heap.Clear()
    self.assertEqual(0, day_visit_finder_heap.Size())
    self.assertEqual([], day_visit_finder_heap.GetPointsCalculatorList())
    

if __name__ == '__main__':
    unittest.main()
  