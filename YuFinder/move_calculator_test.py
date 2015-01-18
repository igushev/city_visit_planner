import unittest

import Yusi
from Yusi.YuFinder.move_calculator import SimpleMoveCalculator,\
  MultiMoveCalculator
from Yusi.YuFinder.point import Coordinates
from Yusi.YuFinder.city_visit import MoveType


# Ferry Biulding, San Francisco.
ferry_biulding_coordinates = Coordinates(37.7955, -122.3937)
# Pier 39, San Francisco.
pier_39_coordinates = Coordinates(37.8100, -122.4104)
# Place near Pier 39, San Francisco.
near_pier_39_coordinates = Coordinates(37.8097, -122.4104)

walking_speed = 2.  # Walking speed in mph.

driving_speed = 20.  # Speed of car in traffic jams in mph.
# 10 minutes to find and than park a car and 10 minutes to find a parking spot
# when arrived. 
pause_before_driving = 0.30

ptt_speed = 15.  # Speed of Public Transportation or Taxi in mph.
# 15 minutes to buy a ticket and wait in case of public transportation or call
# a taxi.
pause_before_ptt = 0.25

fb_to_p39_walking = 1.916 / walking_speed
fb_to_np39_walking = 1.894 / walking_speed
p39_to_np39_walking = 0.029 / walking_speed

fb_to_p39_driving = 1.916 / driving_speed
fb_to_np39_driving = 1.894 / driving_speed
p39_to_np39_driving = 0.029 / driving_speed

fb_to_p39_ptt = 1.916 / ptt_speed
fb_to_np39_ptt = 1.894 / ptt_speed
p39_to_np39_ptt = 0.029 / ptt_speed

fb_to_p39_pause_and_driving = fb_to_p39_driving + pause_before_driving
fb_to_np39_pause_and_driving = fb_to_np39_driving + pause_before_driving
p39_to_np39_pause_and_driving = p39_to_np39_driving + pause_before_driving

fb_to_p39_pause_and_ptt = fb_to_p39_ptt + pause_before_ptt
fb_to_np39_pause_and_ptt = fb_to_np39_ptt + pause_before_ptt
p39_to_np39_pause_and_ptt = p39_to_np39_ptt + pause_before_ptt

              
class SimpleMoveCalculatorTest(unittest.TestCase):

  def testCalculateMoveDescriptionWalking(self):
    move_calculator = SimpleMoveCalculator(walking_speed, MoveType.walking)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(pier_39_coordinates, move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

  def testCalculateMoveDescriptionDriving(self):
    move_calculator = SimpleMoveCalculator(driving_speed, MoveType.driving)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    self.assertEqual(pier_39_coordinates, move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

  def testCalculateMoveDescriptionPauseBeforeDriving(self):
    move_calculator = SimpleMoveCalculator(
        driving_speed, MoveType.driving, pause=pause_before_driving)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_pause_and_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_pause_and_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_pause_and_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    self.assertEqual(pier_39_coordinates, move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)


class MultiMoveCalculatorCalculatorTest(unittest.TestCase):
  
  def testCalculateMoveDescriptionGeneral(self):
    move_calculator = MultiMoveCalculator(
        [0.5],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(
             ptt_speed, MoveType.ptt, pause=pause_before_ptt)])

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(pier_39_coordinates, move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

  def testCalculateMoveDescriptionWalkingOnly(self):
    move_calculator = MultiMoveCalculator(
        [2.0],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(
             ptt_speed, MoveType.ptt, pause=pause_before_ptt)])

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(pier_39_coordinates, move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

  def testCalculateMoveDescriptionPTTOnly(self):
    move_calculator = MultiMoveCalculator(
        [0.02],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(
             ptt_speed, MoveType.ptt, pause=pause_before_ptt)])

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_pause_and_ptt,
        move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_pause_and_ptt,
        move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    self.assertEqual(pier_39_coordinates, move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

  def testCalculateMoveDescriptionWalkingPTTDriving(self):
    move_calculator = MultiMoveCalculator(
        [1.0, 1.9],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(ptt_speed, MoveType.ptt),
         SimpleMoveCalculator(driving_speed, MoveType.driving)])

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_p39_driving, move_description.move_hours, places=3)
    self.assertEqual(MoveType.driving, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        ferry_biulding_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        fb_to_np39_ptt, move_description.move_hours, places=3)
    self.assertEqual(MoveType.ptt, move_description.move_type)
    self.assertEqual(ferry_biulding_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        pier_39_coordinates, near_pier_39_coordinates)
    self.assertAlmostEqual(
        p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(MoveType.walking, move_description.move_type)
    self.assertEqual(pier_39_coordinates, move_description.from_coordinates)
    self.assertEqual(near_pier_39_coordinates, move_description.to_coordinates)

  def testInconsistentArguments(self):
    MultiMoveCalculator(
        [2.0, 4.0],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(ptt_speed, MoveType.ptt),
         SimpleMoveCalculator(driving_speed, MoveType.driving)])
    self.assertRaises(
        AssertionError,
        MultiMoveCalculator,
        [2.0, 'four'],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(ptt_speed, MoveType.ptt),
         SimpleMoveCalculator(driving_speed, MoveType.driving)])
    self.assertRaises(
        AssertionError,
        MultiMoveCalculator,
        [2.0, 4.0],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(ptt_speed, MoveType.ptt),
         driving_speed])
    self.assertRaises(
        AssertionError,
        MultiMoveCalculator,
        [4.0, 2.0],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(ptt_speed, MoveType.ptt),
         SimpleMoveCalculator(driving_speed, MoveType.driving)])
    self.assertRaises(
        AssertionError,
        MultiMoveCalculator,
        [2.0, 4.0, 6.0],
        [SimpleMoveCalculator(walking_speed, MoveType.walking),
         SimpleMoveCalculator(ptt_speed, MoveType.ptt),
         SimpleMoveCalculator(driving_speed, MoveType.driving)])


if __name__ == '__main__':
    unittest.main()

