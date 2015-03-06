class DayVisitCostCalculatorInterface(object):
  """Abstract class which constructs DayVisit and calculates its cost.
  
  If at Point cannot be fit into DayVisit, Calculator stops accepting new points
  (even if a Point can be fit) and just collects to left points. 
  """

  def Copy(self):
    raise NotImplemented()

  def PushPoint(self, point):
    """Try to push a new point to the DayVisit."""
    raise NotImplemented()

  def FinalizedCost(self):
    """DayVisit cost including returning to end coordinates."""
    raise NotImplemented()

  def FinalizedDayVisit(self):
    """DayVisit including returning to end coordinates."""
    raise NotImplemented()

  def GetPointsLeft(self):
    """Get points which cannot be fit into DayVisit."""
    raise NotImplemented()


class DayVisitCostCalculatorGeneratorInterface(object):
  """Abstract class which returns every time new clean instance of
  DayVisitCostCalculatorInterface."""

  def Generate(self, day_visit_parameters):
    """Generate new clean instance of DayVisitCostCalculatorInterface."""
    raise NotImplemented()
