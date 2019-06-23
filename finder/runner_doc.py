import os
from config import config as config_
config = config_.GetConfig(os.path.join('config', 'runner.config'))

import datetime
from data import city_visit
from data import point

start_end_coordinates = point.Coordinates(40.763582, -73.988470)

day1 = city_visit.DayVisitParameters(
    start_datetime=datetime.datetime(2019, 7, 1, 10, 0, 0),
    end_datetime=datetime.datetime(2019, 7, 1, 19, 0, 0),
    lunch_start_datetime=datetime.datetime(2019, 7, 1, 14, 0, 0),
    lunch_hours=1.,
    start_coordinates=start_end_coordinates,
    end_coordinates=start_end_coordinates)

day2 = city_visit.DayVisitParameters(
    start_datetime=datetime.datetime(2019, 7, 2, 10, 0, 0),
    end_datetime=datetime.datetime(2019, 7, 2, 17, 0, 0),
    lunch_start_datetime=datetime.datetime(2019, 7, 1, 14, 0, 0),
    lunch_hours=1.,
    start_coordinates=start_end_coordinates,
    end_coordinates=start_end_coordinates)

from data import city_visit
from data import point

visit_location = city_visit.VisitLocation('New York City')

parameters_point_types = point.PointType(
  city_tours=90,
  landmarks=90,
  nature=10,
  museums=10,
  shopping=50,
  dining=50)

parameters_age_groups = point.AgeGroup(
  senior=None,
  adult=90,
  junior=None,
  child=None,
  toddlers=10)

city_visit_parameters = city_visit.CityVisitParameters(
  visit_location=visit_location,
  day_visit_parameterss=[day1, day2],
  point_type=parameters_point_types,
  age_group=parameters_age_groups)

from data import test_util as point_test_util
points_input = list(point_test_util.GetPointsInput('data', 'test_nyc_1.csv').values())

from config import config as config_
city_visit_finder = config_.GetCityVisitFinder(config)
city_visit_accumulator_generator = config_.GetCityVisitAccumulatorGenerator(config)
city_visit = city_visit_finder.FindCityVisit(points_input, city_visit_parameters, city_visit_accumulator_generator)

print('Your schedule:')
print(city_visit)
