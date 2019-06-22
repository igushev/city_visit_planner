import datetime
import os

from config import config as config_


class CityVisitFinderRunner(object):
  
  def __init__(self):
    config = config_.GetConfig(os.path.join('config', 'runner.config'))
    self.city_visit_finder = config_.GetCityVisitFinder(config)
    self.city_visit_accumulator_generator = config_.GetCityVisitAccumulatorGenerator(config)

  def Run(self, points_input, city_visit_parameters):
    start = datetime.datetime.now()

    city_visit = self.city_visit_finder.FindCityVisit(
        points_input, city_visit_parameters, self.city_visit_accumulator_generator)

    print('Input points: %s' % ', '.join(point.name for point in points_input))
    print('Your schedule:')
    print(city_visit)
    print('Elapsed time %s' % (datetime.datetime.now() - start))
