from data import city_visit
from ranker import rank_adjuster_interface


# NOTE(igushev): This class works only with PointType implementation of
# PointTypeInterface.
class PointTypeRankAdjuster(rank_adjuster_interface.RankAdjusterInterface):
  """Adjusts rank of points by point types."""

  @staticmethod
  def _PointScoreMult(point_names_point_types, parameters_names_point_types):
    return (
        sum(max(point_type, 1) *
            max(point_names_point_types[name], 1)
            for name, point_type in parameters_names_point_types.items()) /
        float(100 * 100) /
        len(parameters_names_point_types))

  def AdjustRank(self, score_points, city_visit_parameters):
    for score_point in score_points:
      assert isinstance(score_point, rank_adjuster_interface.ScorePoint)
    assert isinstance(city_visit_parameters, city_visit.CityVisitParametersInterface)
    
    parameters_names_point_types = (
        city_visit_parameters.point_type.GetNamesPointTypes())
    result_score_points = []
    for score, point in score_points:
      point_names_point_types = point.point_type.GetNamesPointTypes()
      point_score_mult = PointTypeRankAdjuster._PointScoreMult(
          point_names_point_types, parameters_names_point_types)
      result_score_points.append(rank_adjuster_interface.ScorePoint(score * point_score_mult, point))
    return result_score_points
