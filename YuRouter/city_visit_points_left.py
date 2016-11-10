from collections import namedtuple


from Yusi.YuPoint.city_visit import PointVisit, MoveBetween, Lunch, CityVisit,\
  CityVisitSummary


CityVisitPointsLeft = namedtuple(
    'CityVisitPointsLeft', 'city_visit points_left')


class CityVisitPointsLeftGeneratorInterface(object):
  """Abstract class which generates an instance of CityVisitPointsLeft."""

  def Generate(self, day_visits, day_visit_parameterss, points_left):
    """Generates an instance of CityVisitPointsLeft."""
    raise NotImplemented()


class CityVisitPointsLeftGenerator(CityVisitPointsLeftGeneratorInterface):
  """Generates an instance of CityVisitPointsLeft."""

  def __init__(self, cost_accumulator_generator):
    self.cost_accumulator_generator = cost_accumulator_generator
  
  def Generate(self, day_visits, day_visit_parameterss, points_left):

    cost_accumulator = self.cost_accumulator_generator.Generate()
    price = 0
    for day_visit, day_visit_parameters in (
        zip(day_visits, day_visit_parameterss)):
      for action in day_visit.actions:
        if isinstance(action, PointVisit):
          cost_accumulator.AddPointVisit(action.point)
        elif isinstance(action, MoveBetween):
          cost_accumulator.AddMoveBetween(action.move_description)
        elif isinstance(action, Lunch):
          cost_accumulator.AddLunch(action.lunch_hours)
        else:
          raise NotImplemented('Unknown action type %s' % type(action))
      unused_time = (day_visit_parameters.end_datetime -
                     day_visit.actions[-1].start_end_datetime.end)
      cost_accumulator.AddUnusedTime(unused_time)
      price += day_visit.price
    for point_left in points_left:
      cost_accumulator.AddPointLeft(point_left)
    city_visit_summary = CityVisitSummary(cost_accumulator.Cost(), price)
    city_visit = CityVisit(day_visits, city_visit_summary)
    return CityVisitPointsLeft(city_visit, points_left)
