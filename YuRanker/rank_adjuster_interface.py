class RankAdjusterInterface(object):
  """Abstract class which adjusts rank of points."""
  
  def AdjustRank(self):
    raise NotImplemented()