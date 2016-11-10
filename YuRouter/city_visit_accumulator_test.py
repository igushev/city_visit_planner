import unittest


from Yusi.YuPoint.city_visit_test_utils import CityVisitTestExample
from Yusi.YuRouter.cost_accumulator import FactorCostAccumulatorGenerator
from Yusi.YuRouter.city_visit_points_left import CityVisitPointsLeftGenerator
from Yusi.YuRouter.city_visit_accumulator import CityVisitAccumulatorGenerator
from Yusi.YuPoint.city_visit import CityVisit, CityVisitSummary


class CityVisitAccumulatorTest(CityVisitTestExample):

  def setUp(self):
    self.no_point_visit_factor = 0.
    self.no_point_visit_const = 1000.
    self.unused_time_factor = 0.01
    cost_accumulator_generator=FactorCostAccumulatorGenerator(
        no_point_visit_factor=self.no_point_visit_factor,
        no_point_visit_const=self.no_point_visit_const,
        unused_time_factor=self.unused_time_factor)
    self.city_visit_points_left_generator = (
        CityVisitPointsLeftGenerator(
            cost_accumulator_generator=cost_accumulator_generator))
    self.city_visit_accumulator_generator = CityVisitAccumulatorGenerator()
    super(CityVisitAccumulatorTest, self).setUp()

  def testNoDayVisitsNoPointsLeft(self):
    city_visit_accumulator = self.city_visit_accumulator_generator.Generate()
    city_visit, points_left = (
        city_visit_accumulator.Result(
            self.city_visit_points_left_generator))
    self.assertEqual(CityVisit([], CityVisitSummary(0., 0.)), city_visit)
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
        CityVisit([self.day_visit_1, self.day_visit_2],
                  CityVisitSummary(17.7 + 2 * self.no_point_visit_const, 0.)),
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
        CityVisit([self.day_visit_1, self.day_visit_2],
                  CityVisitSummary(17.7 + 2 * self.no_point_visit_const, 0.)),
                     city_visit)
    self.assertEqual([self.points['Union Square'],
                      self.points['Lombard Street']], points_left)


if __name__ == '__main__':
    unittest.main()
