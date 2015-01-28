import Yusi
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.city_visit_heap import CityVisitHeap
from Yusi.YuFinder.days_permutations import DaysPermutations


class CouldPush(object):
  
  def __init__(self):
    self.value = False


class CityVisitFinder(object):
  def __init__(self, day_visit_finder, city_visit_cost_calculator,
               max_depth, city_visit_heap_size, max_non_pushed_points):
    self.day_visit_finder = day_visit_finder
    self.city_visit_cost_calculator = city_visit_cost_calculator
    self.max_depth = max_depth
    self.city_visit_heap_size = city_visit_heap_size
    self.max_non_pushed_points = max_non_pushed_points
    
  def _PushPointsToDayVisits(
      self, points, days_consider, day_visits, day_visit_parameterss,
      depth, could_push, city_visit_heap):
    assert len(day_visits) == len(day_visit_parameterss)
    for days_permutation in DaysPermutations(points, days_consider):
      # Initialize structure for next iteration.
      points_left = []
      next_day_visits_consider = days_consider[:]
      next_day_visits = day_visits[:]
      
      # Try to fit to each day its points.
      for i, day_points_add in days_permutation.iteritems():
        day_points_all = day_visits[i].GetPoints()
        day_points_all.extend(day_points_add)
        day_points_left, day_visit_best = (
            self.day_visit_finder.FindDayVisit(
                day_points_all, day_visit_parameterss[i]))
        points_left.extend(day_points_left)
        next_day_visits_consider[i] = False
        next_day_visits = (
            next_day_visits[:i] + [day_visit_best] + next_day_visits[i+1:])
  
      if len(points_left) > 1:
        print('More than one point left after adding to existing DayVisits!')

      # NOTE(igushev): The only option when points_left are the same as input
      # points, it than each corresponding day has not fit its points. The
      # recursive call will check other days, which should be covered by this
      # level of permutation.
      if set(points_left) == set(points):
        continue
      
      # NOTE(igushev): If maximum depth of recursion or no points_left, add a
      # potential result.
      if depth == self.max_depth or not points_left:
        cost = self.city_visit_cost_calculator.CalculateCityVisitCost(
            next_day_visits, points_left)
        city_visit_heap.PushCityVisit(
            city_visit.CityVisit(next_day_visits, cost))
        if not points_left:
          could_push.value = True
        continue
      
      # NOTE(igushev): Recursion call.
      self._PushPointsToDayVisits(
          points_left, next_day_visits_consider, next_day_visits,
          day_visit_parameterss, depth+1, could_push, city_visit_heap)
  
  def FindCityVisit(self, points, day_visit_parameterss):
    """Find best CityVisit."""
    initial_day_visits = [
        day_visit for _, day_visit in [
           self.day_visit_finder.FindDayVisit([], day_visit_parameters)
           for day_visit_parameters in day_visit_parameterss]]
    initial_cost = self.city_visit_cost_calculator.CalculateCityVisitCost(
        initial_day_visits, [])
    city_visits = [city_visit.CityVisit(initial_day_visits, initial_cost)]
    could_not_push = 0
    for point in points:
      could_push = CouldPush()
      city_visit_heap = CityVisitHeap(
          self.city_visit_heap_size, day_visit_parameterss)
      for city_visit_add_to in city_visits:
        day_visits = city_visit_add_to.day_visits
        days_consider = [True] * len(day_visits)
        self._PushPointsToDayVisits(
            [point], days_consider, day_visits, day_visit_parameterss,
            0, could_push, city_visit_heap)
      if not could_push.value:
        could_not_push += 1
        if could_not_push >= self.max_non_pushed_points:
          assert len(city_visits) >= 1
          return city_visits[0]
      if city_visit_heap.Size():
        city_visit_heap.Shrink()
        city_visits = city_visit_heap.GetCityVisits()
    assert len(city_visits) >= 1
    return city_visits[0]
