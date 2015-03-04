from Yusi.YuRanker.rank_adjuster_interface import ScorePoint,\
  RankAdjusterInterface


class PointsRankerInterface(object):
  """Abstract class which ranks points."""

  def RankPoints(self, points, city_visit_parameters):
    """Rank given points by given city_visit_parameters."""
    raise NotImplemented()


class PointsRanker(PointsRankerInterface):
  
  def __init__(self, rank_adjusters):
    for rank_adjuster in rank_adjusters:
      assert isinstance(rank_adjuster, RankAdjusterInterface)
    self.rank_adjusters = rank_adjusters

  def RankPoints(self, points, city_visit_parameters):
    score_points = [ScorePoint(100., point) for point in points]
    for rank_adjuster in self.rank_adjusters:
      score_points = rank_adjuster.AdjustRank(
          score_points, city_visit_parameters)
    score_points_sorted = sorted(
        score_points, key=lambda score_point: score_point.Score, reverse=True)
    return [point for _, point in score_points_sorted]
