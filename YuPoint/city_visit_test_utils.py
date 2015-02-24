import os
import datetime
import unittest

import Yusi
from Yusi.YuPoint.city_visit import MoveBetween, StartEndDatetime, PointVisit,\
  MoveDescription, MoveType, DayVisit, CityVisit
from Yusi.YuPoint.read_csv import ReadCSVToDict
from Yusi.YuPoint.point import Coordinates


class CityVisitTestExample(unittest.TestCase):
  
  def setUp(self):

    self.points = ReadCSVToDict(
        os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
    
    self.san_francisco_coordinates = Coordinates(37.7833, -122.4167)
    
    self.from_hotel_to_ferry_building_move = MoveBetween(
        StartEndDatetime(datetime.datetime(2014, 9, 1, 9, 0, 0),
                         datetime.datetime(2014, 9, 1, 10, 15, 0)),
        MoveDescription(self.san_francisco_coordinates,
                        self.points['Ferry Building'].coordinates_starts,
                        1.25, MoveType.walking))
    self.ferry_building_point_visit = PointVisit(
        StartEndDatetime(datetime.datetime(2014, 9, 1, 10, 15, 0),
                         datetime.datetime(2014, 9, 1, 11, 15, 0)),
        self.points['Ferry Building'])
    self.from_ferry_building_to_pier_39_move = MoveBetween(
        StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 15, 0),
                         datetime.datetime(2014, 9, 1, 11, 45, 0)),
        MoveDescription(self.points['Ferry Building'].coordinates_ends,
                        self.points['Pier 39'].coordinates_starts,
                        0.5, MoveType.walking))
    self.pier_39_point_visit = PointVisit(
        StartEndDatetime(datetime.datetime(2014, 9, 1, 11, 45, 0),
                         datetime.datetime(2014, 9, 1, 14, 45, 0)),
        self.points['Pier 39'])
    self.from_pier_39_to_hotel = MoveBetween(
        StartEndDatetime(datetime.datetime(2014, 9, 1, 14, 45, 0),
                         datetime.datetime(2014, 9, 1, 16, 15, 0)),
        MoveDescription(self.points['Pier 39'].coordinates_ends,
                        self.san_francisco_coordinates,
                        1.5, MoveType.walking))
    
    self.day_visit_1 = DayVisit(datetime.datetime(2014, 9, 1, 9, 0, 0), [
        self.from_hotel_to_ferry_building_move,
        self.ferry_building_point_visit,
        self.from_ferry_building_to_pier_39_move,
        self.pier_39_point_visit,
        self.from_pier_39_to_hotel], 12.)
    
    self.from_hotel_to_golden_gate_bridge_move = MoveBetween(
        StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 0, 0),
                         datetime.datetime(2014, 9, 2, 9, 15, 0)),
        MoveDescription(self.san_francisco_coordinates,
                        self.points['Golden Gate Bridge'].coordinates_starts,
                        0.25, MoveType.driving))
    self.golden_gate_bridge_point_visit = PointVisit(
        StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 15, 0),
                         datetime.datetime(2014, 9, 2, 9, 45, 0)),
        self.points['Golden Gate Bridge'])
    self.from_golden_gate_bridge_to_hotel_move = MoveBetween(
        StartEndDatetime(datetime.datetime(2014, 9, 2, 9, 45, 0),
                         datetime.datetime(2014, 9, 2, 10, 0, 0)),
        MoveDescription(self.points['Golden Gate Bridge'].coordinates_ends,
                        self.san_francisco_coordinates,
                        0.25, MoveType.driving))
    
    self.day_visit_2 = DayVisit(datetime.datetime(2014, 9, 2, 9, 0, 0), [
        self.from_hotel_to_golden_gate_bridge_move,
        self.golden_gate_bridge_point_visit,
        self.from_golden_gate_bridge_to_hotel_move], 10.)
    
    self.city_visit = CityVisit([self.day_visit_1, self.day_visit_2], 20.)
    
    super(CityVisitTestExample, self).setUp()
