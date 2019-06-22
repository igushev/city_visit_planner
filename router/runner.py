import datetime
import os

from config import config as config_


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
