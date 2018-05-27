import unittest

from YuPoint import city_visit
from YuPoint import city_visit_test_utils
from YuRouter import city_visit_points_left as city_visit_points_left_
from YuRouter import cost_accumulator


class CityVisitPointsLeftTest(city_visit_test_utils.CityVisitTestExample):

  def setUp(self):
    self.no_point_visit_factor = 0.
    self.no_point_visit_const = 1000.
    self.unused_time_factor = 0.01
    cost_accumulator_generator=cost_accumulator.FactorCostAccumulatorGenerator(
        no_point_visit_factor=self.no_point_visit_factor,
        no_point_visit_const=self.no_point_visit_const,
        unused_time_factor=self.unused_time_factor)
    self.city_visit_points_left_generator = (
        city_visit_points_left_.CityVisitPointsLeftGenerator(
            cost_accumulator_generator=cost_accumulator_generator))
    super(CityVisitPointsLeftTest, self).setUp()

  def testDayVisitsNoPointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate(
            [self.day_visit_1, self.day_visit_2],
            [self.day_visit_parameters_1, self.day_visit_parameters_2], []))
    self.assertEqual(city_visit.CityVisitSummary(17.7, 0.),
                     city_visit_points_left.city_visit.city_visit_summary)

  def testDayVisitsOnePointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate(
            [self.day_visit_1, self.day_visit_2],
            [self.day_visit_parameters_1, self.day_visit_parameters_2],
            [self.points['Union Square']]))
    self.assertEqual(city_visit.CityVisitSummary(17.7 + self.no_point_visit_const, 0.),
                     city_visit_points_left.city_visit.city_visit_summary)

  def testDayVisitsTwoPointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate(
            [self.day_visit_1, self.day_visit_2],
            [self.day_visit_parameters_1, self.day_visit_parameters_2],
            [self.points['Union Square'], self.points['Lombard Street']]))
    self.assertEqual(city_visit.CityVisitSummary(17.7 + 2 * self.no_point_visit_const, 0.),
                     city_visit_points_left.city_visit.city_visit_summary)

  def testDayVisitsFourPointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate(
            [self.day_visit_1, self.day_visit_2],
            [self.day_visit_parameters_1, self.day_visit_parameters_2],
            [self.points['Union Square'], self.points['Lombard Street'],
             self.points['Coit Tower'], self.points['Att Park']]))
    self.assertEqual(city_visit.CityVisitSummary(17.7 + 4 * self.no_point_visit_const, 0.),
                     city_visit_points_left.city_visit.city_visit_summary)

  def testNoDayVisitsNoPointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate([], [], []))
    self.assertEqual(city_visit.CityVisitSummary(0., 0.),
                     city_visit_points_left.city_visit.city_visit_summary)

  def testNoDayVisitsOnePointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate(
            [], [],
            [self.points['Union Square']]))
    self.assertEqual(city_visit.CityVisitSummary(self.no_point_visit_const, 0.),
                     city_visit_points_left.city_visit.city_visit_summary)

  def testNoDayVisitsTwoPointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate(
            [], [],
            [self.points['Union Square'], self.points['Lombard Street']]))
    self.assertEqual(city_visit.CityVisitSummary(2 * self.no_point_visit_const, 0.),
                     city_visit_points_left.city_visit.city_visit_summary)

  def testNoDayVisitsFourPointsLeft(self):
    city_visit_points_left = (
        self.city_visit_points_left_generator.Generate(
            [], [],
            [self.points['Union Square'], self.points['Lombard Street'],
             self.points['Coit Tower'], self.points['Att Park']]))
    self.assertEqual(city_visit.CityVisitSummary(4 * self.no_point_visit_const, 0.),
                     city_visit_points_left.city_visit.city_visit_summary)
    

if __name__ == '__main__':
    unittest.main()
  