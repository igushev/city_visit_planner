import os
import unittest

from YuPoint import read_csv
from YuRanker import popularity_rank_adjuster
from YuRanker import rank_adjuster_interface
from YuRanker import test_util


class PopularityRankAdjusterTest(test_util.RankAdjusterTestUtils):
  
  def setUp(self):
    self.points = read_csv.ReadCSVToDict(os.path.join('YuPoint', 'test_sf_1.csv'))
    self.popularity_rank_adjuster = popularity_rank_adjuster.PopularityRankAdjuster()
    super(PopularityRankAdjusterTest, self).setUp()
  
  def testGeneral(self):
    score_points_input = [
        rank_adjuster_interface.ScorePoint(100., self.points['Ferry Building']),
        rank_adjuster_interface.ScorePoint(100., self.points['Golden Gate Bridge']),
        rank_adjuster_interface.ScorePoint(100., self.points['Sutro Baths'])]
    
    score_points_actual = (
        self.popularity_rank_adjuster.AdjustRank(
            score_points_input, test_util.MockCityVisitParameters()))
    
    score_points_expected = [
        rank_adjuster_interface.ScorePoint(80., self.points['Ferry Building']),
        rank_adjuster_interface.ScorePoint(100., self.points['Golden Gate Bridge']),
        rank_adjuster_interface.ScorePoint(20., self.points['Sutro Baths'])]
    
    self.assertScorePointsEqual(score_points_expected, score_points_actual, places=3)
    

if __name__ == '__main__':
    unittest.main()
