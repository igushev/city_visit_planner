class DayVisitCostCalculatorInterface(object):
  """Abstract class which calculates cost of DayVisit."""

  def PushPoint(self, point):
    raise NotImplemented()

  def CanFinalize(self):
    raise NotImplemented()
  
  def FinalizedCost(self):
    raise NotImplemented()

  def FinalizedDayVisit(self):
    raise NotImplemented()


class DayVisitCostCalculatorGeneratorInterface(object):

  def Generate(self, day_visit_parameters):
    raise NotImplemented()
