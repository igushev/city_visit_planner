import datetime
import os

from config import config as config_


class PointsRankerRunner(object):
  
  def __init__(self):
    config = (
        config_.GetConfig(os.path.join(
            'config', 'runner.config')))
    self.points_ranker = config_.GetPointsRanker(config)
    
  def Run(self, points_input, city_visit_parameters):
    start = datetime.datetime.now()

    points_ranked = (
        self.points_ranker.RankPoints(points_input, city_visit_parameters))

    print('Input points: %s' %
          ', '.join(point.name for point in points_input))
    print('Points ranked: %s' %
          ', '.join(point_left.name for point_left in points_ranked))
    print('Elapsed time %s' % (datetime.datetime.now() - start))
