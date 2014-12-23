import datetime
import os

import Yusi
from Yusi.YuFinder.city_visit import DayVisitParameters
from Yusi.YuFinder.cost_accumulator import MoreWalkingCostAccumulatorGenerator
from Yusi.YuFinder.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuFinder.day_visit_finder import FindDayVisit
from Yusi.YuFinder.move_calculator import PauseAndPTTOrWalkingMoveCalculator,\
  WalkingMoveCalculator, PauseAndDrivingMoveCalculator
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder import point
from Yusi.YuFinder import read_csv
from Yusi.YuFinder.city_visit_finder import FindCityVisit
from Yusi.YuFinder.multi_day_visit_cost_calculator import MultiDayVisitCostCalculatorGenerator


points = read_csv.ReadCSVToDict(
    os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))
san_francisco_coordinates = point.Coordinates(37.7833, -122.4167)
driving_move_calculator = PauseAndDrivingMoveCalculator()
ptt_move_calculator = PauseAndPTTOrWalkingMoveCalculator(1)
point_fit = SimplePointFit()
cost_accumulator_generator=MoreWalkingCostAccumulatorGenerator()
driving_day_visit_const_calculator_generator = DayVisitCostCalculatorGenerator(
    move_calculator=driving_move_calculator,
    point_fit=point_fit,
    cost_accumulator_generator=cost_accumulator_generator)
ptt_day_visit_const_calculator_generator = DayVisitCostCalculatorGenerator(
    move_calculator=ptt_move_calculator,
    point_fit=point_fit,
    cost_accumulator_generator=cost_accumulator_generator)
day_visit_const_calculator_generator = MultiDayVisitCostCalculatorGenerator(
    [driving_day_visit_const_calculator_generator,
     ptt_day_visit_const_calculator_generator])


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


points_to_visit = [points['Legion of Honor'],
          points['Palace of Fine Arts'],
          points['Ferry Biulding'],
          points['Lombard Street'],
          points['Almo Square'],
          points['Golden Gate Bridge']]


day_visit_parameterss = [
    day_visit_parameters_dec6_13to18, day_visit_parameters_dec7_13to18]


city_visit = FindCityVisit(points_to_visit, day_visit_parameterss, day_visit_const_calculator_generator)


print('Points to visit in priority: %s' %
      ', '.join(point.name for point in points_to_visit))
print('Maximum walking distance: %d mile(s)' % ptt_move_calculator.max_walking_distance)
print('Your schedule:')
print(city_visit)
