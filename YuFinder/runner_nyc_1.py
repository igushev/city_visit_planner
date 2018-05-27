from Yusi.YuPoint import point
from Yusi.YuPoint import city_visit
from Yusi.YuFinder import runner as finder_runner
from Yusi.YuRanker import runner as ranker_runner
from Yusi.YuRouter import runner as router_runner


def main():
  city_visit_finder_runner = finder_runner.CityVisitFinderRunner()
  visit_location = city_visit.VisitLocation('New York City')
  # 746 Ninth Ave, New York, NY 10019.
  start_end_coordinates = point.Coordinates(40.763582, -73.988470)
  first_day, last_day = 13, 16
  day_visit_parameterss = router_runner.GetDayVisitParameterss(start_end_coordinates, first_day, last_day)
  city_visit_parameters = ranker_runner.GetCityVisitParameters(visit_location, day_visit_parameterss)
  
  city_visit_finder_runner.Run(city_visit_parameters)


if __name__ == '__main__':
  main()
