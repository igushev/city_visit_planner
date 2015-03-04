import os
import unittest

import Yusi
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuRanker.popularity_rank_adjuster import PopularityRankAdjuster
from Yusi.YuRanker.rank_adjuster_interface import ScorePoint
from Yusi.YuRanker.test_utils import RankAdjusterTestUtils,\
  MockCityVisitParameters


class PopularityRankAdjusterTest(RankAdjusterTestUtils):
  
  def setUp(self):
    self.points = ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
    self.popularity_rank_adjuster = PopularityRankAdjuster()
    super(PopularityRankAdjusterTest, self).setUp()
  
  def testGeneral(self):
    score_points_input = [
        ScorePoint(100., self.points['Ferry Building']),
        ScorePoint(100., self.points['Golden Gate Bridge']),
        ScorePoint(100., self.points['Sutro Baths'])]
    
    score_points_actual = (
        self.popularity_rank_adjuster.AdjustRank(
            score_points_input, MockCityVisitParameters))
    
    score_points_expected = [
        ScorePoint(80., self.points['Ferry Building']),
        ScorePoint(100., self.points['Golden Gate Bridge']),
        ScorePoint(20., self.points['Sutro Baths'])]
    
    self.assertScorePointsEqual(
        score_points_expected, score_points_actual, places=3)
    

if __name__ == '__main__':
    unittest.main()
