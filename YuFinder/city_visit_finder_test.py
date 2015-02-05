import datetime
import unittest

import Yusi
from Yusi.YuFinder.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuFinder.city_visit import DayVisitParameters
from Yusi.YuFinder.city_visit_finder import CityVisitFinder
from Yusi.YuFinder.cost_accumulator import FactorCostAccumulatorGenerator
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder import test_utils
from Yusi.YuFinder.day_visit_finder import DayVisitFinder
from Yusi.YuFinder.city_visit_cost_calculator import CityVisitCostCalculatorGenerator


class CityVisitFinderTest(unittest.TestCase):

  @staticmethod
  def GetDayVisitParameters(start_datetime, end_datetime):
    return DayVisitParameters(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        lunch_start_datetime=datetime.datetime(
            start_datetime.year, start_datetime.month, start_datetime.day,
            13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_utils.MockCoordinates('Hotel'),
        end_coordinates=test_utils.MockCoordinates('Restaurant'))

  def setUp(self):
    no_point_visit_factor = 0
    no_point_visit_const = 1000
    day_visit_heap_size = 1000
    max_depth = 1
    city_visit_heap_size = 10
    max_non_pushed_points = 3
    self.points = test_utils.MockPoints()
    move_calculator = test_utils.MockMoveCalculator()
    point_fit = SimplePointFit()
    cost_accumulator_generator=FactorCostAccumulatorGenerator(
        no_point_visit_factor=no_point_visit_factor,
        no_point_visit_const=no_point_visit_const)
    day_visit_cost_calculator_generator = DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=cost_accumulator_generator)
    day_visit_finder = DayVisitFinder(
        calculator_generator=day_visit_cost_calculator_generator,
        day_visit_heap_size=day_visit_heap_size)
    city_visit_cost_calculator_generator = CityVisitCostCalculatorGenerator(
        cost_accumulator_generator=cost_accumulator_generator)
    self.city_visit_finder = CityVisitFinder(
        day_visit_finder=day_visit_finder,
        city_visit_cost_calculator_generator=(
            city_visit_cost_calculator_generator),
        max_depth=max_depth,
        city_visit_heap_size=city_visit_heap_size,
        max_non_pushed_points=max_non_pushed_points)
    super(CityVisitFinderTest, self).setUp()

  def testOneShortDay(self):
    day_visit_parameterss = [
        CityVisitFinderTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 1, 17, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0))]

    # Union Square would fit but it's after 3 failed points.
    city_visit_best, point_left = self.city_visit_finder.FindCityVisit(
        [self.points['Twin Peaks'],
         self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square']],
        day_visit_parameterss)
    day_visits = city_visit_best.day_visits
    self.assertEqual(1, len(day_visits))
    self.assertEqual([], day_visits[0].GetPoints())
    self.assertEqual("""Date: 2014-09-01
Cost: 1.00
Walking from Hotel to Restaurant from 17:00:00 to 18:00:00
Total cost: 5001.00""", str(city_visit_best))
    self.assertEqual(
        [self.points['Twin Peaks'],
         self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square']],
        point_left)

  def testOneDay(self):
    day_visit_parameterss = [
        CityVisitFinderTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0))]

    city_visit_best, point_left = self.city_visit_finder.FindCityVisit(
        [self.points['Twin Peaks'],
         self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square']],
        day_visit_parameterss)
    day_visits = city_visit_best.day_visits
    self.assertEqual(1, len(day_visits))
    self.assertEqual(
        [self.points['Ferry Biulding'],
         self.points['Union Square'],
         self.points['Twin Peaks']], day_visits[0].GetPoints())

    self.assertEqual("""Date: 2014-09-01
Cost: 11.50
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Walking from Ferry Biulding to Union Square from 11:00:00 to 13:00:00
Having lunch from 13:00:00 to 14:00:00
Visiting point "Union Square" from 14:00:00 to 15:00:00
Walking from Union Square to Twin Peaks from 15:00:00 to 18:00:00
Visiting point "Twin Peaks" from 18:00:00 to 18:30:00
Walking from Twin Peaks to Restaurant from 18:30:00 to 20:30:00
Total cost: 2011.50""", str(city_visit_best))
    self.assertEqual(
        [self.points['Pier 39'],
         self.points['Golden Gate Bridge']],
        point_left)

  def testTwoDays(self):
    day_visit_parameterss = [
        CityVisitFinderTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0)),
        CityVisitFinderTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0))]

    city_visit_best, point_left = self.city_visit_finder.FindCityVisit(
        [self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square'],
         self.points['Twin Peaks']],
        day_visit_parameterss)
    
    day_visits = city_visit_best.day_visits
    self.assertEqual(2, len(day_visits))
    self.assertEqual(
        [self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Union Square']], day_visits[0].GetPoints())
    self.assertEqual(
        [self.points['Twin Peaks']], day_visits[1].GetPoints())
    
    self.assertEqual("""Date: 2014-09-01
Cost: 11.00
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Walking from Ferry Biulding to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Union Square from 16:00:00 to 18:00:00
Visiting point "Union Square" from 18:00:00 to 19:00:00
Walking from Union Square to Restaurant from 19:00:00 to 20:00:00
Date: 2014-09-02
Cost: 6.50
Walking from Hotel to Twin Peaks from 09:00:00 to 12:00:00
Visiting point "Twin Peaks" from 12:00:00 to 12:30:00
Having lunch from 12:30:00 to 13:30:00
Walking from Twin Peaks to Restaurant from 13:30:00 to 15:30:00
Total cost: 1017.50""", str(city_visit_best))
    self.assertEqual(
        [self.points['Golden Gate Bridge']],
        point_left)

  def testTwoDaysOneShortDay(self):
    day_visit_parameterss = [
      CityVisitFinderTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 1, 23, 0, 0)),
      CityVisitFinderTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0)),
      CityVisitFinderTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 3, 17, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 3, 21, 0, 0))]                         

    city_visit_best, point_left = self.city_visit_finder.FindCityVisit(
        [self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square'],
         self.points['Twin Peaks']],
        day_visit_parameterss)

    day_visits = city_visit_best.day_visits
    self.assertEqual(3, len(day_visits))
    self.assertEqual(
        [self.points['Pier 39']], day_visits[0].GetPoints())
    self.assertEqual(
        [self.points['Ferry Biulding'],
         self.points['Twin Peaks']], day_visits[1].GetPoints())
    self.assertEqual([self.points['Union Square']], day_visits[2].GetPoints())

    self.assertEqual("""Date: 2014-09-01
Cost: 11.00
Walking from Hotel to Pier 39 from 09:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Restaurant from 16:00:00 to 20:00:00
Date: 2014-09-02
Cost: 10.50
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Having lunch from 11:00:00 to 12:00:00
Walking from Ferry Biulding to Twin Peaks from 12:00:00 to 17:00:00
Visiting point "Twin Peaks" from 17:00:00 to 17:30:00
Walking from Twin Peaks to Restaurant from 17:30:00 to 19:30:00
Date: 2014-09-03
Cost: 3.00
Walking from Hotel to Union Square from 17:00:00 to 18:00:00
Visiting point "Union Square" from 18:00:00 to 19:00:00
Walking from Union Square to Restaurant from 19:00:00 to 20:00:00
Total cost: 1024.50""", str(city_visit_best))
    self.assertEqual(
        [self.points['Golden Gate Bridge']],
        point_left)

  def testThreeDays(self):
    day_visit_parameterss = [
      CityVisitFinderTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 1, 23, 0, 0)),
      CityVisitFinderTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0)),
      CityVisitFinderTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 3, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 3, 21, 0, 0))]                         

    city_visit_best, point_left = self.city_visit_finder.FindCityVisit(
        [self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square'],
         self.points['Twin Peaks']],
        day_visit_parameterss)

    day_visits = city_visit_best.day_visits
    self.assertEqual(3, len(day_visits))
    self.assertEqual(
        [self.points['Golden Gate Bridge']], day_visits[0].GetPoints())
    self.assertEqual(
        [self.points['Ferry Biulding'],
         self.points['Pier 39'],
         self.points['Union Square']], day_visits[1].GetPoints())
    self.assertEqual(
        [self.points['Twin Peaks']], day_visits[2].GetPoints())

    self.assertEqual("""Date: 2014-09-01
Cost: 13.50
Walking from Hotel to Golden Gate Bridge from 09:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Visiting point "Golden Gate Bridge" from 16:00:00 to 16:30:00
Walking from Golden Gate Bridge to Restaurant from 16:30:00 to 22:30:00
Date: 2014-09-02
Cost: 11.00
Walking from Hotel to Ferry Biulding from 09:00:00 to 10:00:00
Visiting point "Ferry Biulding" from 10:00:00 to 11:00:00
Walking from Ferry Biulding to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Union Square from 16:00:00 to 18:00:00
Visiting point "Union Square" from 18:00:00 to 19:00:00
Walking from Union Square to Restaurant from 19:00:00 to 20:00:00
Date: 2014-09-03
Cost: 6.50
Walking from Hotel to Twin Peaks from 09:00:00 to 12:00:00
Visiting point "Twin Peaks" from 12:00:00 to 12:30:00
Having lunch from 12:30:00 to 13:30:00
Walking from Twin Peaks to Restaurant from 13:30:00 to 15:30:00
Total cost: 31.00""", str(city_visit_best))
    self.assertEqual([], point_left)


if __name__ == '__main__':
    unittest.main()
