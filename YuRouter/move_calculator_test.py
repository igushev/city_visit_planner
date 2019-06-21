import unittest

from data import point
from data import city_visit
from YuRouter import move_calculator as move_calculator_


class MoveCalculatorTest(unittest.TestCase):
  
  def setUp(self):
    # Ferry Building, San Francisco.
    self.ferry_building_coordinates = point.Coordinates(37.7955, -122.3937)
    # Pier 39, San Francisco.
    self.pier_39_coordinates = point.Coordinates(37.8100, -122.4104)
    # Place near Pier 39, San Francisco.
    self.near_pier_39_coordinates = point.Coordinates(37.8097, -122.4104)
    
    self.walking_speed = 2.  # Walking speed in mph.
    
    self.driving_speed = 20.  # Speed of car in traffic jams in mph.
    # 10 minutes to find and than park a car and 10 minutes to find a parking
    # spot when arrived. 
    self.pause_before_driving = 0.30
    
    self.ptt_speed = 15.  # Speed of Public Transportation or Taxi in mph.
    # 15 minutes to buy a ticket and wait in case of public transportation or
    # call a taxi.
    self.pause_before_ptt = 0.25
    
    self.fb_to_p39_walking = 1.916 / self.walking_speed
    self.fb_to_np39_walking = 1.894 / self.walking_speed
    self.p39_to_np39_walking = 0.029 / self.walking_speed
    
    self.fb_to_p39_driving = 1.916 / self.driving_speed
    self.fb_to_np39_driving = 1.894 / self.driving_speed
    self.p39_to_np39_driving = 0.029 / self.driving_speed
    
    self.fb_to_p39_ptt = 1.916 / self.ptt_speed
    self.fb_to_np39_ptt = 1.894 / self.ptt_speed
    self.p39_to_np39_ptt = 0.029 / self.ptt_speed
    
    self.fb_to_p39_pause_and_driving = (
        self.fb_to_p39_driving + self.pause_before_driving)
    self.fb_to_np39_pause_and_driving = (
        self.fb_to_np39_driving + self.pause_before_driving)
    self.p39_to_np39_pause_and_driving = (
        self.p39_to_np39_driving + self.pause_before_driving)
    
    self.fb_to_p39_pause_and_ptt = self.fb_to_p39_ptt + self.pause_before_ptt
    self.fb_to_np39_pause_and_ptt = self.fb_to_np39_ptt + self.pause_before_ptt
    self.p39_to_np39_pause_and_ptt = (
        self.p39_to_np39_ptt + self.pause_before_ptt)

    super(MoveCalculatorTest, self).setUp()

              
class SimpleMoveCalculatorTest(MoveCalculatorTest):

  def testCalculateMoveDescriptionWalking(self):
    move_calculator = move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_p39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.pier_39_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.pier_39_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

  def testCalculateMoveDescriptionDriving(self):
    move_calculator = move_calculator_.SimpleMoveCalculator(self.driving_speed, city_visit.MoveType.driving)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_p39_driving, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.driving, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_np39_driving, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.driving, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.pier_39_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.p39_to_np39_driving, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.driving, move_description.move_type)
    self.assertEqual(self.pier_39_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

  def testCalculateMoveDescriptionPauseBeforeDriving(self):
    move_calculator = move_calculator_.SimpleMoveCalculator(
        self.driving_speed, city_visit.MoveType.driving, pause=self.pause_before_driving)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_p39_pause_and_driving, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.driving, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_np39_pause_and_driving, move_description.move_hours,
        places=3)
    self.assertEqual(city_visit.MoveType.driving, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.pier_39_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.p39_to_np39_pause_and_driving, move_description.move_hours,
        places=3)
    self.assertEqual(city_visit.MoveType.driving, move_description.move_type)
    self.assertEqual(self.pier_39_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)


class MultiMoveCalculatorCalculatorTest(MoveCalculatorTest):
  
  def testCalculateMoveDescriptionGeneral(self):
    move_calculator = move_calculator_.MultiMoveCalculator(
        [0.5],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(
             self.ptt_speed, city_visit.MoveType.ptt, pause=self.pause_before_ptt)])

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_p39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.ptt, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_np39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.ptt, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.pier_39_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.pier_39_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

  def testCalculateMoveDescriptionWalkingOnly(self):
    move_calculator = move_calculator_.MultiMoveCalculator(
        [2.0],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(
             self.ptt_speed, city_visit.MoveType.ptt, pause=self.pause_before_ptt)])

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_p39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.pier_39_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.pier_39_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

  def testCalculateMoveDescriptionPTTOnly(self):
    move_calculator = move_calculator_.MultiMoveCalculator(
        [0.02],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(
             self.ptt_speed, city_visit.MoveType.ptt, pause=self.pause_before_ptt)])

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_p39_pause_and_ptt,
        move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.ptt, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_np39_pause_and_ptt,
        move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.ptt, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.pier_39_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.p39_to_np39_pause_and_ptt, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.ptt, move_description.move_type)
    self.assertEqual(self.pier_39_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

  def testCalculateMoveDescriptionWalkingPTTDriving(self):
    move_calculator = move_calculator_.MultiMoveCalculator(
        [1.0, 1.9],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(self.ptt_speed, city_visit.MoveType.ptt),
         move_calculator_.SimpleMoveCalculator(self.driving_speed, city_visit.MoveType.driving)])

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_p39_driving, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.driving, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.pier_39_coordinates, move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.ferry_building_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.fb_to_np39_ptt, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.ptt, move_description.move_type)
    self.assertEqual(self.ferry_building_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

    move_description = move_calculator.CalculateMoveDescription(
        self.pier_39_coordinates, self.near_pier_39_coordinates)
    self.assertAlmostEqual(
        self.p39_to_np39_walking, move_description.move_hours, places=3)
    self.assertEqual(city_visit.MoveType.walking, move_description.move_type)
    self.assertEqual(self.pier_39_coordinates,
                     move_description.from_coordinates)
    self.assertEqual(self.near_pier_39_coordinates,
                     move_description.to_coordinates)

  def testInconsistentArguments(self):
    move_calculator_.MultiMoveCalculator(
        [2.0, 4.0],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(self.ptt_speed, city_visit.MoveType.ptt),
         move_calculator_.SimpleMoveCalculator(self.driving_speed, city_visit.MoveType.driving)])
    self.assertRaises(
        AssertionError,
        move_calculator_.MultiMoveCalculator,
        [2.0, 'four'],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(self.ptt_speed, city_visit.MoveType.ptt),
         move_calculator_.SimpleMoveCalculator(self.driving_speed, city_visit.MoveType.driving)])
    self.assertRaises(
        AssertionError,
        move_calculator_.MultiMoveCalculator,
        [2.0, 4.0],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(self.ptt_speed, city_visit.MoveType.ptt),
         self.driving_speed])
    self.assertRaises(
        AssertionError,
        move_calculator_.MultiMoveCalculator,
        [4.0, 2.0],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(self.ptt_speed, city_visit.MoveType.ptt),
         move_calculator_.SimpleMoveCalculator(self.driving_speed, city_visit.MoveType.driving)])
    self.assertRaises(
        AssertionError,
        move_calculator_.MultiMoveCalculator,
        [2.0, 4.0, 6.0],
        [move_calculator_.SimpleMoveCalculator(self.walking_speed, city_visit.MoveType.walking),
         move_calculator_.SimpleMoveCalculator(self.ptt_speed, city_visit.MoveType.ptt),
         move_calculator_.SimpleMoveCalculator(self.driving_speed, city_visit.MoveType.driving)])


if __name__ == '__main__':
    unittest.main()

