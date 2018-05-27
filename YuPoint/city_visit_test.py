import datetime
import unittest

import Yusi
from Yusi.YuPoint import city_visit
from Yusi.YuPoint import city_visit_test_utils


class DayVisitParametersTest(city_visit_test_utils.CityVisitTestExample):
  
  def testDatelessHashKey(self):
    day_visit_parameters_9to21 = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=self.hotel_coordinates,
        end_coordinates=self.hotel_coordinates)
    day_visit_parameters_9to23 = city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 23, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 13, 0, 0),
        lunch_hours=1.,
        start_coordinates=self.hotel_coordinates,
        end_coordinates=self.hotel_coordinates)
    # Stupid test.
    self.assertEqual(day_visit_parameters_9to21.DatelessHashKey(),
                     day_visit_parameters_9to21.DatelessHashKey())
    self.assertNotEqual(day_visit_parameters_9to21.DatelessHashKey(),
                        day_visit_parameters_9to23.DatelessHashKey())


class MoveBetweenTest(city_visit_test_utils.CityVisitTestExample):

  def testInitValidation(self):
    # move_hours in move_description are not consistent with
    # start_end_datetime.
    self.assertRaises(
        AssertionError, city_visit.MoveBetween,
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 15, 0),
                                    datetime.datetime(2014, 9, 1, 11, 45, 0)),
        city_visit.MoveDescription(self.points['Ferry Building'].coordinates_ends,
                                   self.points['Pier 39'].coordinates_starts,
                                   1.0, city_visit.MoveType.walking))


class DayVisitTest(city_visit_test_utils.CityVisitTestExample):

  def testDatelessHashKey(self):
    self.assertEqual(self.day_visit_1.DatelessHashKey(),
                     self.day_visit_1.DatelessHashKey())
    self.assertNotEqual(self.day_visit_1.DatelessHashKey(),
                        self.day_visit_2.DatelessHashKey())

  def testGetPoints(self):
    self.assertEqual([self.points['Ferry Building'], self.points['Pier 39']],
                      self.day_visit_1.GetPoints())
    self.assertEqual([self.points['Golden Gate Bridge']],
                      self.day_visit_2.GetPoints())

  def testInitValidation(self):
    # No final move.
    self.assertRaisesRegex(
        AssertionError, 'Wrong number of actions.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            self.from_hotel_to_ferry_building_move,
            self.ferry_building_point_visit,
            self.from_ferry_building_to_pier_39_move,
            self.pier_39_point_visit], 10.)
    # No start move.
    self.assertRaisesRegex(
        AssertionError, 'Wrong order of actions: no MoveBetween.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            self.ferry_building_point_visit,
            self.from_ferry_building_to_pier_39_move,
            self.pier_39_point_visit,
            self.from_pier_39_to_hotel], 10.)
    # No middle moves.
    self.assertRaisesRegex(
        AssertionError, 'Wrong order of actions: no MoveBetween.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            self.from_hotel_to_ferry_building_move,
            self.ferry_building_point_visit,
            self.pier_39_point_visit,
            self.from_pier_39_to_hotel], 10.)
    # No first point.
    self.assertRaisesRegex(
        AssertionError, 'Wrong order of actions: no PointVisit.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            self.from_hotel_to_ferry_building_move,
            self.from_ferry_building_to_pier_39_move,
            self.pier_39_point_visit,
            self.from_pier_39_to_hotel], 10.)
    # No second point.
    self.assertRaisesRegex(
        AssertionError, 'Wrong order of actions: no PointVisit.',
        city_visit.DayVisit, datetime.datetime(2014, 9, 1, 9, 0, 0), [
            self.from_hotel_to_ferry_building_move,
            self.ferry_building_point_visit,
            self.from_ferry_building_to_pier_39_move,
            self.from_pier_39_to_hotel], 10.)


class CityVisitTest(city_visit_test_utils.CityVisitTestExample):

  def testGetPoints(self):
    self.assertEqual([self.points['Ferry Building'], self.points['Pier 39'],
                      self.points['Golden Gate Bridge']],
                     self.city_visit.GetPoints())

  def testStr(self):
    city_visit_str_actual = '%s' % self.city_visit
    city_visit_str_expected = """Date: 2014-09-01
Walking from 37.7833:-122.4167 to 37.7955:-122.3937 from 09:00:00 to 10:15:00
Visiting point "Ferry Building" from 10:15:00 to 11:15:00
Walking from 37.7955:-122.3937 to 37.8100:-122.4104 from 11:15:00 to 11:45:00
Visiting point "Pier 39" from 11:45:00 to 14:45:00
Walking from 37.8100:-122.4104 to 37.7833:-122.4167 from 14:45:00 to 16:15:00
Cost: 12.00
Price: 0.00
Date: 2014-09-02
Driving from 37.7833:-122.4167 to 37.8197:-122.4786 from 09:00:00 to 09:15:00
Visiting point "Golden Gate Bridge" from 09:15:00 to 09:45:00
Driving from 37.8197:-122.4786 to 37.7833:-122.4167 from 09:45:00 to 10:00:00
Cost: 10.00
Price: 0.00
Total cost: 20.00
Total price: 0.00"""
    self.assertEqual(city_visit_str_expected, city_visit_str_actual)


if __name__ == '__main__':
    unittest.main()
