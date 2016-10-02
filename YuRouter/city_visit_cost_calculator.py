from Yusi.YuPoint.city_visit import PointVisit, MoveBetween, Lunch, CityVisit


class CityVisitCostCalculatorInterface(object):
  """Abstract class which constructs CityVisit and calculates its cost."""

  def AddPointsLeft(self, points_left):
    """Add points that cannot be visited to the cost of CityVisit."""
    raise NotImplemented()
  
  def Cost(self):
    """Get current cost of CityVisit."""
    raise NotImplemented()

  def CityVisit(self):
    """Construct CityVisit."""
    raise NotImplemented()

  def GetPointsLeft(self):
    """Get all points that cannot be visited."""
    raise NotImplemented()


class CityVisitCostCalculator(CityVisitCostCalculatorInterface):
  """Constructs CityVisit and calculates its cost."""
  
  def __init__(
      self, cost_accumulator_generator, day_visits, day_visit_parameterss):
    self.cost_accumulator = cost_accumulator_generator.Generate()
    self.day_visits = []
    self.day_visit_parameterss = day_visit_parameterss
    self.points_left = []
    self._AddDayVisits(day_visits)
  
  def _AddDayVisits(self, day_visits):
    for day_visit, day_visit_parameters in (
        zip(day_visits, self.day_visit_parameterss)):
      for action in day_visit.actions:
        if isinstance(action, PointVisit):
          self.cost_accumulator.AddPointVisit(action.point)
        elif isinstance(action, MoveBetween):
          self.cost_accumulator.AddMoveBetween(action.move_description)
        elif isinstance(action, Lunch):
          self.cost_accumulator.AddLunch(action.lunch_hours)
        else:
          raise NotImplemented('Unknown action type %s' % type(action))
      unused_time = (day_visit_parameters.end_datetime -
                     day_visit.actions[-1].start_end_datetime.end)
      self.cost_accumulator.AddUnusedTime(unused_time)
    self.day_visits.extend(day_visits)
        
  def AddPointsLeft(self, points_left):
    for point_left in points_left:
      self.cost_accumulator.AddPointLeft(point_left)
    self.points_left.extend(points_left)
  
  def Cost(self):
    return self.cost_accumulator.Cost()

  def CityVisit(self):
    return CityVisit(self.day_visits, self.cost_accumulator.Cost())

  def GetPointsLeft(self):
    return self.points_left


class CityVisitCostCalculatorGeneratorInterface(object):
  """Abstract class which returns every time new clean instance of
  CityVisitCostCalculatorInterface."""

  def Generate(self, day_visits):
    """Generate new clean instance of CityVisitCostCalculatorInterface."""
    raise NotImplemented()


class CityVisitCostCalculatorGenerator(
    CityVisitCostCalculatorGeneratorInterface):
  """Returns every time new clean instance of CityVisitCostCalculator."""

  def __init__(self, cost_accumulator_generator):
    self.cost_accumulator_generator = cost_accumulator_generator
  
  def Generate(self, day_visits, day_visit_parameterss):
    return CityVisitCostCalculator(
        self.cost_accumulator_generator, day_visits, day_visit_parameterss)
