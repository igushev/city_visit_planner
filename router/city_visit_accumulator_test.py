import unittest

from data import city_visit as city_visit_
from data import city_visit_test_utils
from router import cost_accumulator
from router import city_visit_points_left
from router import city_visit_accumulator as city_visit_accumulator_


class CityVisitAccumulatorTest(city_visit_test_utils.CityVisitTestExample):

  def setUp(self):
    self.no_point_visit_factor = 0.
    self.no_point_visit_const = 1000.
    self.unused_time_factor = 0.01
    cost_accumulator_generator=cost_accumulator.FactorCostAccumulatorGenerator(
        no_point_visit_factor=self.no_point_visit_factor,
        no_point_visit_const=self.no_point_visit_const,
        unused_time_factor=self.unused_time_factor)
    self.city_visit_points_left_generator = (
        city_visit_points_left.CityVisitPointsLeftGenerator(
            cost_accumulator_generator=cost_accumulator_generator))
    self.city_visit_accumulator_generator = city_visit_accumulator_.CityVisitAccumulatorGenerator()
    super(CityVisitAccumulatorTest, self).setUp()

  def testNoDayVisitsNoPointsLeft(self):
    city_visit_accumulator = self.city_visit_accumulator_generator.Generate()
    city_visit, points_left = (
        city_visit_accumulator.Result(
            self.city_visit_points_left_generator))
    self.assertEqual(city_visit_.CityVisit([], city_visit_.CityVisitSummary(0., 0.)), city_visit)
    self.assertEqual([], points_left)
    
  def testTwoDayVisitsTwoPointsLeftSeparateCalls(self):
    city_visit_accumulator = self.city_visit_accumulator_generator.Generate()
    city_visit_accumulator.AddDayVisits(
        [self.day_visit_1], [self.day_visit_parameters_1])
    city_visit_accumulator.AddDayVisits(
        [self.day_visit_2], [self.day_visit_parameters_2])
    city_visit_accumulator.AddPointsLeft([self.points['Union Square']])
    city_visit_accumulator.AddPointsLeft([self.points['Lombard Street']])
    city_visit, points_left = (
        city_visit_accumulator.Result(
            self.city_visit_points_left_generator))
    self.assertEqual(
        city_visit_.CityVisit([self.day_visit_1, self.day_visit_2],
                              city_visit_.CityVisitSummary(17.7 + 2 * self.no_point_visit_const, 0.)),
        city_visit)
    self.assertEqual([self.points['Union Square'],
                      self.points['Lombard Street']], points_left)
    
  def testTwoDayVisitsTwoPointsLeftOneCall(self):
    city_visit_accumulator = self.city_visit_accumulator_generator.Generate()
    city_visit_accumulator.AddDayVisits(
        [self.day_visit_1, self.day_visit_2],
        [self.day_visit_parameters_1, self.day_visit_parameters_2])
    city_visit_accumulator.AddPointsLeft(
        [self.points['Union Square'],self.points['Lombard Street']])
    city_visit, points_left = (
        city_visit_accumulator.Result(
            self.city_visit_points_left_generator))
    self.assertEqual(
        city_visit_.CityVisit([self.day_visit_1, self.day_visit_2],
                              city_visit_.CityVisitSummary(17.7 + 2 * self.no_point_visit_const, 0.)),
                              city_visit)
    self.assertEqual([self.points['Union Square'],
                      self.points['Lombard Street']], points_left)


if __name__ == '__main__':
    unittest.main()
