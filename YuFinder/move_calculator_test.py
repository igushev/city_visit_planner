import unittest

import Yusi
from Yusi.YuFinder.move_calculator import WalkingMoveCalculator, DrivingMoveCalculator, PauseAndDrivingMoveCalculator, PauseAndPTTOrWalkingMoveCalculator,\
  WALKING_SPEED, DRIVING_SPEED, PAUSE_BEFORE_DRIVING, MIN_MAX_WALKING_DISTANCE_BEFORE_PTT,\
  PTT_SPEED, PAUSE_BEFORE_PTT
from Yusi.YuFinder.point import Coordinates
from Yusi.YuFinder.city_visit import MoveType


# Ferry Biulding, San Francisco.
ferry_biulding_coordinates = Coordinates(37.7955, -122.3937)
# Pier 39, San Francisco.
pier_39_coordinates = Coordinates(37.8100, -122.4104)
# Place near Pier 39, San Francisco.
near_pier_39_coordinates = Coordinates(37.8097, -122.4104)

fb_to_p39_walking = 1.916 / WALKING_SPEED
fb_to_np39_walking = 1.894 / WALKING_SPEED
p39_to_np39_walking = 0.029 / WALKING_SPEED

fb_to_p39_driving = 1.916 / DRIVING_SPEED
fb_to_np39_driving = 1.894 / DRIVING_SPEED
p39_to_np39_driving = 0.029 / DRIVING_SPEED

fb_to_p39_ptt = 1.916 / PTT_SPEED
fb_to_np39_ptt = 1.894 / PTT_SPEED
p39_to_np39_ptt = 0.029 / PTT_SPEED

fb_to_p39_pause_and_driving = fb_to_p39_driving + PAUSE_BEFORE_DRIVING
fb_to_np39_pause_and_driving = fb_to_np39_driving + PAUSE_BEFORE_DRIVING
p39_to_np39_pause_and_driving = p39_to_np39_driving + PAUSE_BEFORE_DRIVING

fb_to_p39_pause_and_ptt = fb_to_p39_ptt + PAUSE_BEFORE_PTT
fb_to_np39_pause_and_ptt = fb_to_np39_ptt + PAUSE_BEFORE_PTT
p39_to_np39_pause_and_ptt = p39_to_np39_ptt + PAUSE_BEFORE_PTT

              
class WalkingMoveCalculatorTest(unittest.TestCase):

  def testCalculateMoveDescriptionGeneral(self):
    move_calculator = WalkingMoveCalculator()
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)


class DrivingMoveCalculatorTest(unittest.TestCase):

  def testCalculateMoveDescriptionGeneral(self):
    move_calculator = DrivingMoveCalculator()
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)


class PauseAndDrivingMoveCalculatorTest(unittest.TestCase):

  def testCalculateMoveDescriptionGeneral(self):
    move_calculator = PauseAndDrivingMoveCalculator()
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_pause_and_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_pause_and_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_pause_and_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)


class PauseAndPTTOrWalkingMoveCalculatorTest(unittest.TestCase):
  
  def testCalculateMoveDescriptionGeneral(self):
    move_calculator = PauseAndPTTOrWalkingMoveCalculator()
    self.assertAlmostEqual(
        MIN_MAX_WALKING_DISTANCE_BEFORE_PTT,
        move_calculator.max_walking_distance, places=3)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
  
  def testCalculateMoveDescriptionWalkingOnly(self):
    move_calculator = PauseAndPTTOrWalkingMoveCalculator(
        max_walking_distance=2.0, validate_max_walking_distance=False)
    self.assertAlmostEqual(
        2.0, move_calculator.max_walking_distance, places=3)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
  
  def testCalculateMoveDescriptionPTTOnly(self):
    move_calculator = PauseAndPTTOrWalkingMoveCalculator(
        max_walking_distance=0.02, validate_max_walking_distance=False)
    self.assertAlmostEqual(
        0.02, move_calculator.max_walking_distance, places=3)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_pause_and_ptt,
        move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_pause_and_ptt,
        move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)


if __name__ == '__main__':
    unittest.main()

