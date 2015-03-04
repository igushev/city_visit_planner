import datetime
import os

import Yusi
from Yusi.YuRouter.prototype_parameters import PrototypeParameters
from Yusi.YuPoint.city_visit import DayVisitParameters
from Yusi.YuPoint.read_csv import ReadCSVToDict


def GetPointsInput():
  points = ReadCSVToDict(
      os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
  return [
      points['De Young Museum'],
      points['Cable Car Museum'],
      points['Baker Beach'],
      points['Sutro Baths'],
      points['Presidio'],
      points['Ferry Building'],
      points['Lombard Street'],
      points['Alamo Square'],
      points['Twin Peaks'],
      points['Golden Gate Bridge'],
      points['Golden Gate Park']]


def GetDayVisitParameterss():
  points = ReadCSVToDict(
      os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))

  def GetDayVisitParameters(start_datetime, end_datetime):
    return DayVisitParameters(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        lunch_start_datetime=datetime.datetime(
            start_datetime.year, start_datetime.month, start_datetime.day,
            15, 0, 0),
        lunch_hours=1.,
        start_coordinates=points['Union Square'].coordinates_starts,
        end_coordinates=points['Union Square'].coordinates_ends)

  return [
      GetDayVisitParameters(
          start_datetime=datetime.datetime(2015, 2, day, 13, 0, 0),
          end_datetime=datetime.datetime(2015, 2, day, 19, 0, 0))
      for day in range(1, 4)]


class CityVisitRouterRunner(object):
  
  def __init__(self):
    self.max_walking_distance=1.0
    self.city_visit_router = (
        PrototypeParameters(max_walking_distance=self.max_walking_distance).
        CityVisitRouter())

  def Run(self, points_input, day_visit_parameterss):
    return self.city_visit_router.RouteCityVisit(
        points_input, day_visit_parameterss)


def main():
  start = datetime.datetime.now()
  
  points_input = GetPointsInput()
  day_visit_parameterss = GetDayVisitParameterss()
  city_visit_router_runner = CityVisitRouterRunner()
  city_visit_best, points_left = city_visit_router_runner.Run(
      points_input, day_visit_parameterss)

  print('Points to visit in priority: %s' %
        ', '.join(point.name for point in points_input))
  print('Maximum walking distance: %d mile(s)' %
        city_visit_router_runner.max_walking_distance)
  print('Your schedule:')
  print(city_visit_best)
  print('Points left: %s' %
        ', '.join(point_left.name for point_left in points_left))

  print('Elapsed time %s' % (datetime.datetime.now() - start))


if __name__ == '__main__':
  main()
