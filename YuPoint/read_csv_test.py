import datetime
import tempfile
import unittest

from Yusi.YuPoint import read_csv
from Yusi.YuPoint import point


class ReadCSVTest(unittest.TestCase):

  def testExtractCoordinatesGeneral(self):
    ferry_building_coordinates = read_csv.ExtractCoordinates('37.7955N, 122.3937W')
    self.assertEqual(point.Coordinates(37.7955, -122.3937),
                     ferry_building_coordinates)

    ferry_building_coordinates = read_csv.ExtractCoordinates('37.7955, -122.3937')
    self.assertEqual(point.Coordinates(37.7955, -122.3937),
                     ferry_building_coordinates)

    kremlin_coordinates = read_csv.ExtractCoordinates('55.7517N, 37.6178E')
    self.assertEqual(point.Coordinates(55.7517, 37.6178), kremlin_coordinates)

    kremlin_coordinates = read_csv.ExtractCoordinates('55.7517, 37.6178')
    self.assertEqual(point.Coordinates(55.7517, 37.6178), kremlin_coordinates)

    christ_the_redeemer_coordinates = read_csv.ExtractCoordinates('22.9519S, 43.2106W')
    self.assertEqual(point.Coordinates(-22.9519, -43.2106),
                     christ_the_redeemer_coordinates)

    christ_the_redeemer_coordinates = read_csv.ExtractCoordinates('-22.9519, -43.2106')
    self.assertEqual(point.Coordinates(-22.9519, -43.2106),
                     christ_the_redeemer_coordinates)

    self.assertEqual(None, read_csv.ExtractCoordinates(''))

  def testExtractOperatingHoursGeneral(self):
    de_young_museum_operating_hours = (
        read_csv.ExtractOperatingHours('9:30:00', '17:15:00'))
    self.assertEqual(point.OperatingHours(datetime.time(9, 30, 0),
                                          datetime.time(17, 15, 0)),
                     de_young_museum_operating_hours)

  def testReadCSVGeneral(self):
    s = str()
    s += 'ID,Name,CoordinatesStarts,CoordinatesEnds,OperatingHoursOpens,OperatingHoursCloses,Duration,Popularity,City Tours,Landmarks,Nature,Museums,Shopping,Dining,Senior,Adult,Junior,Child,Toddlers,Price,Parking,Eating\n'
    s += '1,Ferry Building,"37.7955N, 122.3937W",,09:00:00,18:00:00,1,80,,100,,,,,90,90,40,70,,,,100\n'
    s += '2,Pier 39,"37.8100N, 122.4104W",,10:00:00,22:00:00,3,80,,100,,,30,60,70,70,70,90,,,,100\n'
    csv_filepath = tempfile.mktemp()
    with open(csv_filepath, 'w') as csv_file:
      csv_file.write(s)

    pier_39 = point.Point(
        name='Pier 39',
        coordinates_starts=point.Coordinates(37.8100, -122.4104),
        coordinates_ends=None,
        operating_hours=point.OperatingHours(datetime.time(10, 0, 0), datetime.time(22, 0, 0)),
        duration=3.,
        popularity=80,
        point_type=point.PointType(
            city_tours=None,
            landmarks=100,
            nature=None,
            museums=None,
            shopping=30,
            dining=60),
        age_group=point.AgeGroup(
            senior=70,
            adult=70,
            junior=70,
            child=90,
            toddlers=None),
        price=None,
        parking=None,
        eating=100)

    points = read_csv.ReadCSV(csv_filepath)
    self.assertEqual(2, len(points))
    self.assertEqual(pier_39, points[1])
    points = read_csv.ReadCSVToDict(csv_filepath)
    self.assertEqual(2, len(points))
    self.assertEqual(set(['Ferry Building', 'Pier 39']), set(points.keys()))
    self.assertEqual(pier_39, points['Pier 39'])
                     

if __name__ == '__main__':
    unittest.main()

