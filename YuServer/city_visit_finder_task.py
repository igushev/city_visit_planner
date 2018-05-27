from Yusi.YuUtils import task_util

from Yusi.YuRouter import city_visit_accumulator


class CityVisitAccumulatorConn(city_visit_accumulator.CityVisitAccumulatorInterface):
  """Accumulates and sends CityVisit and points left.""" 

  def __init__(self, worker_conn):
    self.worker_conn = worker_conn
    self.day_visits = []
    self.day_visit_parameterss = []
    self.points_left = []

  def AddDayVisits(self, day_visits, day_visit_parameterss):
    assert len(day_visits) == len(day_visit_parameterss)
    self.worker_conn.send((day_visits, False))
    self.day_visits.extend(day_visits)
    self.day_visit_parameterss.extend(day_visit_parameterss)
  
  def AddPointsLeft(self, points_left):
    self.points_left.extend(points_left)
  
  def Result(self, city_visit_points_left_generator):
    city_visit_points_left = (
        city_visit_points_left_generator.Generate(
            self.day_visits, self.day_visit_parameterss, self.points_left))
    self.worker_conn.send(
        (city_visit_points_left.city_visit.city_visit_summary, True))
    return (city_visit_points_left.city_visit,
            city_visit_points_left.points_left)


class CityVisitAccumulatorConnGenerator(city_visit_accumulator.CityVisitAccumulatorGeneratorInterface):
  """Returns every time new clean instance of CityVisitAccumulatorConn."""

  def __init__(self, worker_conn):
    self.worker_conn = worker_conn

  def Generate(self):
    return CityVisitAccumulatorConn(self.worker_conn)


class CityVisitFinderTaskWorker(task_util.TaskWorkerInterface):
  """Class which executes a CityVisitFinder task.""" 

  def __init__(self, city_visit_finder, worker_conn):
    self.city_visit_finder = city_visit_finder
    self.worker_conn = worker_conn

  def Start(self, city_visit_parameters):
    city_visit_accumulator_generator = (
        CityVisitAccumulatorConnGenerator(self.worker_conn))
    self.city_visit_finder.FindCityVisit(
        city_visit_parameters, city_visit_accumulator_generator)


class CityVisitFinderTaskWorkerGenerator(task_util.TaskWorkerGeneratorInterface):
  """Class which generates CityVisitFinderTaskWorker objects.""" 

  def __init__(self, city_visit_finder):
    self.city_visit_finder = city_visit_finder

  def Generate(self, worker_conn):
    return CityVisitFinderTaskWorker(self.city_visit_finder, worker_conn)


