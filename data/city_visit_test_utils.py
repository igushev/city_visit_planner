import os
import datetime
import unittest

from data import city_visit
from data import read_csv
from data import point


class CityVisitTestExample(unittest.TestCase):

  @staticmethod
  def GetHotelCoordinates():
    # San Francisco coordinates.
    return point.Coordinates(37.7833, -122.4167)
  
  @staticmethod
  def GetDayVisitParameters(start_datetime, end_datetime, lunch_start_datetime):
    return city_visit.DayVisitParameters(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        lunch_start_datetime=lunch_start_datetime,
        lunch_hours=1.,
        start_coordinates=CityVisitTestExample.GetHotelCoordinates(),
        end_coordinates=CityVisitTestExample.GetHotelCoordinates())

  def setUp(self):

    self.day_visit_parameters_1 = CityVisitTestExample.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 1, 22, 0, 0))

    self.day_visit_parameters_2 = CityVisitTestExample.GetDayVisitParameters(
        start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
        end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0),
        lunch_start_datetime=datetime.datetime(2014, 9, 2, 22, 0, 0))

    self.points = read_csv.ReadCSVToDict(os.path.join('data', 'test_sf_1.csv'))
    
    self.hotel_coordinates = (
       CityVisitTestExample.GetHotelCoordinates())
    
    self.from_hotel_to_ferry_building_move = city_visit.MoveBetween(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 9, 0, 0),
                                    datetime.datetime(2014, 9, 1, 10, 15, 0)),
        city_visit.MoveDescription(self.hotel_coordinates,
                                   self.points['Ferry Building'].coordinates_starts,
                                   1.25, city_visit.MoveType.walking))
    self.ferry_building_point_visit = city_visit.PointVisit(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 10, 15, 0),
                                    datetime.datetime(2014, 9, 1, 11, 15, 0)),
        self.points['Ferry Building'])
    self.from_ferry_building_to_pier_39_move = city_visit.MoveBetween(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 15, 0),
                                    datetime.datetime(2014, 9, 1, 11, 45, 0)),
        city_visit.MoveDescription(self.points['Ferry Building'].coordinates_ends,
                                   self.points['Pier 39'].coordinates_starts,
                                   0.5, city_visit.MoveType.walking))
    self.pier_39_point_visit = city_visit.PointVisit(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 45, 0),
                                    datetime.datetime(2014, 9, 1, 14, 45, 0)),
        self.points['Pier 39'])
    self.from_pier_39_to_hotel = city_visit.MoveBetween(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 1, 14, 45, 0),
                                    datetime.datetime(2014, 9, 1, 16, 15, 0)),
        city_visit.MoveDescription(self.points['Pier 39'].coordinates_ends,
                                   self.hotel_coordinates,
                                   1.5, city_visit.MoveType.walking))
    
    self.day_visit_1 = city_visit.DayVisit(datetime.datetime(2014, 9, 1, 9, 0, 0), [
        self.from_hotel_to_ferry_building_move,
        self.ferry_building_point_visit,
        self.from_ferry_building_to_pier_39_move,
        self.pier_39_point_visit,
        self.from_pier_39_to_hotel], 12.)
    
    self.from_hotel_to_golden_gate_bridge_move = city_visit.MoveBetween(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 0, 0),
                                    datetime.datetime(2014, 9, 2, 9, 15, 0)),
        city_visit.MoveDescription(self.hotel_coordinates,
                                   self.points['Golden Gate Bridge'].coordinates_starts,
                                   0.25, city_visit.MoveType.driving))
    self.golden_gate_bridge_point_visit = city_visit.PointVisit(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 15, 0),
                                    datetime.datetime(2014, 9, 2, 9, 45, 0)),
        self.points['Golden Gate Bridge'])
    self.from_golden_gate_bridge_to_hotel_move = city_visit.MoveBetween(
        city_visit.StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 45, 0),
                                    datetime.datetime(2014, 9, 2, 10, 0, 0)),
        city_visit.MoveDescription(self.points['Golden Gate Bridge'].coordinates_ends,
                                   self.hotel_coordinates,
                                   0.25, city_visit.MoveType.driving))
    
    self.day_visit_2 = city_visit.DayVisit(datetime.datetime(2014, 9, 2, 9, 0, 0), [
        self.from_hotel_to_golden_gate_bridge_move,
        self.golden_gate_bridge_point_visit,
        self.from_golden_gate_bridge_to_hotel_move], 10.)
    
    self.city_visit_summary = city_visit.CityVisitSummary(20., 0.)
    self.city_visit = city_visit.CityVisit([self.day_visit_1, self.day_visit_2], self.city_visit_summary)
    
    super(CityVisitTestExample, self).setUp()
