import unittest

from Yusi.YuRanker.points_ranker import PointsRanker
from Yusi.YuRanker.rank_adjuster_interface import RankAdjusterInterface,\
  ScorePoint
from Yusi.YuRanker.test_utils import MockCityVisitParameters


class MockPoint(object):
  pass


class MockRankAdjuster(RankAdjusterInterface):
  
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
    return [ScorePoint(point_score_mult * score, point)
            for point_score_mult, (score, point)
            in zip(self.point_score_mults, score_points)]
    

class PointsRankerTest(unittest.TestCase):
  
  def testGeneral(self):
    a = MockPoint()
    b = MockPoint()
    c = MockPoint()
    points_input = [a, b, c]
    city_visit_parameters = MockCityVisitParameters()
    points_ranker = PointsRanker([
        MockRankAdjuster(
            self, [1.0, 0.9, 0.9],
            [ScorePoint(100., a), ScorePoint(100., b), ScorePoint(100., c)],
            city_visit_parameters),
        MockRankAdjuster(
            self, [0.7, 0.9, 0.8],
            [ScorePoint(100., a), ScorePoint(90., b), ScorePoint(90., c)],
            city_visit_parameters),
        MockRankAdjuster(
            self, [0.9, 0.9, 0.9],
            [ScorePoint(70., a), ScorePoint(81., b), ScorePoint(72., c)],
            city_visit_parameters)])
    
    points_actual = points_ranker.RankPoints(
        points_input, city_visit_parameters)

    points_expected = [b, c, a]
    self.assertEqual(points_expected, points_actual)    

  def testNoPoints(self):
    points_input = []
    city_visit_parameters = MockCityVisitParameters()
    points_ranker = PointsRanker([
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
    city_visit_parameters = MockCityVisitParameters()
    points_ranker = PointsRanker([])
    
    points_actual = points_ranker.RankPoints(
        points_input, city_visit_parameters)

    points_expected = points_input
    self.assertEqual(points_expected, points_actual)    




if __name__ == '__main__':
    unittest.main()
