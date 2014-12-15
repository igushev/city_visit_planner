import copy

import Yusi
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.day_visit_finder import FindDayVisit
from Yusi.YuFinder.city_visit_heap import CityVisitHeap


MAX_DEPTH = 1
CITY_VISIT_HEAP_SIZE = 10
MAX_NON_PUSHED_POINTS = 3


def _PushToDayVisits(
    point, day_visits_consider, day_visits, calculator_generators, depth,
    city_visit_heap):
  for i, day_visit in enumerate(day_visits):
    if not day_visits_consider[i]:
      continue
    all_points = day_visit.GetPoints()
    all_points.append(point)
    points_left, day_visit_best = FindDayVisit(
        calculator_generators[i], all_points)
    next_day_visits = day_visits[:i] + [day_visit_best] + day_visits[i+1:]
    if not points_left:
      city_visit_heap.PushCityVisit(city_visit.CityVisit(next_day_visits))
      continue
    assert len(points_left) == 1, (
        'Only one point can be left after adding to existing DayVisit.')
    point_left = points_left[0]
    if point_left == point:
      continue
    if depth == MAX_DEPTH:
      continue
    next_day_visits_consider = day_visits_consider[:]
    next_day_visits_consider[i] = False
    _PushToDayVisits(
        point_left, next_day_visits_consider, next_day_visits,
        calculator_generators, depth+1, city_visit_heap)


def FindCityVisit(points, calculator_generators):
  """Find best CityVisit."""
  city_visits = [city_visit.CityVisit(
    [calculator_generator.Generate().FinalizedDayVisit()
     for calculator_generator in calculator_generators])]
  cannot_push = 0
  day_visit_parameterss = [
      calculator_generator.day_visit_parameters
      for calculator_generator in calculator_generators]
  for point in points:
    city_visit_heap = CityVisitHeap(CITY_VISIT_HEAP_SIZE, day_visit_parameterss)
    for city_visit_add_to in city_visits:
      day_visits = city_visit_add_to.day_visits
      day_visits_consider = [True] * len(day_visits)
      _PushToDayVisits(
          point, day_visits_consider, day_visits, calculator_generators, 0,
          city_visit_heap)
    if city_visit_heap.Size():
      city_visit_heap.Shrink()
      city_visits = city_visit_heap.GetCityVisits()
    else:
      cannot_push += 1
      if cannot_push >= MAX_NON_PUSHED_POINTS:
        return city_visits[0]
  return city_visits[0]
