import datetime

from data import city_visit
from data import point as point_


def GetCityVisitParameters(visit_location, day_visit_parameterss):
  parameters_point_types = point_.PointType(
      city_tours=90,
      landmarks=90,
      nature=10,
      museums=10,
      shopping=50,
      dining=50)

  parameters_age_groups = point_.AgeGroup(
      senior=None,
      adult=90,
      junior=None,
      child=None,
      toddlers=10)

  return city_visit.CityVisitParameters(
      visit_location=visit_location,
      day_visit_parameterss=day_visit_parameterss,
      point_type=parameters_point_types,
      age_group=parameters_age_groups)


def GetDayVisitParameterss(start_end_coordinates, first_day, last_day):
  def GetDayVisitParameters(day):
    return city_visit.DayVisitParameters(
        start_datetime=datetime.datetime(2015, 7, day, 10, 0, 0),
        end_datetime=datetime.datetime(2015, 7, day, 19, 0, 0),
        lunch_start_datetime=datetime.datetime(2015, 7, day, 14, 0, 0),
        lunch_hours=1.,
        start_coordinates=start_end_coordinates,
        end_coordinates=start_end_coordinates)

  return [GetDayVisitParameters(day) for day in range(first_day, last_day)]