from data import city_visit
from ranker import rank_adjuster_interface


# NOTE(igushev): This class works only with AgeGroup implementation of
# AgeGroupInterface.
class AgeGroupRankAdjuster(rank_adjuster_interface.RankAdjusterInterface):
  """Adjusts rank of points by age group."""

  @staticmethod
  def _PointScoreMult(point_names_age_groups, parameters_names_age_groups):
    return (
        sum(max(age_group, 1) *
            max(point_names_age_groups[name], 1)
            for name, age_group in parameters_names_age_groups.items()) /
        float(100 * 100) /
        len(parameters_names_age_groups))

  def AdjustRank(self, score_points, city_visit_parameters):
    for score_point in score_points:
      assert isinstance(score_point, rank_adjuster_interface.ScorePoint)
    assert isinstance(city_visit_parameters, city_visit.CityVisitParametersInterface)
    
    parameters_names_age_groups = (
        city_visit_parameters.age_group.GetNamesAgeGroups())
    result_score_points = []
    for score, point in score_points:
      point_names_age_groups = point.age_group.GetNamesAgeGroups()
      point_score_mult = AgeGroupRankAdjuster._PointScoreMult(
          point_names_age_groups, parameters_names_age_groups)
      result_score_points.append(rank_adjuster_interface.ScorePoint(score * point_score_mult, point))
    return result_score_points
