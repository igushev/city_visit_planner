from configparser import ConfigParser

from data import city_visit
from data import test_util as point_test_util
from finder import city_visit_finder as city_visit_finder_
from ranker import age_group_rank_adjuster
from ranker import point_type_rank_adjuster
from ranker import points_ranker as points_ranker_
from ranker import popularity_rank_adjuster
from router import point_fit as point_fit_
from router import cost_accumulator
from router import move_calculator
from router import day_visit_cost_calculator
from router import multi_day_visit_cost_calculator
from router import day_visit_router as day_visit_router_
from router import city_visit_points_left
from router import points_queue
from router import city_visit_router as city_visit_router_
from router import city_visit_accumulator


def GetConfig(filepath=None):
  config = ConfigParser()
  if filepath:
    config.read(filepath)
  return config


def GetDatabaseConnection(config):
  database_connection = point_test_util.MockDatabaseConnection()
  return database_connection


def GetPointsRanker(config):
  rank_adjusters = [popularity_rank_adjuster.PopularityRankAdjuster(),
                    point_type_rank_adjuster.PointTypeRankAdjuster(),
                    age_group_rank_adjuster.AgeGroupRankAdjuster()]
  
  points_ranker = points_ranker_.PointsRanker(rank_adjusters)
  return points_ranker


def GetPointFit(config):
  point_fit = point_fit_.SimplePointFit()
  return point_fit


def GetCostAccumulatorGenerator(config):
  cag_section = 'cost_accumulator_generator'
  
  point_visit_factor = config.getfloat(cag_section, 'point_visit_factor')
  move_walking_factor = config.getfloat(cag_section, 'move_walking_factor')
  move_driving_factor = config.getfloat(cag_section, 'move_driving_factor')
  move_ptt_factor = config.getfloat(cag_section, 'move_ptt_factor')
  lunch_factor = config.getfloat(cag_section, 'lunch_factor')
  no_point_visit_factor = config.getfloat(cag_section, 'no_point_visit_factor')
  no_point_visit_const = config.getfloat(cag_section, 'no_point_visit_const')
  unused_time_factor = config.getfloat(cag_section, 'unused_time_factor')
  
  cost_accumulator_generator = cost_accumulator.FactorCostAccumulatorGenerator(
      point_visit_factor=point_visit_factor,
      move_walking_factor=move_walking_factor,
      move_driving_factor=move_driving_factor,
      move_ptt_factor=move_ptt_factor,
      lunch_factor=lunch_factor,
      no_point_visit_factor=no_point_visit_factor,
      no_point_visit_const=no_point_visit_const,
      unused_time_factor=unused_time_factor)
  
  return cost_accumulator_generator

  
def GetDayVisitCostCalculatorGenerator(config, point_fit, cost_accumulator_generator):
  dvccg_section = 'day_visit_const_calculator_generator'
  
  if (config.has_option(dvccg_section, 'driving_speed') or
      config.has_option(dvccg_section, 'pause_before_driving')):
    assert (config.has_option(dvccg_section, 'driving_speed') and
            config.has_option(dvccg_section, 'pause_before_driving')), (
               'driving_speed and pause_before_driving should both either'
               ' present or absent')
    driving = True
    driving_speed = config.getfloat(dvccg_section, 'driving_speed')
    pause_before_driving = (
        config.getfloat(dvccg_section, 'pause_before_driving'))
  else:
    driving = False

  walking_speed = config.getfloat(dvccg_section, 'walking_speed')
  pause_before_walking = config.getfloat(dvccg_section, 'pause_before_walking')
  ptt_speed = config.getfloat(dvccg_section, 'ptt_speed')
  pause_before_ptt = config.getfloat(dvccg_section, 'pause_before_ptt')
  ptt_cost_mult = config.getfloat(dvccg_section, 'ptt_cost_mult')
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
  if config.has_option(dvccg_section, 'max_walking_distance'):
    max_walking_distance = config.getfloat(dvccg_section, 'max_walking_distance')
  else:
    max_walking_distance = min_max_walking_distance_before_ptt

  validate_max_walking_distance = config.getboolean(dvccg_section, 'validate_max_walking_distance')
  if validate_max_walking_distance:
    assert max_walking_distance >= min_max_walking_distance_before_ptt
    assert max_walking_distance <= max_max_walking_distance_before_ptt

  if driving:
    driving_move_calculator = move_calculator.SimpleMoveCalculator(
        driving_speed, city_visit.MoveType.driving, pause=pause_before_driving)

  walking_move_calculator = move_calculator.SimpleMoveCalculator(
      walking_speed, city_visit.MoveType.walking, pause=pause_before_walking)
  ptt_move_calculator = move_calculator.SimpleMoveCalculator(
      ptt_speed, city_visit.MoveType.ptt, pause=pause_before_ptt)

  walking_ptt_move_calculator = move_calculator.MultiMoveCalculator(
          [max_walking_distance],
          [walking_move_calculator, ptt_move_calculator])

  if driving:
    driving_day_visit_const_calculator_generator = (
        day_visit_cost_calculator.DayVisitCostCalculatorGenerator(
            move_calculator=driving_move_calculator,
            point_fit=point_fit,
            cost_accumulator_generator=cost_accumulator_generator))

  ptt_day_visit_const_calculator_generator = day_visit_cost_calculator.DayVisitCostCalculatorGenerator(
      move_calculator=walking_ptt_move_calculator,
      point_fit=point_fit,
      cost_accumulator_generator=cost_accumulator_generator)

  if driving:
    day_visit_const_calculator_generator = (
        multi_day_visit_cost_calculator.MultiDayVisitCostCalculatorGenerator(
            [driving_day_visit_const_calculator_generator,
             ptt_day_visit_const_calculator_generator]))
  else:
    day_visit_const_calculator_generator = (
        ptt_day_visit_const_calculator_generator)

  return day_visit_const_calculator_generator


def GetPointsQueueGenerator(config):
  points_queue_generator = points_queue.OneByOnePointsQueueGenerator()
  return points_queue_generator


def GetCityVisitRouter(config):
  cvr_section = 'city_visit_router'

  point_fit = GetPointFit(config)
  cost_accumulator_generator = GetCostAccumulatorGenerator(config)
  day_visit_const_calculator_generator = (
      GetDayVisitCostCalculatorGenerator(
          config,
          point_fit=point_fit,
          cost_accumulator_generator=cost_accumulator_generator))

  day_visit_heap_size = config.getint(cvr_section, 'day_visit_heap_size')
  day_visit_router = day_visit_router_.DayVisitRouter(
      calculator_generator=day_visit_const_calculator_generator,
      day_visit_heap_size=day_visit_heap_size)

  city_visit_points_left_generator = city_visit_points_left.CityVisitPointsLeftGenerator(
      cost_accumulator_generator=cost_accumulator_generator)
  points_queue_generator = GetPointsQueueGenerator(config)
  shard_num_days = config.getint(cvr_section, 'shard_num_days') 
  max_depth = config.getint(cvr_section, 'max_depth') 
  city_visit_heap_size = config.getint(cvr_section, 'city_visit_heap_size')
  max_non_pushed_points = config.getint(cvr_section, 'max_non_pushed_points')
  if config.has_option(cvr_section, 'num_processes'):
    num_processes = config.getint(cvr_section, 'num_processes')
  else:
    num_processes = None

  city_visit_router = city_visit_router_.CityVisitRouter(
      day_visit_router=day_visit_router,
      city_visit_points_left_generator=city_visit_points_left_generator,
      points_queue_generator=points_queue_generator,
      shard_num_days=shard_num_days,
      max_depth=max_depth,
      city_visit_heap_size=city_visit_heap_size,
      max_non_pushed_points=max_non_pushed_points,
      num_processes=num_processes)

  return city_visit_router


def GetCityVisitFinder(config, database_connection):
  points_ranker = GetPointsRanker(config)
  city_visit_router = GetCityVisitRouter(config)
  city_visit_finder = city_visit_finder_.CityVisitFinder(
      database_connection=database_connection,
      points_ranker=points_ranker,
      city_visit_router=city_visit_router)
  return city_visit_finder


def GetCityVisitAccumulatorGenerator(config):
  city_visit_accumulator_generator = city_visit_accumulator.CityVisitAccumulatorGenerator()
  return city_visit_accumulator_generator
