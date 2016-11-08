import os
import unittest

import Yusi
from Yusi.YuPoint.city_visit import CityVisitParameters
from Yusi.YuPoint.point import AgeGroup
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuRanker.age_group_rank_adjuster import AgeGroupRankAdjuster
from Yusi.YuRanker.rank_adjuster_interface import ScorePoint
from Yusi.YuRanker.test_utils import RankAdjusterTestUtils,\
  MockDayVisitParameters, MockPointType, MockVisitLocation


class AgeGroupRankAdjusterTest(RankAdjusterTestUtils):
  
  def setUp(self):
    self.points = ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
    self.age_group_rank_adjuster = AgeGroupRankAdjuster()
    super(AgeGroupRankAdjusterTest, self).setUp()
  
  def testGeneral(self):
    score_points_input = [
        ScorePoint(100., self.points['Ferry Building']),
        ScorePoint(100., self.points['Cable Car']),
        ScorePoint(100., self.points['Twin Peaks'])]

    parameters_age_groups = AgeGroup(
        senior=None,
        adult=90,
        junior=None,
        child=None,
        toddlers=10)

    city_visit_parameters = CityVisitParameters(
        MockVisitLocation(),
        day_visit_parameterss=[MockDayVisitParameters()],
        point_type=MockPointType(),
        age_group=parameters_age_groups)

    score_points_actual = (
        self.age_group_rank_adjuster.AdjustRank(
            score_points_input, city_visit_parameters))

    score_points_expected = [
        ScorePoint(16.62, self.points['Ferry Building']),
        ScorePoint(13.08, self.points['Cable Car']),
        ScorePoint(12.88, self.points['Twin Peaks'])]

    self.assertScorePointsEqual(
        score_points_expected, score_points_actual, places=3)


if __name__ == '__main__':
    unittest.main()
