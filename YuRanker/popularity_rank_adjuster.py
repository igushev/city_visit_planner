from Yusi.YuRanker.rank_adjuster_interface import RankAdjusterInterface,\
  ScorePoint


class PopularityRankAdjuster(RankAdjusterInterface):
  """Adjusts rank of points by popularity."""

  def AdjustRank(self, score_points, city_visit_parameters):
    return [ScorePoint(score * point.popularity / float(100), point)
            for score, point in score_points]
