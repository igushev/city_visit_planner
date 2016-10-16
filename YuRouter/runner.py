import datetime

from Yusi.YuPoint.city_visit import DayVisitParameters
from Yusi.YuRouter.prototype_parameters import PrototypeParameters


def GetDayVisitParameterss(start_end_coordinates, first_day, last_day):
  def GetDayVisitParameters(day):
    return DayVisitParameters(
        start_datetime=datetime.datetime(2015, 7, day, 10, 0, 0),
        end_datetime=datetime.datetime(2015, 7, day, 19, 0, 0),
        lunch_start_datetime=datetime.datetime(2015, 7, day, 14, 0, 0),
        lunch_hours=1.,
        start_coordinates=start_end_coordinates,
        end_coordinates=start_end_coordinates)

  return [GetDayVisitParameters(day) for day in range(first_day, last_day)]


class CityVisitRouterRunner(object):
  
  def __init__(self):
    self.max_walking_distance=1.0
    self.city_visit_router = (
        PrototypeParameters(max_walking_distance=self.max_walking_distance,
                            validate_max_walking_distance=False).
        CityVisitRouter())

  def Run(self, points_input, day_visit_parameterss):
    start = datetime.datetime.now()
  
    city_visit_best, points_left = (
        self.city_visit_router.RouteCityVisit(
            points_input, day_visit_parameterss))

    print('Points to visit in priority: %s' %
          ', '.join(point.name for point in points_input))
    print('Maximum walking distance: %d mile(s)' % self.max_walking_distance)
    print('Your schedule:')
    print(city_visit_best)
    print('Points left: %s' %
          ', '.join(point_left.name for point_left in points_left))
  
    print('Elapsed time %s' % (datetime.datetime.now() - start))
