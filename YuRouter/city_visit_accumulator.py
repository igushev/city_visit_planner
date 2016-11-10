class CityVisitAccumulatorInterface(object):
  """Abstract class which accumulates results for CityVisit object."""
  
  def AddDayVisits(self, day_visits):
    """Add DayVisit objects."""
    raise NotImplemented()
  
  def AddPointsLeft(self, points_left):
    """Add points which couldn't be visited."""
    raise NotImplemented()
  
  def Result(self, cost_accumulator_generator):
    """Returns tuple of CityVisit and points_left."""
    raise NotImplemented()


class CityVisitAccumulatorGeneratorInterface(object):
  """Abstract class which returns every time new clean instance of
  CityVisitAccumulatorInterface."""

  def Generate(self):
    """Generate new clean instance of CityVisitAccumulatorInterface."""
    raise NotImplemented()


class CityVisitAccumulator(CityVisitAccumulatorInterface):
  """Accumulates CityVisit and points left.""" 

  def __init__(self):
    self.day_visits = []
    self.day_visit_parameterss = []
    self.points_left = []

  def AddDayVisits(self, day_visits, day_visit_parameterss):
    assert len(day_visits) == len(day_visit_parameterss)
    self.day_visits.extend(day_visits)
    self.day_visit_parameterss.extend(day_visit_parameterss)
  
  def AddPointsLeft(self, points_left):
    self.points_left.extend(points_left)
  
  def Result(self, city_visit_points_left_generator):
    city_visit_points_left = (
        city_visit_points_left_generator.Generate(
            self.day_visits, self.day_visit_parameterss, self.points_left))
    return (city_visit_points_left.city_visit,
            city_visit_points_left.points_left)


class CityVisitAccumulatorGenerator(CityVisitAccumulatorGeneratorInterface):
  """Returns every time new clean instance of CityVisitAccumulator."""

  def Generate(self):
    return CityVisitAccumulator()
