import datetime
import os

from data import city_visit
from config import config as config_


def GetDayVisitParameterss(start_end_coordinates, first_day, last_day):
  def GetDayVisitParameters(day):
    return city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2015, 7, day, 10, 0, 0),
        end_datetime=datetime.datetime(2015, 7, day, 19, 0, 0),
        lunch_start_datetime=datetime.datetime(2015, 7, day, 14, 0, 0),
        lunch_hours=1.,
        start_coordinates=start_end_coordinates,
        end_coordinates=start_end_coordinates)

  return [GetDayVisitParameters(day) for day in range(first_day, last_day)]


class CityVisitRouterRunner(object):
  
  def __init__(self):
    config = config_.GetConfig(os.path.join('config', 'runner.config'))
    self.city_visit_router = config_.GetCityVisitRouter(config)
    self.city_visit_accumulator_generator = config_.GetCityVisitAccumulatorGenerator(config)


  def Run(self, points_input, day_visit_parameterss):
    start = datetime.datetime.now()
  
    city_visit_best, points_left = (
        self.city_visit_router.RouteCityVisit(
            points_input, day_visit_parameterss, self.city_visit_accumulator_generator))

    print('Points to visit in priority: %s' %
          ', '.join(point.name for point in points_input))
    print('Your schedule:')
    print(city_visit_best)
    print('Points left: %s' %
          ', '.join(point_left.name for point_left in points_left))
  
    print('Elapsed time %s' % (datetime.datetime.now() - start))
