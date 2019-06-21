from ranker import points_ranker as points_ranker_
from router import city_visit_router as city_visit_router_
from data import city_visit as city_visit_
from data import point
from data import database_connection as database_connection_


class CityVisitFinderInterface(object):
  """Abstract class which finds CityVisit."""

  def FindCityVisit(self, city_visit_parameters,
                    city_visit_accumulator_generator):
    """Find CityVisit with appropriate points by given city_visit_parameters."""
    raise NotImplemented()


class CityVisitFinder(CityVisitFinderInterface):
  """Finds CityVisit by getting points, ranking them and routing."""
  
  def __init__(self, database_connection, points_ranker, city_visit_router):
    assert isinstance(database_connection, database_connection_.DatabaseConnectionInterface)
    assert isinstance(points_ranker, points_ranker_.PointsRankerInterface)
    assert isinstance(city_visit_router, city_visit_router_.CityVisitRouterInterface)

    self.database_connection = database_connection
    self.points_ranker = points_ranker
    self.city_visit_router = city_visit_router

  def FindCityVisit(self, city_visit_parameters,
                    city_visit_accumulator_generator):
    assert isinstance(city_visit_parameters, city_visit_.CityVisitParametersInterface)
    
    points_input = (
        self.database_connection.GetPoints(
            city_visit_parameters.visit_location))
    for point_input in  points_input:
      assert isinstance(point_input, point.PointInterface)

    points_ranked = self.points_ranker.RankPoints(
        points_input, city_visit_parameters)
    for point_ranked in points_ranked:
      assert isinstance(point_ranked, point.PointInterface)
    
    city_visit, points_left = self.city_visit_router.RouteCityVisit(
        points_ranked, city_visit_parameters.day_visit_parameterss,
        city_visit_accumulator_generator)
    assert isinstance(city_visit, city_visit_.CityVisitInterface)
    for point_left in points_left:
      assert isinstance(point_left, point.PointInterface)

    return city_visit
