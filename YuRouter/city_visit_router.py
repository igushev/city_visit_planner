import multiprocessing

import Yusi
from Yusi.YuRouter.city_visit_points_left import CityVisitPointsLeftGenerator
from Yusi.YuRouter.city_visit_heap import CityVisitHeap
from Yusi.YuRouter.days_permutations import DaysPermutations
from Yusi.YuRouter.day_visit_router import DayVisitRouterInterface
from Yusi.YuRouter.points_queue import PointsQueueGeneratorInterface
from Yusi.YuPoint.point import PointInterface
from Yusi.YuPoint.city_visit import DayVisitParametersInterface,\
  DayVisitInterface
from Yusi.YuRouter.city_visit_accumulator import CityVisitAccumulatorGenerator


################################################################################
# NOTE(igushev): Code between hashtags lines is to be run inside worker
# processes, therefore instead of module-level should be considered as
# process-level.
_day_visit_router = None
_city_visit_points_left_generator = None
_max_depth = None
_city_visit_heap_size = None


def _PushPointsToDayVisitsInit(
    day_visit_router, city_visit_points_left_generator, max_depth,
    city_visit_heap_size):
  global _day_visit_router
  global _city_visit_points_left_generator
  global _max_depth
  global _city_visit_heap_size
  _day_visit_router = day_visit_router
  _city_visit_points_left_generator = city_visit_points_left_generator
  _max_depth = max_depth
  _city_visit_heap_size = city_visit_heap_size
  

class CouldPush(object):
  
  def __init__(self):
    self.value = False


def _PushPointsToDayVisitsImpl(
    depth, points, days_consider, day_visits, points_left,
    could_push, city_visit_heap, day_visit_parameterss, points_left_consistent):
  assert len(days_consider) == len(day_visits)
  assert len(day_visits) == len(day_visit_parameterss)
  for days_permutation in DaysPermutations(points, days_consider):
    # Initialize structure for next iteration.
    next_points_left = []
    next_day_visits_consider = days_consider[:]
    next_day_visits = day_visits[:]
    
    # Try to fit to each day its points.
    for i, day_points_add in days_permutation.items():
      day_points_all = day_visits[i].GetPoints()
      day_points_all.extend(day_points_add)
      day_visit_best, points_left_best = (
          _day_visit_router.RouteDayVisit(
              day_points_all, day_visit_parameterss[i]))
      assert isinstance(day_visit_best, DayVisitInterface)
      for point_left_best in points_left_best:
        assert isinstance(point_left_best, PointInterface)
      next_points_left.extend(points_left_best)
      next_day_visits_consider[i] = False
      next_day_visits = (
          next_day_visits[:i] + [day_visit_best] + next_day_visits[i+1:])

    if len(next_points_left) > 1:
      print('More than one point left after adding to existing DayVisits!')

    # NOTE(igushev): The only option when next_points_left are the same as
    # input points, it than each corresponding day has not fit its points. The
    # recursive call will check other days, which should be covered by this
    # level of permutation.
    # NOTE(igushev): If maximum depth of recursion or no next_points_left, add
    # a potential result.
    if (set(next_points_left) == set(points) or
        depth == _max_depth or
        not next_points_left or
        all(not day_visit_consider
            for day_visit_consider in next_day_visits_consider)):
      city_visit_points_left = (
          _city_visit_points_left_generator.Generate(
              next_day_visits, day_visit_parameterss,
              points_left + next_points_left))
      city_visit_heap.PushCityVisit(city_visit_points_left)
      # If next_points_left are only the ones we consistently can't push,
      # consider this iteration successful and assign could_push True.
      if set(next_points_left) <= points_left_consistent:
        could_push.value = True
      continue
    
    # NOTE(igushev): Recursion call.
    _PushPointsToDayVisitsImpl(
        depth+1, next_points_left, next_day_visits_consider, next_day_visits,
        points_left, could_push, city_visit_heap, day_visit_parameterss,
        points_left_consistent)


def _PushPointsToDayVisitsWork(
    points, day_visits, points_left, day_visit_parameterss,
    points_left_consistent):
  days_consider = [True] * len(day_visits)
  could_push = CouldPush()
  city_visit_heap = CityVisitHeap(
      _city_visit_heap_size, day_visit_parameterss)
  _PushPointsToDayVisitsImpl(
      1, points, days_consider, day_visits, points_left,
      could_push, city_visit_heap, day_visit_parameterss,
      points_left_consistent)
  city_visit_heap.Shrink()
  return could_push, city_visit_heap
################################################################################


class CityVisitRouterInterface(object):
  """Abstract class which routes points during CityVisit."""
  
  def RouteCityVisit(self, points, day_visit_parameterss,
                     city_visit_accumulator_generator):
    """Route maximum number of points with minimum cost for CityVisit."""
    raise NotImplemented()


class CityVisitRouter(CityVisitRouterInterface):
  """Routes points during CityVisit using permutation and keeping track of
  best so far."""

  def __init__(self, day_visit_router, city_visit_points_left_generator,
               points_queue_generator, shard_num_days, max_depth,
               city_visit_heap_size, max_non_pushed_points, num_processes):
    assert isinstance(day_visit_router, DayVisitRouterInterface)
    assert isinstance(city_visit_points_left_generator,
                      CityVisitPointsLeftGenerator)
    assert isinstance(points_queue_generator, PointsQueueGeneratorInterface)
    if shard_num_days is not None:
      assert isinstance(shard_num_days, int)
    assert isinstance(max_depth, int)
    assert isinstance(city_visit_heap_size, int)
    assert isinstance(max_non_pushed_points, int)
    if num_processes is not None:
      assert isinstance(num_processes, int)

    self.day_visit_router = day_visit_router
    self.city_visit_points_left_generator = city_visit_points_left_generator
    self.points_queue_generator = points_queue_generator
    self.shard_num_days = shard_num_days
    self.max_depth = max_depth  # Don't need, but still add as member.
    self.city_visit_heap_size = city_visit_heap_size
    self.max_non_pushed_points = max_non_pushed_points
    self.workers_pool = multiprocessing.Pool(
        num_processes,
        initializer=_PushPointsToDayVisitsInit,
        initargs=(day_visit_router, city_visit_points_left_generator,
                  max_depth, city_visit_heap_size))

  def RouteCityVisitShard(self, points_queue, day_visit_parameterss,
                          points_left_consistent):
    initial_day_visits = []
    for day_visit_parameters in day_visit_parameterss:
        day_visit, points_left = (
            self.day_visit_router.RouteDayVisit([], day_visit_parameters))
        assert isinstance(day_visit, DayVisitInterface)
        assert not points_left
        initial_day_visits.append(day_visit) 
    city_visit_points_lefts = [
        self.city_visit_points_left_generator.Generate(
            initial_day_visits, day_visit_parameterss, [])]
    could_not_push = 0
    while points_queue.HasPoints():
      # NOTE(igushev): Run in parallel pushing points to different
      # CityVisitPointsLefts from previous heap and collect AsyncResult
      # objects. 
      push_points = points_queue.GetPushPoints(day_visit_parameterss)
      push_points_to_day_visits_results = []
      for city_visit_points_left in city_visit_points_lefts:
        day_visits = city_visit_points_left.city_visit.day_visits
        points_left = city_visit_points_left.points_left
        push_points_to_day_visits_results.append(
            self.workers_pool.apply_async(
                _PushPointsToDayVisitsWork,
                args=(push_points, day_visits, points_left,
                      day_visit_parameterss, points_left_consistent)))

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
        for city_visit_points_left in city_visit_heap_one.GetCityVisitPointsLeftList():
          city_visit_heap.PushCityVisit(city_visit_points_left)

      city_visit_heap.Shrink()
      city_visit_points_lefts = city_visit_heap.GetCityVisitPointsLeftList()
      if not could_push.value:
        could_not_push += 1
        if could_not_push >= self.max_non_pushed_points:
          break
    assert len(city_visit_points_lefts) >= 1
    city_visit_points_left_best = city_visit_points_lefts[0]
    return (city_visit_points_left_best.city_visit,
            city_visit_points_left_best.points_left)

  def RouteCityVisit(self, points, day_visit_parameterss,
                     city_visit_accumulator_generator):
    for point in points:
      assert isinstance(point, PointInterface)
    for day_visit_parameters in day_visit_parameterss:
      assert isinstance(day_visit_parameters, DayVisitParametersInterface)
    assert isinstance(city_visit_accumulator_generator,
                      CityVisitAccumulatorGenerator)

    shard_num_days = self.shard_num_days or len(day_visit_parameterss)
    city_visit_accumulator = city_visit_accumulator_generator.Generate()
    points_queue = self.points_queue_generator.Generate(points)
    points_left_consistent = set([])
    for shard_i, begin in (
        enumerate(range(0, len(day_visit_parameterss), shard_num_days))):
      end = min(begin + shard_num_days, len(day_visit_parameterss))
      print('Processing shard %d from %d to %d' % (shard_i+1, begin, end))

      city_visit_points_left_shard, points_left_shard = (
          self.RouteCityVisitShard(
              points_queue, day_visit_parameterss[begin:end],
              points_left_consistent))

      city_visit_accumulator.AddDayVisits(
          city_visit_points_left_shard.day_visits,
          day_visit_parameterss[begin:end])
      # Next iteration points_queue should points left from previous iteration
      # and the rest of points.
      points_queue.AddBackToQueue(points_left_shard)
      points_left_consistent.update(set(points_left_shard))

    city_visit_accumulator.AddPointsLeft(points_queue.GetPointsLeft())
    return city_visit_accumulator.Result(
        self.city_visit_points_left_generator)
