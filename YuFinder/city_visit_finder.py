from Yusi.YuFinder.database_connection import DatabaseConnectionInterface
from Yusi.YuRanker.points_ranker import PointsRankerInterface
from Yusi.YuRouter.city_visit_router import CityVisitRouterInterface


class CityVisitFinder(object):
  
  def __init__(self, database_connection, points_ranker, city_visit_router):
    assert isinstance(database_connection, DatabaseConnectionInterface)
    assert isinstance(points_ranker, PointsRankerInterface)
    assert isinstance(city_visit_router, CityVisitRouterInterface)

    self.database_connection = database_connection
    self.points_ranker = points_ranker
    self.city_visit_router = city_visit_router

  def FindDayVisit(self, city_visit_parameters):
    points_input = self.database_connection.GetPoints(city_visit_parameters)
    points_ranked = self.points_ranker.RankPoints(
        points_input, city_visit_parameters)
    city_visit = self.city_visit_router.RouteCityVisit(
        points_ranked, city_visit_parameters.day_visit_parameterss)
    return city_visit
