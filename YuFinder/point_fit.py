class SimplePointFit(object):
  """Defines if a point can be visited by given visit time and given operating hours."""

  def IfPointFit(self, start_end_datetime, operating_hours):
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

