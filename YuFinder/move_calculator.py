# NOTE(igushev): Source http://www.movable-type.co.uk/scripts/latlong.html
# (Bearing)
import math

import Yusi
from Yusi.YuFinder.city_visit import MoveType, MoveDescription


R = 3959  # Earth radius in miles.
WALKING_SPEED = 2.  # Walking speed in mph.
# Speed of car in traffic jams or public transportation in mph.
DRIVING_SPEED = 25.
# 15 minutes to call a taxi, to find and than park a car, to buy a ticket and
# wait in case of public transportation.
BREAK_BEFORE_DRIVING = 0.25
# Minimum distance which can be set as max_walking_distance, since driving less
# would cause driving taking more time than walking.

# TODO(igushev): Form and encapsulate statements for Smart* classes as
# separate class, change Smart to another name.
MAX_WALKING_DISTANCE_MIN = (
    DRIVING_SPEED * BREAK_BEFORE_DRIVING * WALKING_SPEED /
    (DRIVING_SPEED - WALKING_SPEED))
# Multiplier which penalize driving against walking
DRIVING_COST_MULT = 10.
assert DRIVING_COST_MULT < DRIVING_SPEED / WALKING_SPEED
# Maximum distance which can set as max_walking_distance, since walking more
# would cause not increasingly monotonic function of cost.
MAX_WALKING_DISTANCE_MAX = (
    DRIVING_SPEED * BREAK_BEFORE_DRIVING * WALKING_SPEED /
    ((DRIVING_SPEED / DRIVING_COST_MULT) - WALKING_SPEED))



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


class MoveCalculator(object):
  """Abstract class which calculates move_description."""
  
  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    raise NotImplemented()

class WalkingMoveCalculator(MoveCalculator):
  """Calculates move_description to walk."""

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    return MoveDescription(d / WALKING_SPEED, MoveType.walking)


class DrivingMoveCalculator(MoveCalculator):
  """Calculates move_description to drive."""

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    return MoveDescription(d / DRIVING_SPEED, MoveType.driving)


class BreakDrivingMoveCalculator(MoveCalculator):
  """Calculates move_description to drive considering break before driving."""

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    return MoveDescription(
        (d / DRIVING_SPEED) + BREAK_BEFORE_DRIVING, MoveType.driving)


class SmartMoveCalculator(MoveCalculator):
  """Calculates move_description to either work or drive."""

  def __init__(self, max_walking_distance=None,
               validate_max_walking_distance=True):
    if max_walking_distance is not None:
      self.max_walking_distance = max_walking_distance
    else:
      self.max_walking_distance = MAX_WALKING_DISTANCE_MIN
    if validate_max_walking_distance:
      assert self.max_walking_distance >= MAX_WALKING_DISTANCE_MIN
      assert self.max_walking_distance <= MAX_WALKING_DISTANCE_MAX

  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    d = CalculateDistance(coordinates_from, coordinates_to)
    d = d * math.sqrt(2)  # Because most cities have grid streets.
    if d < self.max_walking_distance:
      return MoveDescription(d / WALKING_SPEED, MoveType.walking)
    else:
      return MoveDescription(
          (d / DRIVING_SPEED) + BREAK_BEFORE_DRIVING, MoveType.driving)
