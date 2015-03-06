from Yusi.YuRanker.rank_adjuster_interface import RankAdjusterInterface,\
  ScorePoint
from Yusi.YuPoint.city_visit import CityVisitParametersInterface


class PopularityRankAdjuster(RankAdjusterInterface):
  """Adjusts rank of points by popularity."""

  def AdjustRank(self, score_points, city_visit_parameters):
    for score_point in score_points:
      assert isinstance(score_point, ScorePoint)
    assert isinstance(city_visit_parameters, CityVisitParametersInterface)
    
    return [ScorePoint(score * point.popularity / float(100), point)
            for score, point in score_points]
