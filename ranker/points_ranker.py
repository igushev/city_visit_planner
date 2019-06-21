from data import point as point_
from data import city_visit
from ranker import rank_adjuster_interface


class PointsRankerInterface(object):
  """Abstract class which ranks points."""

  def RankPoints(self, points, city_visit_parameters):
    """Rank given points by given city_visit_parameters."""
    raise NotImplemented()


class PointsRanker(PointsRankerInterface):
  """Ranks points by given RankAdjusters."""
  
  def __init__(self, rank_adjusters):
    for rank_adjuster in rank_adjusters:
      assert isinstance(rank_adjuster, rank_adjuster_interface.RankAdjusterInterface)

    self.rank_adjusters = rank_adjusters

  def RankPoints(self, points, city_visit_parameters):
    for point in points:
      isinstance(point, point_.PointInterface)
    assert isinstance(city_visit_parameters, city_visit.CityVisitParametersInterface)
    
    score_points = [rank_adjuster_interface.ScorePoint(100., point) for point in points]
    for rank_adjuster in self.rank_adjusters:
      score_points = rank_adjuster.AdjustRank(
          score_points, city_visit_parameters)
    score_points_sorted = sorted(
        score_points, key=lambda score_point: score_point.Score, reverse=True)
    return [point for _, point in score_points_sorted]
