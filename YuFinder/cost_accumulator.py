import copy

from Yusi.YuFinder.point import Point
from Yusi.YuFinder.city_visit import MoveDescription, MoveType


# TODO(igushev): Do we need to add lunch time to cost?
class CostAccumulatorInterface(object):
  """Abstract class which accumulates cost for a day."""

  def __init__(self):
    self.cost = 0

  def Copy(self):
    return copy.deepcopy(self)

  def Cost(self):
    return self.cost
  
  def AddPointVisit(self, point):
    raise NotImplemented()

  def AddMoveBetween(self, move_description):
    raise NotImplemented()

  def AddLunch(self, lunch_hour):
    raise NotImplemented()

  def AddPointLeft(self, point):
    raise NotImplemented()


class CostAccumulatorGeneratorInterface(object):
  
  def Generate(self):
    raise NotImplemented()


class FactorCostAccumulator(CostAccumulatorInterface):
  """Accumulates time spent for each action multiplied by a factor."""
  
  def __init__(self,
               point_visit_factor=1,
               move_walking_factor=1,
               move_driving_factor=1,
               move_ptt_factor=1,
               lunch_factor=1,
               no_point_visit_factor=1,
               no_point_visit_const=0):
    self._point_visit_factor = point_visit_factor
    self._move_walking_factor = move_walking_factor
    self._move_driving_factor = move_driving_factor
    self._move_ptt_factor = move_ptt_factor
    self._lunch_factor = lunch_factor
    self._no_point_visit_factor = no_point_visit_factor
    self._no_point_visit_const = no_point_visit_const
    super(FactorCostAccumulator, self).__init__()

  def AddPointVisit(self, point):
    assert isinstance(point, Point)
    self.cost += point.duration * self._point_visit_factor

  def AddMoveBetween(self, move_description):
    assert isinstance(move_description, MoveDescription)
    if move_description.move_type == MoveType.walking:
      factor = self._move_walking_factor
    elif move_description.move_type == MoveType.driving:
      factor = self._move_driving_factor
    elif move_description.move_type == MoveType.ptt:
      factor = self._move_ptt_factor
    else:
      raise NotImplemented('Unknown MoveType: %s' % move_description.move_type)
    self.cost += move_description.move_hours * factor

  def AddLunch(self, lunch_hour):
    assert isinstance(lunch_hour, float)
    self.cost += lunch_hour * self._lunch_factor

  def AddPointLeft(self, point):
    assert isinstance(point, Point)
    self.cost += (point.duration * self._no_point_visit_factor +
                  self._no_point_visit_const)


class FactorCostAccumulatorGenerator(CostAccumulatorGeneratorInterface):
  
  def __init__(self,
               point_visit_factor=1,
               move_walking_factor=1,
               move_driving_factor=1,
               move_ptt_factor=1,
               lunch_factor=1,
               no_point_visit_factor=1,
               no_point_visit_const=0):
    self._point_visit_factor = point_visit_factor
    self._move_walking_factor = move_walking_factor
    self._move_driving_factor = move_driving_factor
    self._move_ptt_factor = move_ptt_factor
    self._lunch_factor = lunch_factor
    self._no_point_visit_factor = no_point_visit_factor
    self._no_point_visit_const = no_point_visit_const

  def Generate(self):
    return FactorCostAccumulator(
        point_visit_factor=self._point_visit_factor,
        move_walking_factor=self._move_walking_factor,
        move_driving_factor=self._move_driving_factor,
        move_ptt_factor=self._move_ptt_factor,
        lunch_factor=self._lunch_factor,
        no_point_visit_factor=self._no_point_visit_factor,
        no_point_visit_const=self._no_point_visit_const)
