from Yusi.YuRanker.points_ranker import PointsRankerInterface
from Yusi.YuRouter.city_visit_router import CityVisitRouterInterface
from Yusi.YuPoint.city_visit import CityVisitParametersInterface,\
  CityVisitInterface
from Yusi.YuPoint.point import PointInterface
from Yusi.YuPoint.database_connection import DatabaseConnectionInterface


class CityVisitFinderInterface(object):
  """Abstract class which finds CityVisit."""

  def FindCityVisit(self, city_visit_parameters):
    """Find CityVisit with appropriate points by given city_visit_parameters."""
    raise NotImplemented()


class CityVisitFinder(CityVisitFinderInterface):
  """Finds CityVisit by getting points, ranking them and routing."""
  
  def __init__(self, database_connection, points_ranker, city_visit_router):
    assert isinstance(database_connection, DatabaseConnectionInterface)
    assert isinstance(points_ranker, PointsRankerInterface)
    assert isinstance(city_visit_router, CityVisitRouterInterface)

    self.database_connection = database_connection
    self.points_ranker = points_ranker
    self.city_visit_router = city_visit_router

  def FindCityVisit(self, city_visit_parameters,
                    city_visit_accumulator_generator):
    assert isinstance(city_visit_parameters, CityVisitParametersInterface)
    
    points_input = (
        self.database_connection.GetPoints(
            city_visit_parameters.visit_location))
    for point_input in  points_input:
      assert isinstance(point_input, PointInterface)

    points_ranked = self.points_ranker.RankPoints(
        points_input, city_visit_parameters)
    for point_ranked in points_ranked:
      assert isinstance(point_ranked, PointInterface)
    
    city_visit, points_left = self.city_visit_router.RouteCityVisit(
        points_ranked, city_visit_parameters.day_visit_parameterss,
        city_visit_accumulator_generator)
    assert isinstance(city_visit, CityVisitInterface)
    for point_left in points_left:
      assert isinstance(point_left, PointInterface)

    return city_visit
