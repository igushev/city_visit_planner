import datetime
import os
import unittest

import Yusi
from Yusi.YuFinder import point
from Yusi.YuFinder import read_csv
from Yusi.YuFinder import city_visit


points = read_csv.ReadCSVToDict(
    os.path.join(Yusi.GetYusiDir(), 'YuFinder', 'test_sf_1.csv'))

san_francisco_coordinates = point.Coordinates(37.7833, -122.4167)

from_hotel_to_ferry_biulding_move = city_visit.MoveBetween(
    san_francisco_coordinates, points['Ferry Biulding'].coordinates_starts,
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 9, 0, 0),
                                datetime.datetime(2014, 9, 1, 10, 15, 0)),
    city_visit.MoveDescription(1.25, city_visit.MoveType.walking))
ferry_biulding_point_visit = city_visit.PointVisit(
    points['Ferry Biulding'],
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 10, 15, 0),
                                datetime.datetime(2014, 9, 1, 11, 15, 0)))
from_ferry_biulding_to_pier_39_move = city_visit.MoveBetween(
    points['Ferry Biulding'].coordinates_ends,
    points['Pier 39'].coordinates_starts,
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 15, 0),
                                datetime.datetime(2014, 9, 1, 11, 45, 0)),
    city_visit.MoveDescription(0.5, city_visit.MoveType.walking))
pier_39_point_visit = city_visit.PointVisit(
    points['Pier 39'],
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 45, 0),
                                datetime.datetime(2014, 9, 1, 14, 45, 0)))
from_pier_39_to_hotel = city_visit.MoveBetween(
    points['Pier 39'].coordinates_ends, san_francisco_coordinates,
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 14, 45, 0),
                                datetime.datetime(2014, 9, 1, 16, 15, 0)),
    city_visit.MoveDescription(1.5, city_visit.MoveType.walking))

day_visit_1 = city_visit.DayVisit(datetime.datetime(2014, 9, 1, 9, 0, 0), [
    from_hotel_to_ferry_biulding_move,
    ferry_biulding_point_visit,
    from_ferry_biulding_to_pier_39_move,
    pier_39_point_visit,
    from_pier_39_to_hotel], 12.)

from_hotel_to_golden_gate_bridge_move = city_visit.MoveBetween(
    san_francisco_coordinates,
    points['Golden Gate Bridge'].coordinates_starts,
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 0, 0),
                                datetime.datetime(2014, 9, 2, 9, 15, 0)),
    city_visit.MoveDescription(0.25, city_visit.MoveType.driving))
golden_gate_bridge_point_visit = city_visit.PointVisit(
    points['Golden Gate Bridge'],
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 15, 0),
                                datetime.datetime(2014, 9, 2, 9, 45, 0)))
from_golden_gate_bridge_to_hotel_move = city_visit.MoveBetween(
    points['Golden Gate Bridge'].coordinates_ends, san_francisco_coordinates,
    city_visit.StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 45, 0),
                                datetime.datetime(2014, 9, 2, 10, 0, 0)),
    city_visit.MoveDescription(0.25, city_visit.MoveType.driving))

day_visit_2 = city_visit.DayVisit(datetime.datetime(2014, 9, 2, 9, 0, 0), [
    from_hotel_to_golden_gate_bridge_move,
    golden_gate_bridge_point_visit,
    from_golden_gate_bridge_to_hotel_move], 10.)

city_visit_ex = city_visit.CityVisit([day_visit_1, day_visit_2])


class DayVisitParametersTest(unittest.TestCase):
  
  def testHashKey(self):
    day_visit_parameters_9to21 = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=san_francisco_coordinates,
        end_coordinates=san_francisco_coordinates)
    day_visit_parameters_9to23 = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 23, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=san_francisco_coordinates,
        end_coordinates=san_francisco_coordinates)
    # Stupid test.
    self.assertEqual(day_visit_parameters_9to21.HashKey(),
                     day_visit_parameters_9to21.HashKey())
    self.assertNotEqual(day_visit_parameters_9to21.HashKey(),
                        day_visit_parameters_9to23.HashKey())


class MoveBetweenTest(unittest.TestCase):

  def testInitValidation(self):
    # move_hours in move_description are not consistent with
    # start_end_datetime.
    self.assertRaises(
        AssertionError, city_visit.MoveBetween,
        points['Ferry Biulding'].coordinates_ends,
        points['Pier 39'].coordinates_starts,
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 15, 0),
                                    datetime.datetime(2014, 9, 1, 11, 45, 0)),
        city_visit.MoveDescription(1.0, city_visit.MoveType.walking))


class DayVisitTest(unittest.TestCase):

  def testHashKey(self):
    self.assertEqual(day_visit_1.HashKey(), day_visit_1.HashKey())
    self.assertNotEqual(day_visit_1.HashKey(), day_visit_2.HashKey())

  def testGetPoints(self):
    self.assertEqual([points['Ferry Biulding'], points['Pier 39']],
                     day_visit_1.GetPoints())
    self.assertEqual([points['Golden Gate Bridge']],
                     day_visit_2.GetPoints())

  def testInitValidation(self):
    # No final move.
    self.assertRaisesRegexp(
        AssertionError, 'Wrong number of actions.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            from_hotel_to_ferry_biulding_move,
            ferry_biulding_point_visit,
            from_ferry_biulding_to_pier_39_move,
            pier_39_point_visit], 10.)
    # No start move.
    self.assertRaisesRegexp(
        AssertionError, 'Wrong order of actions: no MoveBetween.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            ferry_biulding_point_visit,
            from_ferry_biulding_to_pier_39_move,
            pier_39_point_visit,
            from_pier_39_to_hotel], 10.)
    # No middle moves.
    self.assertRaisesRegexp(
        AssertionError, 'Wrong order of actions: no MoveBetween.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            from_hotel_to_ferry_biulding_move,
            ferry_biulding_point_visit,
            pier_39_point_visit,
            from_pier_39_to_hotel], 10.)
    # No first point.
    self.assertRaisesRegexp(
        AssertionError, 'Wrong order of actions: no PointVisit.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            from_hotel_to_ferry_biulding_move,
            from_ferry_biulding_to_pier_39_move,
            pier_39_point_visit,
            from_pier_39_to_hotel], 10.)
    # No second point.
    self.assertRaisesRegexp(
        AssertionError, 'Wrong order of actions: no PointVisit.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            from_hotel_to_ferry_biulding_move,
            ferry_biulding_point_visit,
            from_ferry_biulding_to_pier_39_move,
            from_pier_39_to_hotel], 10.)


class CityVisitTest(unittest.TestCase):

  def testCost(self):
    self.assertEqual(22., city_visit_ex.cost)

  def testStr(self):
    city_visit_str_actual = '%s' % city_visit_ex
    city_visit_str_expected = """Date: 2014-09-01
Cost: 12.00
Walking from 37.7833:-122.4167 to 37.7955:-122.3937 from 09:00:00 to 10:15:00
Visiting point "Ferry Biulding" from 10:15:00 to 11:15:00
Walking from 37.7955:-122.3937 to 37.8100:-122.4104 from 11:15:00 to 11:45:00
Visiting point "Pier 39" from 11:45:00 to 14:45:00
Walking from 37.8100:-122.4104 to 37.7833:-122.4167 from 14:45:00 to 16:15:00
Date: 2014-09-02
Cost: 10.00
Driving from 37.7833:-122.4167 to 37.8197:-122.4786 from 09:00:00 to 09:15:00
Visiting point "Golden Gate Bridge" from 09:15:00 to 09:45:00
Driving from 37.8197:-122.4786 to 37.7833:-122.4167 from 09:45:00 to 10:00:00
Total cost: 22.00"""
    self.assertEqual(city_visit_str_expected, city_visit_str_actual)


if __name__ == '__main__':
    unittest.main()

