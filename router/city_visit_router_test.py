import datetime
import unittest

from data import city_visit
from router import day_visit_cost_calculator
from router import city_visit_router
from router import cost_accumulator
from router import point_fit as point_fit_
from router import day_visit_router as day_visit_router_
from router import city_visit_points_left
from router import test_util
from router import points_queue
from router import city_visit_accumulator


class CityVisitRouterTest(unittest.TestCase):

  @staticmethod
  def GetDayVisitParameters(start_datetime, end_datetime):
    return city_visit.DayVisitParameters(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        lunch_start_datetime=datetime.datetime(
            start_datetime.year, start_datetime.month, start_datetime.day,
            13, 0, 0),
        lunch_hours=1.,
        start_coordinates=test_util.MockCoordinates('Hotel'),
        end_coordinates=test_util.MockCoordinates('Restaurant'))

  def setUp(self):
    no_point_visit_factor = 0.
    no_point_visit_const = 1000.
    unused_time_factor = 0.01
    day_visit_heap_size = 1000
    shard_num_days = 2
    max_depth = 1
    city_visit_heap_size = 10
    max_non_pushed_points = 3
    self.points = test_util.MockPoints()
    move_calculator = test_util.MockMoveCalculator()
    point_fit = point_fit_.SimplePointFit()
    cost_accumulator_generator=cost_accumulator.FactorCostAccumulatorGenerator(
        no_point_visit_factor=no_point_visit_factor,
        no_point_visit_const=no_point_visit_const,
        unused_time_factor=unused_time_factor)
    day_visit_cost_calculator_generator = day_visit_cost_calculator.DayVisitCostCalculatorGenerator(
        move_calculator=move_calculator,
        point_fit=point_fit,
        cost_accumulator_generator=cost_accumulator_generator)
    day_visit_router = day_visit_router_.DayVisitRouter(
        calculator_generator=day_visit_cost_calculator_generator,
        day_visit_heap_size=day_visit_heap_size)
    city_visit_points_left_generator = city_visit_points_left.CityVisitPointsLeftGenerator(
        cost_accumulator_generator=cost_accumulator_generator)
    points_queue_generator = points_queue.OneByOnePointsQueueGenerator()
    self.city_visit_router = city_visit_router.CityVisitRouter(
        day_visit_router=day_visit_router,
        city_visit_points_left_generator=city_visit_points_left_generator,
        points_queue_generator=points_queue_generator,
        shard_num_days=shard_num_days,
        max_depth=max_depth,
        city_visit_heap_size=city_visit_heap_size,
        max_non_pushed_points=max_non_pushed_points,
        num_processes=None)
    self.city_visit_accumulator_generator = city_visit_accumulator.CityVisitAccumulatorGenerator()
    super(CityVisitRouterTest, self).setUp()

  def testOneShortDay(self):
    day_visit_parameterss = [
        CityVisitRouterTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 1, 17, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0))]

    # Union Square would fit but it's after 3 failed points.
    city_visit_best, point_left = self.city_visit_router.RouteCityVisit(
        [self.points['Twin Peaks'],
         self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square']],
        day_visit_parameterss,
        self.city_visit_accumulator_generator)
    day_visits = city_visit_best.day_visits
    self.assertEqual(1, len(day_visits))
    self.assertEqual([], day_visits[0].GetPoints())
    self.assertEqual("""Date: 2014-09-01
Walking from Hotel to Restaurant from 17:00:00 to 18:00:00
Cost: 2.80
Price: 0.00
Total cost: 5002.80
Total price: 0.00""", str(city_visit_best))
    self.assertEqual(
        [self.points['Twin Peaks'],
         self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square']],
        point_left)

  def testOneDay(self):
    day_visit_parameterss = [
        CityVisitRouterTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0))]

    city_visit_best, point_left = self.city_visit_router.RouteCityVisit(
        [self.points['Twin Peaks'],
         self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square']],
        day_visit_parameterss,
        self.city_visit_accumulator_generator)
    day_visits = city_visit_best.day_visits
    self.assertEqual(1, len(day_visits))
    self.assertEqual(
        [self.points['Ferry Building'],
         self.points['Union Square'],
         self.points['Twin Peaks']], day_visits[0].GetPoints())

    self.assertEqual("""Date: 2014-09-01
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Union Square from 11:00:00 to 13:00:00
Having lunch from 13:00:00 to 14:00:00
Visiting point "Union Square" from 14:00:00 to 15:00:00
Walking from Union Square to Twin Peaks from 15:00:00 to 18:00:00
Visiting point "Twin Peaks" from 18:00:00 to 18:30:00
Walking from Twin Peaks to Restaurant from 18:30:00 to 20:30:00
Cost: 11.80
Price: 0.00
Total cost: 2011.80
Total price: 0.00""", str(city_visit_best))
    self.assertEqual(
        [self.points['Pier 39'],
         self.points['Golden Gate Bridge']],
        point_left)

  def testOneLongDayOneShortDay(self):
    day_visit_parameterss = [
        CityVisitRouterTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 1, 23, 0, 0)),
        CityVisitRouterTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0))]

    city_visit_best, point_left = self.city_visit_router.RouteCityVisit(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square']],
        day_visit_parameterss,
        self.city_visit_accumulator_generator)

    day_visits = city_visit_best.day_visits
    self.assertEqual(2, len(day_visits))
    self.assertEqual(
        [self.points['Golden Gate Bridge']], day_visits[0].GetPoints())
    self.assertEqual(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Union Square']], day_visits[1].GetPoints())
    
    self.assertEqual("""Date: 2014-09-01
Walking from Hotel to Golden Gate Bridge from 09:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Visiting point "Golden Gate Bridge" from 16:00:00 to 16:30:00
Walking from Golden Gate Bridge to Restaurant from 16:30:00 to 22:30:00
Cost: 13.80
Price: 0.00
Date: 2014-09-02
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Union Square from 16:00:00 to 18:00:00
Visiting point "Union Square" from 18:00:00 to 19:00:00
Walking from Union Square to Restaurant from 19:00:00 to 20:00:00
Cost: 11.60
Price: 0.00
Total cost: 25.40
Total price: 0.00""", str(city_visit_best))
    self.assertEqual([], point_left)

  def testTwoDays(self):
    day_visit_parameterss = [
        CityVisitRouterTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0)),
        CityVisitRouterTest.GetDayVisitParameters(
            start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
            end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0))]

    city_visit_best, point_left = self.city_visit_router.RouteCityVisit(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square'],
         self.points['Twin Peaks']],
        day_visit_parameterss,
        self.city_visit_accumulator_generator)
    
    day_visits = city_visit_best.day_visits
    self.assertEqual(2, len(day_visits))
    self.assertEqual(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Union Square']], day_visits[0].GetPoints())
    self.assertEqual(
        [self.points['Twin Peaks']], day_visits[1].GetPoints())
    
    self.assertEqual("""Date: 2014-09-01
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Union Square from 16:00:00 to 18:00:00
Visiting point "Union Square" from 18:00:00 to 19:00:00
Walking from Union Square to Restaurant from 19:00:00 to 20:00:00
Cost: 11.60
Price: 0.00
Date: 2014-09-02
Walking from Hotel to Twin Peaks from 09:00:00 to 12:00:00
Visiting point "Twin Peaks" from 12:00:00 to 12:30:00
Having lunch from 12:30:00 to 13:30:00
Walking from Twin Peaks to Restaurant from 13:30:00 to 15:30:00
Cost: 9.80
Price: 0.00
Total cost: 1021.40
Total price: 0.00""", str(city_visit_best))
    self.assertEqual(
        [self.points['Golden Gate Bridge']],
        point_left)

  def testTwoDaysOneShortDay(self):
    day_visit_parameterss = [
      CityVisitRouterTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 1, 23, 0, 0)),
      CityVisitRouterTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0)),
      CityVisitRouterTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 3, 17, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 3, 21, 0, 0))]                         

    city_visit_best, point_left = self.city_visit_router.RouteCityVisit(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square'],
         self.points['Twin Peaks']],
        day_visit_parameterss,
        self.city_visit_accumulator_generator)

    day_visits = city_visit_best.day_visits
    self.assertEqual(3, len(day_visits))
    self.assertEqual(
        [self.points['Twin Peaks']], day_visits[0].GetPoints())
    self.assertEqual(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Union Square']], day_visits[1].GetPoints())
    self.assertEqual([], day_visits[2].GetPoints())

    self.assertEqual("""Date: 2014-09-01
Walking from Hotel to Twin Peaks from 09:00:00 to 12:00:00
Visiting point "Twin Peaks" from 12:00:00 to 12:30:00
Having lunch from 12:30:00 to 13:30:00
Walking from Twin Peaks to Restaurant from 13:30:00 to 15:30:00
Cost: 11.00
Price: 0.00
Date: 2014-09-02
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Union Square from 16:00:00 to 18:00:00
Visiting point "Union Square" from 18:00:00 to 19:00:00
Walking from Union Square to Restaurant from 19:00:00 to 20:00:00
Cost: 11.60
Price: 0.00
Date: 2014-09-03
Walking from Hotel to Restaurant from 17:00:00 to 18:00:00
Cost: 2.80
Price: 0.00
Total cost: 1025.40
Total price: 0.00""", str(city_visit_best))
    self.assertEqual(
        [self.points['Golden Gate Bridge']],
        point_left)

  def testThreeDays(self):
    day_visit_parameterss = [
      CityVisitRouterTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 1, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 1, 21, 0, 0)),
      CityVisitRouterTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 2, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 2, 21, 0, 0)),
      CityVisitRouterTest.GetDayVisitParameters(
          start_datetime=datetime.datetime(2014, 9, 3, 9, 0, 0),
          end_datetime=datetime.datetime(2014, 9, 3, 23, 0, 0))]                         

    city_visit_best, point_left = self.city_visit_router.RouteCityVisit(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Golden Gate Bridge'],
         self.points['Union Square'],
         self.points['Twin Peaks']],
        day_visit_parameterss,
        self.city_visit_accumulator_generator)

    day_visits = city_visit_best.day_visits
    self.assertEqual(3, len(day_visits))
    self.assertEqual(
        [self.points['Ferry Building'],
         self.points['Pier 39'],
         self.points['Union Square']], day_visits[0].GetPoints())
    self.assertEqual(
        [self.points['Twin Peaks']], day_visits[1].GetPoints())
    self.assertEqual(
        [self.points['Golden Gate Bridge']], day_visits[2].GetPoints())

    self.assertEqual("""Date: 2014-09-01
Walking from Hotel to Ferry Building from 09:00:00 to 10:00:00
Visiting point "Ferry Building" from 10:00:00 to 11:00:00
Walking from Ferry Building to Pier 39 from 11:00:00 to 12:00:00
Having lunch from 12:00:00 to 13:00:00
Visiting point "Pier 39" from 13:00:00 to 16:00:00
Walking from Pier 39 to Union Square from 16:00:00 to 18:00:00
Visiting point "Union Square" from 18:00:00 to 19:00:00
Walking from Union Square to Restaurant from 19:00:00 to 20:00:00
Cost: 11.60
Price: 0.00
Date: 2014-09-02
Walking from Hotel to Twin Peaks from 09:00:00 to 12:00:00
Visiting point "Twin Peaks" from 12:00:00 to 12:30:00
Having lunch from 12:30:00 to 13:30:00
Walking from Twin Peaks to Restaurant from 13:30:00 to 15:30:00
Cost: 9.80
Price: 0.00
Date: 2014-09-03
Walking from Hotel to Golden Gate Bridge from 09:00:00 to 15:00:00
Having lunch from 15:00:00 to 16:00:00
Visiting point "Golden Gate Bridge" from 16:00:00 to 16:30:00
Walking from Golden Gate Bridge to Restaurant from 16:30:00 to 22:30:00
Cost: 13.80
Price: 0.00
Total cost: 35.20
Total price: 0.00""", str(city_visit_best))
    self.assertEqual([], point_left)


if __name__ == '__main__':
    unittest.main()
