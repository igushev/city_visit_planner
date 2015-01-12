import copy
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.point import Point
from Yusi.YuFinder.move_calculator import PTT_COST_MULT


SIMPLE_POINT_NO_VISIT_COST = 1000


# TODO(igushev): Do we need to add lunch time to cost?
class CostAccumulatorInterface(object):
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

  def AddPointNoVisit(self, point):
    raise NotImplemented()


class CostAccumulatorGeneratorInterface(object):
  
  def Generate(self):
    raise NotImplemented()


class SimpleCostAccumulator(CostAccumulatorInterface):
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

  def AddPointNoVisit(self, point):
    assert isinstance(point, Point)
    self.cost += SIMPLE_POINT_NO_VISIT_COST


class SimpleCostAccumulatorGenerator(CostAccumulatorGeneratorInterface):
  
  def Generate(self):
    return SimpleCostAccumulator()


class MoreWalkingCostAccumulator(CostAccumulatorInterface):
  """Accumulates time but penalize driving."""
  
  def AddPointVisit(self, point):
    pass

  def AddMoveBetween(self, move_description):
    assert isinstance(move_description, city_visit.MoveDescription)
    if move_description.move_type == city_visit.MoveType.walking:
      mult = 1
    elif move_description.move_type == city_visit.MoveType.driving:
      mult = PTT_COST_MULT
    elif move_description.move_type == city_visit.MoveType.ptt:
      mult = PTT_COST_MULT
    else:
      raise NotImplemented('Unknown MoveType: %s' % move_description.move_type)
    self.cost += move_description.move_hours * mult

  def AddLunch(self, lunch_hour):
    pass

  def AddPointNoVisit(self, point):
    self.cost += SIMPLE_POINT_NO_VISIT_COST


class MoreWalkingCostAccumulatorGenerator(CostAccumulatorGeneratorInterface):

  def Generate(self):
    return MoreWalkingCostAccumulator()
