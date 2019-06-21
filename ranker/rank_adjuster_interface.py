from collections import namedtuple


ScorePoint = namedtuple('ScorePoint', 'Score Point')


class RankAdjusterInterface(object):
  """Abstract class which adjusts rank of points."""
  
  def AdjustRank(self, score_points, city_visit_parameters):
    """Adjusts scores of points."""
    raise NotImplemented()
