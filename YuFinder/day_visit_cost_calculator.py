import copy
import datetime

from Yusi.YuFinder import city_visit
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface,\
  DayVisitCostCalculatorGeneratorInterface


class DayVisitCostCalculatorState(object):
  def __init__(self, current_datetime, current_coordinates, cost_accumulator,
               actions):
    self.current_datetime = current_datetime
    self.current_coordinates = current_coordinates
    self.cost_accumulator = cost_accumulator
    self.actions = actions
  
  @classmethod
  def Init(cls, day_visit_parameters, cost_accumulator_generator):
    return cls(
        day_visit_parameters.start_datetime,
        day_visit_parameters.start_coordinates,
        cost_accumulator_generator.Generate(),
        [])
    
  def Copy(self):
    return self.__class__(
        copy.deepcopy(self.current_datetime),
        self.current_coordinates.Copy(),
        self.cost_accumulator.Copy(),
        self.actions[:])


class ActionAdderInterface(object):
  
  def StartEndDatetime(self, current_state):
    raise NotImplemented
  
  def Add(self, current_state):
    raise NotImplemented


class PointVisitAdder(ActionAdderInterface):
  
  def __init__(self, calculator, point):
    self.calculator = calculator
    self.point = point
  
  def StartEndDatetime(self, current_state):
    visit_timedelta = datetime.timedelta(hours=self.point.duration)
    visit_start_end_datetime = city_visit.StartEndDatetime(
        current_state.current_datetime,
        current_state.current_datetime + visit_timedelta)
    return visit_start_end_datetime
  
  def Add(self, current_state):
    visit_start_end_datetime = self.StartEndDatetime(current_state)
    if not self.calculator.point_fit.IfPointFit(
        visit_start_end_datetime, self.point.operating_hours):
      return False
    if (visit_start_end_datetime.end >
        self.calculator.day_visit_parameters.end_datetime):
      return False
    current_state.current_datetime = visit_start_end_datetime.end
    current_state.current_coordinates = self.point.coordinates_ends
    current_state.cost_accumulator.AddPointVisit(self.point)
    current_state.actions.append(
        city_visit.PointVisit(visit_start_end_datetime, self.point))
    return True


class MoveBetweenAdder(ActionAdderInterface):

  def __init__(self, calculator, to_coordinates):
    self.calculator = calculator
    self.to_coordinates = to_coordinates

  def StartEndDatetime(self, current_state):
    move_description = (
        self.calculator.move_calculator.CalculateMoveDescription(
            current_state.current_coordinates, self.to_coordinates))
    move_timedelta = datetime.timedelta(hours=move_description.move_hours)
    move_start_end_datetime = city_visit.StartEndDatetime(
        current_state.current_datetime,
        current_state.current_datetime + move_timedelta)
    return move_start_end_datetime

  def Add(self, current_state):
    move_description = (
        self.calculator.move_calculator.CalculateMoveDescription(
            current_state.current_coordinates, self.to_coordinates))
    move_timedelta = datetime.timedelta(hours=move_description.move_hours)
    move_start_end_datetime = city_visit.StartEndDatetime(
        current_state.current_datetime,
        current_state.current_datetime + move_timedelta)
    if (move_start_end_datetime.end >
        self.calculator.day_visit_parameters.end_datetime):
      return False
    current_state.current_datetime = move_start_end_datetime.end
    current_state.current_coordinates = move_description.to_coordinates
    current_state.cost_accumulator.AddMoveBetween(move_description)
    current_state.actions.append(
      city_visit.MoveBetween(move_start_end_datetime, move_description))
    return True


class LunchAdder(ActionAdderInterface):

  def __init__(self, calculator):
    self.calculator = calculator

  def StartEndDatetime(self, current_state):
    lunch_timedelta = datetime.timedelta(
        hours=self.calculator.day_visit_parameters.lunch_hours)
    lunch_start_end_datetime = city_visit.StartEndDatetime(
        current_state.current_datetime,
        current_state.current_datetime + lunch_timedelta)
    return lunch_start_end_datetime
  
  def Add(self, current_state):
    lunch_start_end_datetime = self.StartEndDatetime(current_state)
    if (lunch_start_end_datetime.end >
        self.calculator.day_visit_parameters.end_datetime):
      return False
    current_state.current_datetime = lunch_start_end_datetime.end
    current_state.cost_accumulator.AddLunch(
        self.calculator.day_visit_parameters.lunch_hours)
    current_state.actions.append(
        city_visit.Lunch(
            lunch_start_end_datetime,
            self.calculator.day_visit_parameters.lunch_hours))
    return True


# NOTE(igushev): PushPoint responsible for checking point itself, move to this
# point and if day visit can be finalized. After first such point can't be
# pushed, none of following will be pushed, since higher level modules should
# be responsible for permutation.
class DayVisitCostCalculator(DayVisitCostCalculatorInterface):
  """Calculates cost of DayVisit."""

  def __init__(self, move_calculator, point_fit, day_visit_parameters,
               current_state, points_left):
    self.move_calculator = move_calculator
    self.point_fit = point_fit
    self.day_visit_parameters = day_visit_parameters
    self.current_state = current_state
    self.points_left = points_left

  @classmethod
  def Init(cls, move_calculator, point_fit, day_visit_parameters,
               cost_accumulator_generator):
    return cls(
       move_calculator,
       point_fit,
       day_visit_parameters,
       DayVisitCostCalculatorState.Init(
           day_visit_parameters, cost_accumulator_generator),
       [])

  def Copy(self):
    return self.__class__(
        self.move_calculator,
        self.point_fit,
        self.day_visit_parameters,
        self.current_state.Copy(),
        self.points_left[:])

  def _AddActionAndLunch(self, action_adder, current_state):
    action_start_end_datetime = action_adder.StartEndDatetime(current_state)
    if action_start_end_datetime.Fit(
        self.day_visit_parameters.lunch_start_datetime):
      # We have lunch during action and should add it.
      gap_between_start_and_lunch = (
          self.day_visit_parameters.lunch_start_datetime -
          action_start_end_datetime.start)
      gap_between_lunch_and_end = (
          action_start_end_datetime.end - 
          self.day_visit_parameters.lunch_start_datetime)
      lunch_adder = LunchAdder(self)
      if gap_between_start_and_lunch > gap_between_lunch_and_end:
        # It's better to have lunch after action.
        if not action_adder.Add(current_state):
          return False
        if not lunch_adder.Add(current_state):
          return False
      else:
        # It's better to have lunch before action.
        if not lunch_adder.Add(current_state):
          return False
        if not action_adder.Add(current_state):
          return False
      return True
    else:
      # We don't have lunch during action. Just add action.
      return action_adder.Add(current_state)

  def _CanPushPoint(self, point, current_state):
    move_between_adder = MoveBetweenAdder(self, point.coordinates_starts)
    if not self._AddActionAndLunch(move_between_adder, current_state):
      return False
    point_visit_adder = PointVisitAdder(self, point)
    if not self._AddActionAndLunch(point_visit_adder, current_state):
      return False
    finalized_current_state = current_state.Copy()
    finalize_action_adder = (
        MoveBetweenAdder(self, self.day_visit_parameters.end_coordinates))
    if not self._AddActionAndLunch(
        finalize_action_adder, finalized_current_state):
      return False
    return True
  
  def PushPoint(self, point):
    # If self.points_left is empty, it means no point has not been pushed, so
    # we can proceed.
    if not self.points_left:
      current_state = self.current_state.Copy()
      can_push = self._CanPushPoint(point, current_state)
    else:
      can_push = False
    
    if can_push:
      self.current_state = current_state
      return True
    else:
      self.current_state.cost_accumulator.AddPointLeft(point)
      self.points_left.append(point)
      return False

  def FinalizedCost(self):
    finalized_current_state = self.current_state.Copy()
    finalize_action_adder = (
        MoveBetweenAdder(self, self.day_visit_parameters.end_coordinates))
    assert self._AddActionAndLunch(
        finalize_action_adder, finalized_current_state), (
            'Finalizing Move must be able to be added.')
    return finalized_current_state.cost_accumulator.Cost()

  def FinalizedDayVisit(self):
    finalized_current_state = self.current_state.Copy()
    finalize_action_adder = (
        MoveBetweenAdder(self, self.day_visit_parameters.end_coordinates))
    assert self._AddActionAndLunch(
        finalize_action_adder, finalized_current_state), (
            'Finalizing Move must be able to be added.')
    return city_visit.DayVisit(
        self.day_visit_parameters.start_datetime,
        finalized_current_state.actions,
        finalized_current_state.cost_accumulator.Cost())
    
  def GetPointsLeft(self):
    return self.points_left
  
  # NOTE(igushev): Methods below are not part of Interface API. 
  def CurrentTime(self):
    return self.current_state.current_datetime

  def CurrentCoordinates(self):
    return self.current_state.current_coordinates

  def CurrentCost(self):
    return self.current_state.cost_accumulator.Cost()


class DayVisitCostCalculatorGenerator(DayVisitCostCalculatorGeneratorInterface):

  def __init__(self, move_calculator, point_fit, cost_accumulator_generator):
    self.move_calculator = move_calculator
    self.point_fit = point_fit
    self.cost_accumulator_generator = cost_accumulator_generator
  
  def Generate(self, day_visit_parameters):
    return DayVisitCostCalculator.Init(
        self.move_calculator, self.point_fit, day_visit_parameters,
        self.cost_accumulator_generator)
