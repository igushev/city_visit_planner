import Yusi
from Yusi.YuRouter.cost_accumulator import FactorCostAccumulatorGenerator
from Yusi.YuRouter.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuRouter.day_visit_router import DayVisitRouter
from Yusi.YuRouter.move_calculator import SimpleMoveCalculator, MultiMoveCalculator
from Yusi.YuRouter.point_fit import SimplePointFit
from Yusi.YuRouter.city_visit_router import CityVisitRouter
from Yusi.YuRouter.multi_day_visit_cost_calculator import MultiDayVisitCostCalculatorGenerator
from Yusi.YuRouter.city_visit_points_left import CityVisitPointsLeftGenerator
from Yusi.YuRouter.points_queue import OneByOnePointsQueueGenerator
from Yusi.YuPoint.city_visit import MoveType
from Yusi.YuRouter.city_visit_accumulator import CityVisitAccumulatorGenerator


class PrototypeParameters(object):
  
  def __init__(self, max_walking_distance=None,
               validate_max_walking_distance=True):

    walking_speed = 2.  # Walking speed in mph.
    
    driving_speed = 20.  # Speed of car in traffic jams in mph.
    # 10 minutes to find and than park a car and 10 minutes to find a parking
    # spot when arrived. 
    pause_before_driving = 0.30
    
    ptt_speed = 15.  # Speed of Public Transportation or Taxi in mph.
    # 15 minutes to buy a ticket and wait in case of public transportation or
    # call a taxi.
    pause_before_ptt = 0.25
    
    # Multiplier which penalize PTT against walking.
    ptt_cost_mult = 7.49
    assert ptt_cost_mult < ptt_speed / walking_speed
    # Minimum distance which can be set as max_walking_distance, since using
    # PTT less would cause PTT taking more time than walking.
    min_max_walking_distance_before_ptt = (
        ptt_speed * pause_before_ptt * walking_speed /
        (ptt_speed - walking_speed))
    # Maximum distance which can set as max_walking_distance, since walking
    # more would cause not increasingly monotonic function of cost.
    max_max_walking_distance_before_ptt = (
        ptt_speed * pause_before_ptt * walking_speed /
        ((ptt_speed / ptt_cost_mult) - walking_speed))
    
    if max_walking_distance is None:
      max_walking_distance = min_max_walking_distance_before_ptt

    if validate_max_walking_distance:
      assert max_walking_distance >= min_max_walking_distance_before_ptt
      assert max_walking_distance <= max_max_walking_distance_before_ptt

    point_visit_factor=0.
    move_walking_factor=1.
    move_driving_factor=ptt_cost_mult
    move_ptt_factor=ptt_cost_mult
    lunch_factor=0.
    no_point_visit_factor = 0.
    no_point_visit_const = 1000.
    unused_time_factor = 0.01
    
    driving_move_calculator = SimpleMoveCalculator(
        driving_speed, MoveType.driving, pause=pause_before_driving)

    walking_move_calculator = SimpleMoveCalculator(
        walking_speed, MoveType.walking)

    ptt_move_calculator = SimpleMoveCalculator(
        ptt_speed, MoveType.ptt, pause=pause_before_ptt)

    walking_ptt_move_calculator = MultiMoveCalculator(
            [max_walking_distance],
            [walking_move_calculator, ptt_move_calculator])

    point_fit = SimplePointFit()

    cost_accumulator_generator=FactorCostAccumulatorGenerator(
        point_visit_factor=point_visit_factor,
        move_walking_factor=move_walking_factor,
        move_driving_factor=move_driving_factor,
        move_ptt_factor=move_ptt_factor,
        lunch_factor=lunch_factor,
        no_point_visit_factor=no_point_visit_factor,
        no_point_visit_const=no_point_visit_const,
        unused_time_factor=unused_time_factor)

#     driving_day_visit_const_calculator_generator = (
#         DayVisitCostCalculatorGenerator(
#             move_calculator=driving_move_calculator,
#             point_fit=point_fit,
#             cost_accumulator_generator=cost_accumulator_generator))

    ptt_day_visit_const_calculator_generator = DayVisitCostCalculatorGenerator(
        move_calculator=walking_ptt_move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=cost_accumulator_generator)

#     day_visit_const_calculator_generator = MultiDayVisitCostCalculatorGenerator(
#         [driving_day_visit_const_calculator_generator,
#          ptt_day_visit_const_calculator_generator])

    day_visit_heap_size = 1000

    day_visit_router = DayVisitRouter(
        calculator_generator=ptt_day_visit_const_calculator_generator,
        day_visit_heap_size=day_visit_heap_size)

    city_visit_points_left_generator = CityVisitPointsLeftGenerator(
        cost_accumulator_generator=cost_accumulator_generator)

    city_visit_accumulator_generator = CityVisitAccumulatorGenerator()

    points_queue_generator = OneByOnePointsQueueGenerator()

    shard_num_days = 2
    max_depth = 1
    city_visit_heap_size = 10
    max_non_pushed_points = 5

    self.city_visit_router = CityVisitRouter(
        day_visit_router=day_visit_router,
        city_visit_points_left_generator=city_visit_points_left_generator,
        city_visit_accumulator_generator=city_visit_accumulator_generator,
        points_queue_generator=points_queue_generator,
        shard_num_days=shard_num_days,
        max_depth=max_depth,
        city_visit_heap_size=city_visit_heap_size,
        max_non_pushed_points=max_non_pushed_points,
        num_processes=None)

  def CityVisitRouter(self):
    return self.city_visit_router
