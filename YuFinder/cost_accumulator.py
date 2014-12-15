import copy
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.point import Point
from Yusi.YuFinder.move_calculator import DRIVING_COST_MULT


# TODO(igushev): Do we need to add lunch time to cost?
class CostAccumulator(object):
  """Abstract class which accumulates cost for a day."""

  def __init__(self):
    self.cost = 0

  def Cost(self):
    return self.cost
  
  def Copy(self):
    return copy.deepcopy(self)

  def AddPointVisit(self, point):
    raise NotImplemented()

  def AddMoveBetween(self, move_description):
    raise NotImplemented()

  def AddLunch(self, lunch_hour):
    raise NotImplemented()


class CostAccumulatorGenerator(object):
  
  def Generate(self):
    raise NotImplemented()


class SimpleCostAccumulator(CostAccumulator):
  """Accumulates time spent for each action."""
  
  def AddPointVisit(self, point):
    assert isinstance(point, Point)
    self.cost += point.duration

  def AddMoveBetween(self, move_description):
    assert isinstance(move_description, city_visit.MoveDescription)
    self.cost += move_description.move_hours

  def AddLunch(self, lunch_hour):
    assert isinstance(lunch_hour, float)
    self.cost += lunch_hour


class SimpleCostAccumulatorGenerator(CostAccumulatorGenerator):
  
  def Generate(self):
    return SimpleCostAccumulator()


class SmartCostAccumulator(CostAccumulator):
  """Accumulates time but penalize driving."""
  
  def AddPointVisit(self, point):
    pass

  def AddMoveBetween(self, move_description):
    assert isinstance(move_description, city_visit.MoveDescription)
    if move_description.move_type == city_visit.MoveType.walking:
      mult = 1
    elif move_description.move_type == city_visit.MoveType.driving:
      mult = DRIVING_COST_MULT
    else:
      raise NotImplemented('Unknown MoveType: %s' % move_description.move_type)
    self.cost += move_description.move_hours * mult

  def AddLunch(self, lunch_hour):
    pass


class SmartCostAccumulatorGenerator(CostAccumulatorGenerator):

  def Generate(self):
    return SmartCostAccumulator()
