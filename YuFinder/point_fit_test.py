import datetime
import unittest

from Yusi.YuFinder.point import OperatingHours
from Yusi.YuFinder.point_fit import SimplePointFit
from Yusi.YuFinder.city_visit import StartEndDatetime


# Ferry Biulding, San Francisco.
ferry_biulding_operating_hours = OperatingHours(datetime.time(9, 0, 0), datetime.time(18, 0, 0))
# Pier 39, San Francisco.
pier_39_operating_hours = OperatingHours(datetime.time(10, 0, 0), datetime.time(22, 0, 0))
# Golden Gate Bridge, San Francisco.
golden_gate_bridge_operating_hours = None


early_morning_start_end_datetime = StartEndDatetime(
    datetime.datetime(2014, 9, 1, 9, 0, 0), datetime.datetime(2014, 9, 1, 12, 0, 0))
late_everning_start_end_datetime = StartEndDatetime(
    datetime.datetime(2014, 9, 1, 18, 0, 0), datetime.datetime(2014, 9, 1, 21, 0, 0))
after_midnight_start_end_datetime = StartEndDatetime(
    datetime.datetime(2014, 9, 1, 0, 0, 0), datetime.datetime(2014, 9, 1, 3, 0, 0))


class PointFitTest(unittest.TestCase):

  def testIfPointFitGeneral(self):
    point_fit = SimplePointFit()
    self.assertEqual(True, point_fit.IfPointFit(
        early_morning_start_end_datetime, ferry_biulding_operating_hours))  # Left border.
    self.assertEqual(False, point_fit.IfPointFit(
        late_everning_start_end_datetime, ferry_biulding_operating_hours))  # Right border.
    self.assertEqual(False, point_fit.IfPointFit(
        after_midnight_start_end_datetime, ferry_biulding_operating_hours))  # No overlap.
    self.assertEqual(False, point_fit.IfPointFit(
        early_morning_start_end_datetime, pier_39_operating_hours))  # Partial overlap.
    self.assertEqual(True, point_fit.IfPointFit(
        late_everning_start_end_datetime, pier_39_operating_hours))  # Fully inside.
    self.assertEqual(False, point_fit.IfPointFit(
        after_midnight_start_end_datetime, pier_39_operating_hours))  # No overlap.
    self.assertEqual(True, point_fit.IfPointFit(
        early_morning_start_end_datetime, golden_gate_bridge_operating_hours))
    self.assertEqual(True, point_fit.IfPointFit(
        late_everning_start_end_datetime, golden_gate_bridge_operating_hours))
    self.assertEqual(True, point_fit.IfPointFit(
        after_midnight_start_end_datetime, golden_gate_bridge_operating_hours))


if __name__ == '__main__':
    unittest.main()
