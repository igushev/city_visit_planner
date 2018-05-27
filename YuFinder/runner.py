import datetime
import os

from YuConfig import config as config_


class CityVisitFinderRunner(object):
  
  def __init__(self):
    config = config_.GetConfig(os.path.join('YuConfig', 'runner.config'))
    database_connection = config_.GetDatabaseConnection(config)
    self.city_visit_finder = config_.GetCityVisitFinder(config, database_connection)
    self.city_visit_accumulator_generator = config_.GetCityVisitAccumulatorGenerator(config)

  def Run(self, city_visit_parameters):
    start = datetime.datetime.now()

    city_visit = self.city_visit_finder.FindCityVisit(city_visit_parameters, self.city_visit_accumulator_generator)

    print('Input points: %s' %
          ', '.join(point.name for point in
                    self.city_visit_finder.database_connection.GetPoints(city_visit_parameters.visit_location)))
    print('Your schedule:')
    print(city_visit)
    print('Elapsed time %s' % (datetime.datetime.now() - start))
