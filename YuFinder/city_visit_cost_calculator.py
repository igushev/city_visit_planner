from Yusi.YuFinder.city_visit import PointVisit, MoveBetween, Lunch, CityVisit


class CityVisitCostCalculator(object):
  
  def __init__(self, cost_accumulator_generator, day_visits):
    self.cost_accumulator = cost_accumulator_generator.Generate()
    self.day_visits = []
    self.points_left = []
    self.AddDayVisits(day_visits)
  
  def AddDayVisits(self, day_visits):
    for day_visit in day_visits:
      for action in day_visit.actions:
        if isinstance(action, PointVisit):
          self.cost_accumulator.AddPointVisit(action.point)
        elif isinstance(action, MoveBetween):
          self.cost_accumulator.AddMoveBetween(action.move_description)
        elif isinstance(action, Lunch):
          self.cost_accumulator.AddLunch(action.lunch_hours)
        else:
          raise NotImplemented('Unknown action type %s' % type(action))
    self.day_visits.extend(day_visits)
        
  def AddPointsLeft(self, points_left):
    for point_left in points_left:
      self.cost_accumulator.AddPointNoVisit(point_left)
    self.points_left.extend(points_left)
  
  def Cost(self):
    return self.cost_accumulator.Cost()

  def CityVisit(self):
    return CityVisit(self.day_visits, self.cost_accumulator.Cost())

  def GetPointsLeft(self):
    return self.points_left


class CityVisitCostCalculatorGenerator(object):

  def __init__(self, cost_accumulator_generator):
    self.cost_accumulator_generator = cost_accumulator_generator
  
  def Generate(self, day_visits):
    return CityVisitCostCalculator(self.cost_accumulator_generator, day_visits)
