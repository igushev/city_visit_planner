import Yusi
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.city_visit_heap import CityVisitHeap
from Yusi.YuFinder.days_permutations import DaysPermutations


class CouldPush(object):
  
  def __init__(self):
    self.value = False


class CityVisitFinder(object):
  def __init__(self, day_visit_finder, city_visit_cost_calculator_generator,
               max_depth, city_visit_heap_size, max_non_pushed_points):
    self.day_visit_finder = day_visit_finder
    self.city_visit_cost_calculator_generator = (
        city_visit_cost_calculator_generator)
    self.max_depth = max_depth
    self.city_visit_heap_size = city_visit_heap_size
    self.max_non_pushed_points = max_non_pushed_points
    
  def _PushPointsToDayVisits(
      self, depth, points, days_consider, day_visits, points_left,
      could_push, city_visit_heap, day_visit_parameterss):
    assert len(days_consider) == len(day_visits)
    assert len(day_visits) == len(day_visit_parameterss)
    for days_permutation in DaysPermutations(points, days_consider):
      # Initialize structure for next iteration.
      next_points_left = []
      next_day_visits_consider = days_consider[:]
      next_day_visits = day_visits[:]
      
      # Try to fit to each day its points.
      for i, day_points_add in days_permutation.iteritems():
        day_points_all = day_visits[i].GetPoints()
        day_points_all.extend(day_points_add)
        day_points_left, day_visit_best = (
            self.day_visit_finder.FindDayVisit(
                day_points_all, day_visit_parameterss[i]))
        next_points_left.extend(day_points_left)
        next_day_visits_consider[i] = False
        next_day_visits = (
            next_day_visits[:i] + [day_visit_best] + next_day_visits[i+1:])
  
      if len(next_points_left) > 1:
        print('More than one point left after adding to existing DayVisits!')

      # NOTE(igushev): The only option when next_points_left are the same as
      # input points, it than each corresponding day has not fit its points. The
      # recursive call will check other days, which should be covered by this
      # level of permutation.
      if set(next_points_left) == set(points):
        continue
      
      # NOTE(igushev): If maximum depth of recursion or no next_points_left, add
      # a potential result.
      if depth == self.max_depth or not next_points_left:
        city_visit_cost_calculator = (
            self.city_visit_cost_calculator_generator.Generate(
                next_day_visits))
        city_visit_cost_calculator.AddPointsLeft(points_left + next_points_left)
        city_visit_heap.PushCalculator(city_visit_cost_calculator)
        if not next_points_left:
          could_push.value = True
        continue
      
      # NOTE(igushev): Recursion call.
      self._PushPointsToDayVisits(
          depth+1, next_points_left, next_day_visits_consider, next_day_visits,
          points_left, could_push, city_visit_heap, day_visit_parameterss)
  
  def FindCityVisit(self, points, day_visit_parameterss):
    """Find best CityVisit."""
    initial_day_visits = [
        day_visit for _, day_visit in [
           self.day_visit_finder.FindDayVisit([], day_visit_parameters)
           for day_visit_parameters in day_visit_parameterss]]
    city_visit_cost_calculators = [
        self.city_visit_cost_calculator_generator.Generate(initial_day_visits)]
    could_not_push = 0
    for i, point in enumerate(points):
      could_push = CouldPush()
      city_visit_heap = CityVisitHeap(
          self.city_visit_heap_size, day_visit_parameterss)
      for city_visit_cost_calculator_add_to in city_visit_cost_calculators:
        day_visits = city_visit_cost_calculator_add_to.day_visits
        days_consider = [True] * len(day_visits)
        points_left = city_visit_cost_calculator_add_to.GetPointsLeft()
        self._PushPointsToDayVisits(
            0, [point], days_consider, day_visits, points_left,
            could_push, city_visit_heap, day_visit_parameterss)
      if not could_push.value:
        could_not_push += 1
        if could_not_push >= self.max_non_pushed_points:
          for city_visit_cost_calculator in city_visit_cost_calculators:
            city_visit_cost_calculator.AddPointsLeft(points[i:])
          break
      if city_visit_heap.Size():
        city_visit_heap.Shrink()
        city_visit_cost_calculators = city_visit_heap.GetCalculators()
      else:
        for city_visit_cost_calculator in city_visit_cost_calculators:
          city_visit_cost_calculator.AddPointsLeft([point])
    assert len(city_visit_cost_calculators) >= 1
    return city_visit_cost_calculators[0].CityVisit()
