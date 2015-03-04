import multiprocessing

import Yusi
from Yusi.YuRouter.city_visit_heap import CityVisitHeap
from Yusi.YuRouter.days_permutations import DaysPermutations


################################################################################
# NOTE(igushev): Code between hashtags lines is to be run inside worker
# processes, therefore instead of module-level should be considered as
# process-level.
_day_visit_router = None
_city_visit_cost_calculator_generator = None
_max_depth = None
_city_visit_heap_size = None


def _PushPointsToDayVisitsInit(
    day_visit_router, city_visit_cost_calculator_generator, max_depth,
    city_visit_heap_size):
  global _day_visit_router
  global _city_visit_cost_calculator_generator
  global _max_depth
  global _city_visit_heap_size
  _day_visit_router = day_visit_router
  _city_visit_cost_calculator_generator = city_visit_cost_calculator_generator
  _max_depth = max_depth
  _city_visit_heap_size = city_visit_heap_size
  

class CouldPush(object):
  
  def __init__(self):
    self.value = False


def _PushPointsToDayVisitsImpl(
    depth, points, days_consider, day_visits, points_left,
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
      day_visit_best, day_points_left = (
          _day_visit_router.RouteDayVisit(
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
    if depth == _max_depth or not next_points_left:
      city_visit_cost_calculator = (
          _city_visit_cost_calculator_generator.Generate(
              next_day_visits))
      city_visit_cost_calculator.AddPointsLeft(points_left + next_points_left)
      city_visit_heap.PushCalculator(city_visit_cost_calculator)
      if not next_points_left:
        could_push.value = True
      continue
    
    # NOTE(igushev): Recursion call.
    _PushPointsToDayVisitsImpl(
        depth+1, next_points_left, next_day_visits_consider, next_day_visits,
        points_left, could_push, city_visit_heap, day_visit_parameterss)


def _PushPointsToDayVisitsWork(
    points, day_visits, points_left, day_visit_parameterss):
  days_consider = [True] * len(day_visits)
  could_push = CouldPush()
  city_visit_heap = CityVisitHeap(
      _city_visit_heap_size, day_visit_parameterss)
  _PushPointsToDayVisitsImpl(
      0, points, days_consider, day_visits, points_left,
      could_push, city_visit_heap, day_visit_parameterss)
  city_visit_heap.Shrink()
  return could_push, city_visit_heap
################################################################################


class CityVisitRouterInterface(object):
  """Abstract class which routes points."""
  
  def RouteCityVisit(self, points, day_visit_parameterss):
    """Route maximum number of points with minimum cost for CityVisit."""
    raise NotImplemented()


class CityVisitRouter(CityVisitRouterInterface):

  def __init__(self, day_visit_router, city_visit_cost_calculator_generator,
               max_depth, city_visit_heap_size, max_non_pushed_points,
               num_processes):
    self.day_visit_router = day_visit_router
    self.city_visit_cost_calculator_generator = (
        city_visit_cost_calculator_generator)
    self.max_depth = max_depth  # Don't need, but still add as member.
    self.city_visit_heap_size = city_visit_heap_size
    self.max_non_pushed_points = max_non_pushed_points
    self.workers_pool = multiprocessing.Pool(
        num_processes,
        initializer=_PushPointsToDayVisitsInit,
        initargs=(day_visit_router, city_visit_cost_calculator_generator,
                  max_depth, city_visit_heap_size))

  def RouteCityVisit(self, points, day_visit_parameterss):
    initial_day_visits = [
        day_visit for day_visit, _ in [
           self.day_visit_router.RouteDayVisit([], day_visit_parameters)
           for day_visit_parameters in day_visit_parameterss]]
    city_visit_cost_calculators = [
        self.city_visit_cost_calculator_generator.Generate(initial_day_visits)]
    could_not_push = 0
    for i, point in enumerate(points):

      # NOTE(igushev): Run in parallel pushing points to different
      # CityVisitCostCalculators from previous heap and collect AsyncResult
      # objects. 
      push_points_to_day_visits_results = []
      for city_visit_cost_calculator in city_visit_cost_calculators:
        day_visits = city_visit_cost_calculator.day_visits
        points_left = city_visit_cost_calculator.GetPointsLeft()
        push_points_to_day_visits_results.append(
            self.workers_pool.apply_async(
                _PushPointsToDayVisitsWork,
                args=([point], day_visits, points_left, day_visit_parameterss)))

      # NOTE(igushev): Process results and fill overall could_push and
      # city_visit_heap.
      could_push = CouldPush()
      city_visit_heap = CityVisitHeap(
          self.city_visit_heap_size, day_visit_parameterss)
      for push_points_to_day_visits_result in push_points_to_day_visits_results:
        could_push_one, city_visit_heap_one = (
            push_points_to_day_visits_result.get())
        if could_push_one.value:
          could_push.value = True
        for city_visit_cost_calculator in city_visit_heap_one.GetCalculators():
          city_visit_heap.PushCalculator(city_visit_cost_calculator)

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
    city_visit_cost_calculators_best = city_visit_cost_calculators[0]
    return (city_visit_cost_calculators_best.CityVisit(),
            city_visit_cost_calculators_best.GetPointsLeft())
