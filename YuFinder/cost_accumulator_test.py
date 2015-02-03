import os
import unittest

import Yusi
from Yusi.YuFinder import read_csv, point
from Yusi.YuFinder.cost_accumulator import FactorCostAccumulatorGenerator
from Yusi.YuFinder import city_visit


class FactorCostAccumulatorTest(unittest.TestCase):

  def setUp(self):
    self.san_francisco_coordinates = point.Coordinates(37.7833, -122.4167)
    self.points = read_csv.ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    super(FactorCostAccumulatorTest, self).setUp()
    
  
  def testDefaults(self):
    cost_accumulator = FactorCostAccumulatorGenerator().Generate()
    self.assertEqual(0., cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(
            self.san_francisco_coordinates,
            self.points['Ferry Biulding'].coordinates_starts,
            1.25, city_visit.MoveType.walking))
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(self.points['Ferry Biulding'])
    self.assertEqual(2.25, cost_accumulator.Cost())
    cost_accumulator.AddLunch(1.0)
    self.assertEqual(3.25, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(
            self.points['Ferry Biulding'].coordinates_ends,
            self.points['Pier 39'].coordinates_starts,
            0.05, city_visit.MoveType.driving))
    self.assertEqual(3.30, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(self.points['Pier 39'])
    self.assertEqual(6.30, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(
            self.points['Pier 39'].coordinates_ends,
            self.san_francisco_coordinates,
            0.50, city_visit.MoveType.ptt))
    self.assertEqual(6.80, cost_accumulator.Cost())
    cost_accumulator.AddPointLeft(self.points['Golden Gate Bridge'])
    self.assertEqual(7.30, cost_accumulator.Cost())
  
  def testGeneral(self):
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
        city_visit.MoveDescription(
            self.san_francisco_coordinates,
            self.points['Ferry Biulding'].coordinates_starts,
            1.25, city_visit.MoveType.walking))
    self.assertEqual(1.25, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(self.points['Ferry Biulding'])
    self.assertEqual(1.75, cost_accumulator.Cost())
    cost_accumulator.AddLunch(1.0)
    self.assertEqual(2.00, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(
            self.points['Ferry Biulding'].coordinates_ends,
            self.points['Pier 39'].coordinates_starts,
            0.05, city_visit.MoveType.driving))
    self.assertEqual(2.10, cost_accumulator.Cost())
    cost_accumulator.AddPointVisit(self.points['Pier 39'])
    self.assertEqual(3.60, cost_accumulator.Cost())
    cost_accumulator.AddMoveBetween(
        city_visit.MoveDescription(
            self.points['Pier 39'].coordinates_ends,
            self.san_francisco_coordinates,
            0.50, city_visit.MoveType.ptt))
    self.assertEqual(5.10, cost_accumulator.Cost())
    cost_accumulator.AddPointLeft(self.points['Golden Gate Bridge'])
    self.assertEqual(110.10, cost_accumulator.Cost())
    

if __name__ == '__main__':
    unittest.main()
