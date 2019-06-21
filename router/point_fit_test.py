import datetime
import unittest

from data import point
from data import city_visit
from router import point_fit as point_fit_


class PointFitTest(unittest.TestCase):

  def setUp(self):
    # Ferry Building, San Francisco.
    self.ferry_building_operating_hours = point.OperatingHours(
        datetime.time(9, 0, 0), datetime.time(18, 0, 0))
    # Pier 39, San Francisco.
    self.pier_39_operating_hours = point.OperatingHours(
        datetime.time(10, 0, 0), datetime.time(22, 0, 0))
    # Golden Gate Bridge, San Francisco.
    self.golden_gate_bridge_operating_hours = None
    
    
    self.early_morning_start_end_datetime = city_visit.StartEndDatetime(
        datetime.datetime(2014, 9, 1, 9, 0, 0),
        datetime.datetime(2014, 9, 1, 12, 0, 0))
    self.late_everning_start_end_datetime = city_visit.StartEndDatetime(
        datetime.datetime(2014, 9, 1, 18, 0, 0),
        datetime.datetime(2014, 9, 1, 21, 0, 0))
    self.after_midnight_start_end_datetime = city_visit.StartEndDatetime(
        datetime.datetime(2014, 9, 1, 0, 0, 0),
        datetime.datetime(2014, 9, 1, 3, 0, 0))

    super(PointFitTest, self).setUp()

  def testIfPointFitGeneral(self):
    point_fit = point_fit_.SimplePointFit()
    self.assertEqual(True, point_fit.IfPointFit(
        self.early_morning_start_end_datetime,
        self.ferry_building_operating_hours))  # Left border.
    self.assertEqual(False, point_fit.IfPointFit(
        self.late_everning_start_end_datetime,
        self.ferry_building_operating_hours))  # Right border.
    self.assertEqual(False, point_fit.IfPointFit(
        self.after_midnight_start_end_datetime,
        self.ferry_building_operating_hours))  # No overlap.
    self.assertEqual(False, point_fit.IfPointFit(
        self.early_morning_start_end_datetime,
        self.pier_39_operating_hours))  # Partial overlap.
    self.assertEqual(True, point_fit.IfPointFit(
        self.late_everning_start_end_datetime,
        self.pier_39_operating_hours))  # Fully inside.
    self.assertEqual(False, point_fit.IfPointFit(
        self.after_midnight_start_end_datetime,
        self.pier_39_operating_hours))  # No overlap.
    self.assertEqual(True, point_fit.IfPointFit(
        self.early_morning_start_end_datetime,
        self.golden_gate_bridge_operating_hours))
    self.assertEqual(True, point_fit.IfPointFit(
        self.late_everning_start_end_datetime,
        self.golden_gate_bridge_operating_hours))
    self.assertEqual(True, point_fit.IfPointFit(
        self.after_midnight_start_end_datetime,
        self.golden_gate_bridge_operating_hours))


if __name__ == '__main__':
    unittest.main()
