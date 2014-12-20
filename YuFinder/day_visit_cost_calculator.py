import datetime

from Yusi.YuFinder import city_visit
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface,\
  DayVisitCostCalculatorGeneratorInterface


# TODO(igushev): If point cannot be added, internal state still changes
# depending what couldn't be added (move, lunch or point). When it happens
# none of methods can be called agains. Internal self._invariant responsible
# for that. Good solution should be, if point cannot be added, internal state
# should not be changed at all.
class DayVisitCostCalculator(DayVisitCostCalculatorInterface):
  """Calculates cost of DayVisit."""

  def __init__(self, move_calculator, point_fit, day_visit_parameters,
               cost_accumulator_generator):
    self.move_calculator = move_calculator
    self.point_fit = point_fit
    self.start_datetime = day_visit_parameters.start_datetime
    self.current_datetime = day_visit_parameters.start_datetime
    self.end_datetime = day_visit_parameters.end_datetime
    self.lunch_start_datetime = day_visit_parameters.lunch_start_datetime
    self.lunch_hours = day_visit_parameters.lunch_hours
    self.start_coordinates = day_visit_parameters.start_coordinates
    self.current_coordinates = day_visit_parameters.start_coordinates
    self.end_coordinates = (
      day_visit_parameters.end_coordinates or
      day_visit_parameters.start_coordinates)
    self.cost_accumulator = cost_accumulator_generator.Generate()
    self.actions = []
    self._invariant = True

  def _AddPointVisit(self, point):
    visit_timedelta = datetime.timedelta(hours=point.duration)
    visit_start_end_datetime = city_visit.StartEndDatetime(
        self.current_datetime, self.current_datetime + visit_timedelta)
    if not self.point_fit.IfPointFit(
        visit_start_end_datetime, point.operating_hours):
      return False
    if visit_start_end_datetime.end > self.end_datetime:
      return False
    self.current_datetime = visit_start_end_datetime.end
    self.current_coordinates = point.coordinates_ends
    self.cost_accumulator.AddPointVisit(point)
    self.actions.append(city_visit.PointVisit(point, visit_start_end_datetime))
    if visit_start_end_datetime.Fit(self.lunch_start_datetime):
      if not self._AddLunch():
        return False
    return True

  def _AddMoveBetween(self, to_coordinates):
    move_description = self.move_calculator.CalculateMoveDescription(
        self.current_coordinates, to_coordinates)
    move_timedelta = datetime.timedelta(hours=move_description.move_hours)
    move_start_end_datetime = city_visit.StartEndDatetime(
        self.current_datetime, self.current_datetime + move_timedelta)
    if move_start_end_datetime.end > self.end_datetime:
      return False
    from_coordinates = self.current_coordinates
    self.current_datetime = move_start_end_datetime.end
    self.current_coordinates = to_coordinates
    self.cost_accumulator.AddMoveBetween(move_description)
    self.actions.append(city_visit.MoveBetween(
      from_coordinates, to_coordinates,
      move_start_end_datetime, move_description))
    if move_start_end_datetime.Fit(self.lunch_start_datetime):
      if not self._AddLunch():
        return False
    return True

  def _AddLunch(self):
    lunch_start_end_datetime = city_visit.StartEndDatetime(
        self.current_datetime,
        self.current_datetime + datetime.timedelta(hours=self.lunch_hours))
    if lunch_start_end_datetime.end > self.end_datetime:
      return False
    self.current_datetime = lunch_start_end_datetime.end
    self.cost_accumulator.AddLunch(self.lunch_hours)
    self.actions.append(city_visit.Lunch(lunch_start_end_datetime))
    return True

  def PushPoint(self, point):
    assert self._invariant
    if not self._AddMoveBetween(point.coordinates_starts):
      self._invariant = False
      return False
    if not self._AddPointVisit(point):
      self._invariant = False
      return False
    return True

  def CanFinalize(self):
    assert self._invariant
    move_description = self.move_calculator.CalculateMoveDescription(
        self.current_coordinates, self.end_coordinates)
    move_timedelta = datetime.timedelta(hours=move_description.move_hours)
    if self.current_datetime + move_timedelta > self.end_datetime:
      return False
    return True
  
  def FinalizedCost(self):
    assert self.CanFinalize()
    move_description = self.move_calculator.CalculateMoveDescription(
        self.current_coordinates, self.end_coordinates)
    finalized_cost_accumulator = self.cost_accumulator.Copy()
    finalized_cost_accumulator.AddMoveBetween(move_description)
    return finalized_cost_accumulator.Cost()

  def FinalizedDayVisit(self):
    assert self.CanFinalize()
    finalized_cost = self.FinalizedCost()
    actions = self.actions[:]
    move_description = self.move_calculator.CalculateMoveDescription(
        self.current_coordinates, self.end_coordinates)
    move_timedelta = datetime.timedelta(hours=move_description.move_hours)
    move_start_end_datetime = city_visit.StartEndDatetime(
        self.current_datetime, self.current_datetime + move_timedelta)
    actions.append(city_visit.MoveBetween(
      self.current_coordinates, self.end_coordinates,
      move_start_end_datetime, move_description))
    return city_visit.DayVisit(self.start_datetime, actions, finalized_cost)
  
  def CurrentTime(self):
    assert self._invariant
    return self.current_datetime

  def CurrentCoordinates(self):
    assert self._invariant
    return self.current_coordinates

  def CurrentCost(self):
    assert self._invariant
    return self.cost_accumulator.Cost()


class DayVisitCostCalculatorGenerator(DayVisitCostCalculatorGeneratorInterface):

  def __init__(self, move_calculator, point_fit, day_visit_parameters,
               cost_accumulator_generator):
    self.move_calculator = move_calculator
    self.point_fit = point_fit
    self.day_visit_parameters = day_visit_parameters
    self.cost_accumulator_generator = cost_accumulator_generator
  
  def Generate(self):
    return DayVisitCostCalculator(
        self.move_calculator, self.point_fit, self.day_visit_parameters,
        self.cost_accumulator_generator)
