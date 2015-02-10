import datetime
import os

import Yusi
from Yusi.YuFinder.city_visit import DayVisitParameters
from Yusi.YuFinder.prototype_parameters import PrototypeParameters
from Yusi.YuFinder.point import Coordinates
from Yusi.YuFinder.read_csv import ReadCSVToDict


class Runner(object):
  
  def __init__(self):
    points = ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    san_francisco_coordinates = Coordinates(37.7833, -122.4167)
    
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
    
    self.points_to_visit = [
              points['De Young Museum'],
              points['Cable Car Museum'],
              points['Baker Beach'],
              points['Sutro Baths'],
              points['Presidio'],
              points['Ferry Biulding'],
              points['Lombard Street'],
              points['Almo Square'],
              points['Twin Peaks'],
              points['Golden Gate Bridge'],
              points['Golden Gate Park']]
    
    day_visit_parameterss = [
        GetDayVisitParameters(
            start_datetime=datetime.datetime(2015, 2, day, 13, 0, 0),
            end_datetime=datetime.datetime(2015, 2, day, 19, 0, 0))
        for day in range(1, 4)]

    
    self.max_walking_distance=1.0
    
    city_visit_finder = (
        PrototypeParameters(max_walking_distance=self.max_walking_distance).
        CityVisitFinder())
    
    self.city_visit_best, self.points_left = city_visit_finder.FindCityVisit(
        self.points_to_visit, day_visit_parameterss)


def main():
  start = datetime.datetime.now()
  runner = Runner()
  print('Points to visit in priority: %s' %
        ', '.join(point.name for point in runner.points_to_visit))
  print('Maximum walking distance: %d mile(s)' % runner.max_walking_distance)
  print('Your schedule:')
  print(runner.city_visit_best)
  print('Points left: %s' %
        ', '.join(point_left.name for point_left in runner.points_left))
  print('Elapsed time %s' % (datetime.datetime.now() - start))


if __name__ == '__main__':
  main()