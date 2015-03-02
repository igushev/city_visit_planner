from Yusi.YuRanker.rank_adjuster_interface import RankAdjusterInterface,\
  ScorePoint


class AgeGroupRankAdjuster(RankAdjusterInterface):
  """Adjusts rank of points by age group."""

  @staticmethod
  def _PointScoreMult(point_names_age_groups, parameters_names_age_groups):
    return (
        sum(max(age_group, 1) *
            max(point_names_age_groups[name], 1)
            for name, age_group in parameters_names_age_groups.iteritems()) /
        float(100 * 100) /
        len(parameters_names_age_groups))

  def AdjustRank(self, score_points, city_visit_parameters):
    parameters_names_age_groups = (
        city_visit_parameters.age_group.GetNamesAgeGroups())
    result_score_points = []
    for score, point in score_points:
      point_names_age_groups = point.age_group.GetNamesAgeGroups()
      point_score_mult = AgeGroupRankAdjuster._PointScoreMult(
          point_names_age_groups, parameters_names_age_groups)
      result_score_points.append(ScorePoint(score * point_score_mult, point))
    return result_score_points
