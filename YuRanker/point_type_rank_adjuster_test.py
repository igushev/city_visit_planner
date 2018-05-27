import os
import unittest

from YuPoint import city_visit
from YuPoint import point
from YuPoint import read_csv
from YuRanker import point_type_rank_adjuster
from YuRanker import rank_adjuster_interface
from YuRanker import test_utils


class PointTypeRankAdjusterTest(test_utils.RankAdjusterTestUtils):
  
  def setUp(self):
    self.points = read_csv.ReadCSVToDict(os.path.join('YuPoint', 'test_sf_1.csv'))
    self.point_type_rank_adjuster = point_type_rank_adjuster.PointTypeRankAdjuster()
    super(PointTypeRankAdjusterTest, self).setUp()
  
  def testGeneral(self):
    score_points_input = [
        rank_adjuster_interface.ScorePoint(100., self.points['Pier 39']),
        rank_adjuster_interface.ScorePoint(100., self.points['Golden Gate Bridge']),
        rank_adjuster_interface.ScorePoint(100., self.points['Sutro Baths'])]

    parameters_point_types = point.PointType(
        city_tours=90,
        landmarks=90,
        nature=10,
        museums=10,
        shopping=50,
        dining=50)

    city_visit_parameters = city_visit.CityVisitParameters(
        test_utils.MockVisitLocation(),
        day_visit_parameterss=[test_utils.MockDayVisitParameters()],
        point_type=parameters_point_types,
        age_group=test_utils.MockAgeGroup())

    score_points_actual = (
        self.point_type_rank_adjuster.AdjustRank(
            score_points_input, city_visit_parameters))

    score_points_expected = [
        rank_adjuster_interface.ScorePoint(22.683, self.points['Pier 39']),
        rank_adjuster_interface.ScorePoint(22.7, self.points['Golden Gate Bridge']),
        rank_adjuster_interface.ScorePoint(9.15, self.points['Sutro Baths'])]

    self.assertScorePointsEqual(
        score_points_expected, score_points_actual, places=3)


if __name__ == '__main__':
    unittest.main()
