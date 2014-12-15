import datetime
import os

import Yusi
from Yusi.YuFinder.city_visit import DayVisitParameters
from Yusi.YuFinder.cost_accumulator import SmartCostAccumulatorGenerator
from Yusi.YuFinder.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuFinder.day_visit_finder import FindDayVisit
from Yusi.YuFinder.move_calculator import SmartMoveCalculator
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder import point
from Yusi.YuFinder import read_csv
from Yusi.YuFinder.city_visit_finder import FindCityVisit


points = read_csv.ReadCSVToDict(
    os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
san_francisco_coordinates = point.Coordinates(37.7833, -122.4167)
move_calculator = SmartMoveCalculator(1)
point_fit = SimplePointFit()
cost_accumulator_generator=SmartCostAccumulatorGenerator()


def GetDayVisitCostCalculatorGenerator(start_datetime, end_datetime):
  day_visit_parameters = DayVisitParameters(
      start_datetime=start_datetime,
      end_datetime=end_datetime,
      lunch_start_datetime=datetime.datetime(
          start_datetime.year, start_datetime.month, start_datetime.day,
          15, 0, 0),
      lunch_hours=1.,
      start_coordinates=points['Union Square'].coordinates_starts,
      end_coordinates=points['Union Square'].coordinates_ends)
  return DayVisitCostCalculatorGenerator(
      move_calculator=move_calculator,
      point_fit=point_fit,
      day_visit_parameters=day_visit_parameters,
      cost_accumulator_generator=cost_accumulator_generator)


calculator_generator_dec6_13to18 = GetDayVisitCostCalculatorGenerator(
    start_datetime=datetime.datetime(2014, 12, 6, 13, 0, 0),
    end_datetime=datetime.datetime(2014, 12, 6, 18, 0, 0))

calculator_generator_dec7_13to18 = GetDayVisitCostCalculatorGenerator(
    start_datetime=datetime.datetime(2014, 12, 6, 13, 0, 0),
    end_datetime=datetime.datetime(2014, 12, 6, 18, 0, 0))


points_to_visit = [points['Legion of Honor'],
          points['Palace of Fine Arts'],
          points['Ferry Biulding'],
          points['Lombard Street'],
          points['Almo Square'],
          points['Golden Gate Bridge']]


calculator_generators = [
    calculator_generator_dec6_13to18, calculator_generator_dec7_13to18]


city_visit = FindCityVisit(points_to_visit, calculator_generators)


print('Points to visit in priority: %s' %
      ', '.join(point.name for point in points_to_visit))
print('Maximum walking distance: %d mile(s)' % move_calculator.max_walking_distance)
print('Your schedule:')
print(city_visit)
