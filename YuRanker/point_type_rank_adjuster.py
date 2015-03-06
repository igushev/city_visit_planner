from Yusi.YuRanker.rank_adjuster_interface import RankAdjusterInterface,\
  ScorePoint
from Yusi.YuPoint.city_visit import CityVisitParametersInterface


class PointTypeRankAdjuster(RankAdjusterInterface):
  """Adjusts rank of points by point types."""

  @staticmethod
  def _PointScoreMult(point_names_point_types, parameters_names_point_types):
    return (
        sum(max(point_type, 1) *
            max(point_names_point_types[name], 1)
            for name, point_type in parameters_names_point_types.iteritems()) /
        float(100 * 100) /
        len(parameters_names_point_types))

  def AdjustRank(self, score_points, city_visit_parameters):
    for score_point in score_points:
      assert isinstance(score_point, ScorePoint)
    assert isinstance(city_visit_parameters, CityVisitParametersInterface)
    
    parameters_names_point_types = (
        city_visit_parameters.point_type.GetNamesPointTypes())
    result_score_points = []
    for score, point in score_points:
      point_names_point_types = point.point_type.GetNamesPointTypes()
      point_score_mult = PointTypeRankAdjuster._PointScoreMult(
          point_names_point_types, parameters_names_point_types)
      result_score_points.append(ScorePoint(score * point_score_mult, point))
    return result_score_points
