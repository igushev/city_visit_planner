import os
import unittest

import Yusi
from Yusi.YuFinder import read_csv
from Yusi.YuFinder.cost_accumulator import FactorCostAccumulatorGenerator
from Yusi.YuFinder import city_visit


class FactorCostAccumulatorTest(unittest.TestCase):
  
  def testDefaults(self):
    points = read_csv.ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    cost_accumulator = FactorCostAccumulatorGenerator().Generate()
    self.assertEqual(0., cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(1.25, city_visit.MoveType.walking))
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(points['Ferry Biulding'])
    self.assertEqual(2.25, cost_accumulator.Cost())
    cost_accumulator.AddLunch(1.0)
    self.assertEqual(3.25, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(0.05, city_visit.MoveType.driving))
    self.assertEqual(3.30, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(points['Pier 39'])
    self.assertEqual(6.30, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(0.50, city_visit.MoveType.ptt))
    self.assertEqual(6.80, cost_accumulator.Cost())
    cost_accumulator.AddPointNoVisit(points['Golden Gate Bridge'])
    self.assertEqual(7.30, cost_accumulator.Cost())
  
  def testGeneral(self):
    points = read_csv.ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    cost_accumulator = FactorCostAccumulatorGenerator(
        point_visit_factor=0.5,
        move_walking_factor=1,
        move_driving_factor=2,
        move_ptt_factor=3,
        lunch_factor=0.25,
        no_point_visit_factor=10,
        no_point_visit_const=100).Generate()
    self.assertEqual(0., cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(1.25, city_visit.MoveType.walking))
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(points['Ferry Biulding'])
    self.assertEqual(1.75, cost_accumulator.Cost())
    cost_accumulator.AddLunch(1.0)
    self.assertEqual(2.00, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(0.05, city_visit.MoveType.driving))
    self.assertEqual(2.10, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(points['Pier 39'])
    self.assertEqual(3.60, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(0.50, city_visit.MoveType.ptt))
    self.assertEqual(5.10, cost_accumulator.Cost())
    cost_accumulator.AddPointNoVisit(points['Golden Gate Bridge'])
    self.assertEqual(110.10, cost_accumulator.Cost())
    

if __name__ == '__main__':
    unittest.main()
