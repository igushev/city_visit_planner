import datetime
import tempfile
import unittest

from Yusi.YuFinder.read_csv import ReadCSV, ReadCSVToDict, ExtractOperatingHours,\
  ExtractCoordinates
from Yusi.YuFinder.point import OperatingHours, Coordinates, Point


class ReadCSVTest(unittest.TestCase):

  def testExtractCoordinatesGeneral(self):
    ferry_building_coordinates = ExtractCoordinates('37.7955N, 122.3937W')
    self.assertEqual(Coordinates(37.7955, -122.3937),
                     ferry_building_coordinates)

    ferry_building_coordinates = ExtractCoordinates('37.7955, -122.3937')
    self.assertEqual(Coordinates(37.7955, -122.3937),
                     ferry_building_coordinates)

    kremlin_coordinates = ExtractCoordinates('55.7517N, 37.6178E')
    self.assertEqual(Coordinates(55.7517, 37.6178), kremlin_coordinates)

    kremlin_coordinates = ExtractCoordinates('55.7517, 37.6178')
    self.assertEqual(Coordinates(55.7517, 37.6178), kremlin_coordinates)

    christ_the_redeemer_coordinates = ExtractCoordinates('22.9519S, 43.2106W')
    self.assertEqual(Coordinates(-22.9519, -43.2106),
                     christ_the_redeemer_coordinates)

    christ_the_redeemer_coordinates = ExtractCoordinates('-22.9519, -43.2106')
    self.assertEqual(Coordinates(-22.9519, -43.2106),
                     christ_the_redeemer_coordinates)

    self.assertEqual(None, ExtractCoordinates(''))

  def testExtractOperatingHoursGeneral(self):
    de_young_museum_operating_hours = (
        ExtractOperatingHours('9:30:00', '17:15:00'))
    self.assertEqual(OperatingHours(datetime.time(9, 30, 0),
                                    datetime.time(17, 15, 0)),
                     de_young_museum_operating_hours)

  def testReadCSVGeneral(self):
    s = str()
    s += 'ID,Name,CoordinatesStarts,CoordinatesEnds,OperatingHoursOpens,OperatingHoursCloses,Duration,Rank\n'
    s += '1,Ferry Building,"37.7955N, 122.3937W",,09:00:00,18:00:00,1,1\n'
    s += '2,Pier 39,"37.8100N, 122.4104W",,10:00:00,22:00:00,3,2\n'
    csv_filepath = tempfile.mktemp()
    with open(csv_filepath, 'w') as csv_file:
      csv_file.write(s)

    pier_39 = Point(
        'Pier 39',
        Coordinates(37.8100, -122.4104),
        None,
        OperatingHours(datetime.time(10, 0, 0), datetime.time(22, 0, 0)),
        3.)

    points = ReadCSV(csv_filepath)
    self.assertEqual(2, len(points))
    self.assertEqual(pier_39, points[1])
    points = ReadCSVToDict(csv_filepath)
    self.assertEqual(2, len(points))
    self.assertEqual(set(['Ferry Building', 'Pier 39']), set(points.keys()))
    self.assertEqual(pier_39, points['Pier 39'])
                     

if __name__ == '__main__':
    unittest.main()

