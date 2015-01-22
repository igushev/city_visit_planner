import datetime
import os

import Yusi
from Yusi.YuFinder.city_visit import DayVisitParameters
from Yusi.YuFinder import point
from Yusi.YuFinder import read_csv
from Yusi.YuFinder.prototype_parameters import PrototypeParameters


class CityVisitFinderRunner(object):
  
  def __init__(self):
    points = read_csv.ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
    san_francisco_coordinates = point.Coordinates(37.7833, -122.4167)
    
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
    
    day_visit_parameters_dec6_13to18 = GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 12, 6, 13, 0, 0),
        end_datetime=datetime.datetime(2014, 12, 6, 18, 0, 0))
    
    day_visit_parameters_dec7_13to18 = GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 12, 6, 13, 0, 0),
        end_datetime=datetime.datetime(2014, 12, 6, 18, 0, 0))
    
    self.points_to_visit = [points['Legion of Honor'],
              points['Palace of Fine Arts'],
              points['Ferry Biulding'],
              points['Lombard Street'],
              points['Almo Square'],
              points['Golden Gate Bridge']]
    
    day_visit_parameterss = [
        day_visit_parameters_dec6_13to18, day_visit_parameters_dec7_13to18]
    
    self.max_walking_distance=1.0
    
    city_visit_finder = (
        PrototypeParameters(max_walking_distance=self.max_walking_distance).
        CityVisitFinder())
    
    self.city_visit = city_visit_finder.FindCityVisit(
        self.points_to_visit, day_visit_parameterss)


def main():
  runner = CityVisitFinderRunner()
  print('Points to visit in priority: %s' %
        ', '.join(point.name for point in runner.points_to_visit))
  print('Maximum walking distance: %d mile(s)' % runner.max_walking_distance)
  print('Your schedule:')
  print(runner.city_visit)


if __name__ == '__main__':
  main()