from Yusi.YuFinder.city_visit import PointVisit, MoveBetween, Lunch


class CityVisitCostCalculator(object):
  
  def __init__(self, cost_accumulator_generator):
    self.cost_accumulator_generator = cost_accumulator_generator
  
  def CalculateCityVisitCost(self, day_visits, points_left):
    cost_accumulator = self.cost_accumulator_generator.Generate()
    for day_visit in day_visits:
      for action in day_visit.actions:
        if isinstance(action, PointVisit):
          cost_accumulator.AddPointVisit(action.point)
        elif isinstance(action, MoveBetween):
          cost_accumulator.AddMoveBetween(action.move_description)
        elif isinstance(action, Lunch):
          cost_accumulator.AddLunch(action.lunch_hours)
        else:
          raise NotImplemented('Unknown action type %s' % type(action))
    for point_left in points_left:
      cost_accumulator.AddPointNoVisit(point_left)

    return cost_accumulator.Cost()
