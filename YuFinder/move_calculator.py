# NOTE(igushev): Source http://www.movable-type.co.uk/scripts/latlong.html
# (Bearing)
import math

import Yusi
from Yusi.YuFinder.city_visit import MoveType, MoveDescription


R = 3959  # Earth radius in miles.
WALKING_SPEED = 2.  # Walking speed in mph.
# Speed of car in traffic jams in mph.
DRIVING_SPEED = 25.
# 10 minutes to find and than park a car and 10 minutes to find a parking spot
# when arrived. 
PAUSE_BEFORE_DRIVING = 0.25
# Speed of Public Transportation or Taxi in mph.
PTT_SPEED = 25.
# 15 minutes to buy a ticket and wait in case of public transportation or call
# a taxi.
PAUSE_BEFORE_PTT = 0.25

# TODO(igushev): Form and encapsulate statements for Smart* classes as
# separate class, change Smart to another name.
# Multiplier which penalize PTT against walking.
PTT_COST_MULT = 10.
assert PTT_COST_MULT < PTT_SPEED / WALKING_SPEED
# Minimum distance which can be set as max_walking_distance, since using PTT
# less would cause PTT taking more time than walking.
MIN_MAX_WALKING_DISTANCE_BEFORE_PTT = (
    PTT_SPEED * PAUSE_BEFORE_PTT * WALKING_SPEED /
    (PTT_SPEED - WALKING_SPEED))
# Maximum distance which can set as max_walking_distance, since walking more
# would cause not increasingly monotonic function of cost.
MAX_MAX_WALKING_DISTANCE_BEFORE_PTT = (
    PTT_SPEED * PAUSE_BEFORE_PTT * WALKING_SPEED /
    ((PTT_SPEED / PTT_COST_MULT) - WALKING_SPEED))



def CalculateDistance(coordinates_from, coordinates_to):
  """Calculates distance in km/miles."""
  lat_1 = math.radians(coordinates_from.latitude)
  lat_2 = math.radians(coordinates_to.latitude)
  delta_lat = math.radians(coordinates_to.latitude - coordinates_from.latitude)
  long_1 = math.radians(coordinates_from.longitude)
  long_2 = math.radians(coordinates_to.longitude)
  delta_long = math.radians(
      coordinates_to.longitude - coordinates_from.longitude)

  a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
       math.cos(lat_1) * math.cos(lat_2) *
       math.sin(delta_long/2) * math.sin(delta_long/2))
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c
  return d


class MoveCalculatorInterface(object):
  """Abstract class which calculates move_description."""
  
  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    raise NotImplemented()


class WalkingMoveCalculator(MoveCalculatorInterface):
  """Calculates move_description to walk."""

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    return MoveDescription(d / WALKING_SPEED, MoveType.walking)


class DrivingMoveCalculator(MoveCalculatorInterface):
  """Calculates move_description to drive."""

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    return MoveDescription(d / DRIVING_SPEED, MoveType.driving)


class PauseAndDrivingMoveCalculator(MoveCalculatorInterface):
  """Calculates move_description to drive considering pause before driving."""

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    return MoveDescription(
        (d / DRIVING_SPEED) + PAUSE_BEFORE_DRIVING, MoveType.driving)


class PauseAndPTTOrWalkingMoveCalculator(MoveCalculatorInterface):
  """Calculates move_description to either work or use PTT."""

  def __init__(self, max_walking_distance=None,
               validate_max_walking_distance=True):
    if max_walking_distance is not None:
      self.max_walking_distance = max_walking_distance
    else:
      self.max_walking_distance = MIN_MAX_WALKING_DISTANCE_BEFORE_PTT
    if validate_max_walking_distance:
      assert self.max_walking_distance >= MIN_MAX_WALKING_DISTANCE_BEFORE_PTT
      assert self.max_walking_distance <= MAX_MAX_WALKING_DISTANCE_BEFORE_PTT

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    if d < self.max_walking_distance:
      return MoveDescription(d / WALKING_SPEED, MoveType.walking)
    else:
      return MoveDescription(
          (d / PTT_SPEED) + PAUSE_BEFORE_PTT, MoveType.ptt)
