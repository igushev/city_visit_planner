class PointsRanker(object):
  
  def __init__(self, rank_adjusters):
    self.rank_adjusters = rank_adjusters
  
  def RankPoints(self, points):
    raise NotImplemented