from data import city_visit
from ranker import rank_adjuster_interface


class PopularityRankAdjuster(rank_adjuster_interface.RankAdjusterInterface):
  """Adjusts rank of points by popularity."""

  def AdjustRank(self, score_points, city_visit_parameters):
    for score_point in score_points:
      assert isinstance(score_point, rank_adjuster_interface.ScorePoint)
    assert isinstance(city_visit_parameters, city_visit.CityVisitParametersInterface)
    
    return [rank_adjuster_interface.ScorePoint(score * point.popularity / float(100), point)
            for score, point in score_points]
