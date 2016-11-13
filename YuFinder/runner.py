import datetime
import os

import Yusi
from Yusi.YuConfig.config import GetConfig, GetCityVisitFinder,\
  GetCityVisitAccumulatorGenerator


class CityVisitFinderRunner(object):
  
  def __init__(self):
    config = (
        GetConfig(os.path.join(
            Yusi.GetYusiDir(), 'YuConfig', 'prototype.config')))
    self.city_visit_finder = GetCityVisitFinder(config)
    self.city_visit_accumulator_generator = (
        GetCityVisitAccumulatorGenerator(config))

  def Run(self, city_visit_parameters):
    start = datetime.datetime.now()

    city_visit = self.city_visit_finder.FindCityVisit(
        city_visit_parameters, self.city_visit_accumulator_generator)

    print('Input points: %s' %
          ', '.join(point.name
                    for point in
                    self.city_visit_finder.database_connection.GetPoints(
                        city_visit_parameters.visit_location)))
    print('Your schedule:')
    print(city_visit)
    print('Elapsed time %s' % (datetime.datetime.now() - start))
