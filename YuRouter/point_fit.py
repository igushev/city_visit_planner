from Yusi.YuPoint.city_visit import StartEndDatetimeInterface
from Yusi.YuPoint.point import OperatingHoursInterface


class PointFitInterface(object):
  """Abstract class which checks if point can be visited."""

  def IfPointFit(self, start_end_datetime, operating_hours):
    """Return if point with given operating_hours can be visited during given
    start_end_datetime."""
    raise NotImplemented


# NOTE(igushev): This class works only with StartEndDatetime of
# StartEndDatetimeInterface implementation and OperatingHours implementation
# of OperatingHoursInterface.
class SimplePointFit(PointFitInterface):
  """Checks if point can be visited in a very straightforward way. Doesn't know
  about days of week, seasons, etc."""

  def IfPointFit(self, start_end_datetime, operating_hours):
    assert isinstance(start_end_datetime, StartEndDatetimeInterface)
    if operating_hours is not None:
      assert isinstance(operating_hours, OperatingHoursInterface)
    
    # If it's 24/7, point can be visited regardless of start_end_datetime.
    if not operating_hours:
      return True
    # If start and end are different days, point can't be visited.
    if start_end_datetime.start.date() != start_end_datetime.end.date():
      return False
    if (start_end_datetime.start.time() >= operating_hours.opens and
        start_end_datetime.end.time() <= operating_hours.closes):
      return True
    return False

