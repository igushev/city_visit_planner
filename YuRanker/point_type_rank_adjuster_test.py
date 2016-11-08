import os
import unittest

import Yusi
from Yusi.YuPoint.city_visit import CityVisitParameters
from Yusi.YuPoint.point import PointType
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuRanker.point_type_rank_adjuster import PointTypeRankAdjuster
from Yusi.YuRanker.rank_adjuster_interface import ScorePoint
from Yusi.YuRanker.test_utils import RankAdjusterTestUtils,\
  MockDayVisitParameters, MockAgeGroup, MockVisitLocation


class PointTypeRankAdjusterTest(RankAdjusterTestUtils):
  
  def setUp(self):
    self.points = ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
    self.point_type_rank_adjuster = PointTypeRankAdjuster()
    super(PointTypeRankAdjusterTest, self).setUp()
  
  def testGeneral(self):
    score_points_input = [
        ScorePoint(100., self.points['Pier 39']),
        ScorePoint(100., self.points['Golden Gate Bridge']),
        ScorePoint(100., self.points['Sutro Baths'])]

    parameters_point_types = PointType(
        city_tours=90,
        landmarks=90,
        nature=10,
        museums=10,
        shopping=50,
        dining=50)

    city_visit_parameters = CityVisitParameters(
        MockVisitLocation(),
        day_visit_parameterss=[MockDayVisitParameters()],
        point_type=parameters_point_types,
        age_group=MockAgeGroup())

    score_points_actual = (
        self.point_type_rank_adjuster.AdjustRank(
            score_points_input, city_visit_parameters))

    score_points_expected = [
        ScorePoint(22.683, self.points['Pier 39']),
        ScorePoint(22.7, self.points['Golden Gate Bridge']),
        ScorePoint(9.15, self.points['Sutro Baths'])]

    self.assertScorePointsEqual(
        score_points_expected, score_points_actual, places=3)


if __name__ == '__main__':
    unittest.main()
