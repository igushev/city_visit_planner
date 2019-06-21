import unittest

from YuPoint import point as point_
from YuRanker import points_ranker as points_ranker_
from YuRanker import rank_adjuster_interface
from YuRanker import test_util


class MockPoint(point_.PointInterface):
  pass


class MockRankAdjuster(rank_adjuster_interface.RankAdjusterInterface):
  
  def __init__(self, test_obj, point_score_mults, score_points_expected,
               city_visit_parameters_expected, places=None):
    self.test_obj = test_obj
    self.point_score_mults = point_score_mults
    self.score_points_expected = score_points_expected
    self.city_visit_parameters_expected = city_visit_parameters_expected
    self.places = places
    
  def AdjustRank(self, score_points, city_visit_parameters):
    for ((score_expected, point_expected),
         (score, point)) in zip(self.score_points_expected,
                                score_points):
      self.test_obj.assertAlmostEqual(score_expected, score, places=self.places)
      self.test_obj.assertTrue(point is point_expected)
    self.test_obj.assertTrue(
        city_visit_parameters is self.city_visit_parameters_expected)
    assert len(self.point_score_mults) == len(score_points)
    return [rank_adjuster_interface.ScorePoint(point_score_mult * score, point)
            for point_score_mult, (score, point)
            in zip(self.point_score_mults, score_points)]
    

class PointsRankerTest(unittest.TestCase):
  
  def testGeneral(self):
    a = MockPoint()
    b = MockPoint()
    c = MockPoint()
    points_input = [a, b, c]
    city_visit_parameters = test_util.MockCityVisitParameters()
    points_ranker = points_ranker_.PointsRanker([
        MockRankAdjuster(
            self, [1.0, 0.9, 0.9],
            [rank_adjuster_interface.ScorePoint(100., a),
             rank_adjuster_interface.ScorePoint(100., b),
             rank_adjuster_interface.ScorePoint(100., c)],
            city_visit_parameters),
        MockRankAdjuster(
            self, [0.7, 0.9, 0.8],
            [rank_adjuster_interface.ScorePoint(100., a),
             rank_adjuster_interface.ScorePoint(90., b),
             rank_adjuster_interface.ScorePoint(90., c)],
            city_visit_parameters),
        MockRankAdjuster(
            self, [0.9, 0.9, 0.9],
            [rank_adjuster_interface.ScorePoint(70., a),
             rank_adjuster_interface.ScorePoint(81., b),
             rank_adjuster_interface.ScorePoint(72., c)],
            city_visit_parameters)])
    
    points_actual = points_ranker.RankPoints(points_input, city_visit_parameters)

    points_expected = [b, c, a]
    self.assertEqual(points_expected, points_actual)    

  def testNoPoints(self):
    points_input = []
    city_visit_parameters = test_util.MockCityVisitParameters()
    points_ranker = points_ranker_.PointsRanker([
        MockRankAdjuster(self, [], [], city_visit_parameters),
        MockRankAdjuster(self, [], [], city_visit_parameters),
        MockRankAdjuster(self, [], [], city_visit_parameters)])
    
    points_actual = points_ranker.RankPoints(
        points_input, city_visit_parameters)

    points_expected = points_input
    self.assertEqual(points_expected, points_actual)    

  def testNoRankAdjusters(self):
    a = MockPoint()
    b = MockPoint()
    c = MockPoint()
    points_input = [a, b, c]
    city_visit_parameters = test_util.MockCityVisitParameters()
    points_ranker = points_ranker_.PointsRanker([])
    
    points_actual = points_ranker.RankPoints(points_input, city_visit_parameters)

    points_expected = points_input
    self.assertEqual(points_expected, points_actual)    




if __name__ == '__main__':
    unittest.main()
