import os
import unittest

import Yusi
from Yusi.YuFinder import read_csv
from Yusi.YuFinder.cost_accumulator import SimpleCostAccumulatorGenerator, MoreWalkingCostAccumulatorGenerator
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.move_calculator import PTT_COST_MULT


class SimpleCostAccumulatorTest(unittest.TestCase):
  
  def testGeneral(self):
    points = read_csv.ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    cost_accumulator = SimpleCostAccumulatorGenerator().Generate()
    self.assertEqual(0., cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(1.25, city_visit.MoveType.walking))
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(points['Ferry Biulding'])
    self.assertEqual(2.25, cost_accumulator.Cost())
    cost_accumulator.AddLunch(0.5)
    self.assertEqual(2.75, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(0.05, city_visit.MoveType.driving))
    self.assertEqual(2.80, cost_accumulator.Cost())
    cost_accumulator.AddPointNoVisit(points['Pier 39'])
    self.assertEqual(5.80, cost_accumulator.Cost())


class MoreWalkingCostAccumulatorTest(unittest.TestCase):
  
  def testGeneral(self):
    points = read_csv.ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    cost_accumulator = MoreWalkingCostAccumulatorGenerator().Generate()
    self.assertEqual(0., cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(1.25, city_visit.MoveType.walking))
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(points['Ferry Biulding'])
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddLunch(0.5)
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(0.05, city_visit.MoveType.driving))
    self.assertEqual(1.25 + 0.05 * PTT_COST_MULT, cost_accumulator.Cost())
    cost_accumulator.AddPointNoVisit(points['Pier 39'])
    self.assertEqual(1.25 + 0.05 * PTT_COST_MULT, cost_accumulator.Cost())
    

if __name__ == '__main__':
    unittest.main()
