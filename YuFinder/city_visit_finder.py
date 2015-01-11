import copy

import Yusi
from Yusi.YuFinder import city_visit
from Yusi.YuFinder.day_visit_finder import FindDayVisit
from Yusi.YuFinder.city_visit_heap import CityVisitHeap


MAX_DEPTH = 1
CITY_VISIT_HEAP_SIZE = 10
MAX_NON_PUSHED_POINTS = 3


def _PushToDayVisits(
    point, days_consider, day_visits, day_visit_parameterss,
    calculator_generator, day_visit_finder_heap_generator, depth,
    city_visit_heap):
  assert len(day_visits) == len(day_visit_parameterss)
  for i, day_visit in enumerate(day_visits):
    if not days_consider[i]:
      continue
    all_points = day_visit.GetPoints()
    all_points.append(point)
    points_left, day_visit_best = FindDayVisit(
        all_points, day_visit_parameterss[i], calculator_generator,
        day_visit_finder_heap_generator)
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
    next_day_visits_consider = days_consider[:]
    next_day_visits_consider[i] = False
    _PushToDayVisits(
        point_left, next_day_visits_consider, next_day_visits,
        day_visit_parameterss, calculator_generator,
        day_visit_finder_heap_generator, depth+1, city_visit_heap)


# TODO(igushev): Distinguish Cost of DayVisit when compare DayVisit and when
# compare CityVisit, since when comparing CityVisit we don't need to consider
# PointNoVisit, because such points are going to be in other DayVisits.
def FindCityVisit(points, day_visit_parameterss, calculator_generator,
                  day_visit_finder_heap_generator):
  """Find best CityVisit."""
  city_visits = [city_visit.CityVisit(
    [calculator_generator.Generate(day_visit_parameters).FinalizedDayVisit()
     for day_visit_parameters in day_visit_parameterss])]
  cannot_push = 0
  for point in points:
    city_visit_heap = CityVisitHeap(CITY_VISIT_HEAP_SIZE, day_visit_parameterss)
    for city_visit_add_to in city_visits:
      day_visits = city_visit_add_to.day_visits
      days_consider = [True] * len(day_visits)
      _PushToDayVisits(
          point, days_consider, day_visits, day_visit_parameterss,
          calculator_generator, day_visit_finder_heap_generator, 0,
          city_visit_heap)
    if city_visit_heap.Size():
      city_visit_heap.Shrink()
      city_visits = city_visit_heap.GetCityVisits()
    else:
      cannot_push += 1
      if cannot_push >= MAX_NON_PUSHED_POINTS:
        return city_visits[0]
  return city_visits[0]
