import time
import unittest

from Yusi.YuFinder.city_visit_finder import CityVisitFinderInterface
from Yusi.YuRouter.city_visit_points_left import CityVisitPointsLeftGeneratorInterface,\
  CityVisitPointsLeft
from Yusi.YuPoint.city_visit import CityVisit, DayVisitParametersInterface,\
  CityVisitParametersInterface, DayVisitInterface, CityVisitSummaryInterface
from Yusi.YuUtils.task_utils import TaskManager
from Yusi.YuServer.city_visit_finder_task import CityVisitFinderTaskWorkerGenerator
from Yusi.YuPoint.point import PointInterface


class MockPoint(PointInterface):
  
  def __init__(self, name):
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class MockDayVisitParameters(DayVisitParametersInterface):
  
  def __init__(self, name):
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class MockCityVisitParameters(CityVisitParametersInterface):
  
  def __init__(self, name):
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class MockDayVisit(DayVisitInterface):
  
  def __init__(self, name):
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class MockCityVisitSummary(CityVisitSummaryInterface):
  
  def __init__(self, name):
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class MockCityVisitPointsLeftGenerator(CityVisitPointsLeftGeneratorInterface):

  def __init__(self, test_obj, day_visits_expected,
               day_visit_parameterss_expected, points_left_expected,
               city_visit_summary):
    self.test_obj = test_obj
    self.day_visits_expected = day_visits_expected
    self.day_visit_parameterss_expected = day_visit_parameterss_expected
    self.points_left_expected = points_left_expected
    self.city_visit_summary = city_visit_summary

  def Generate(self, day_visits, day_visit_parameterss, points_left):
    self.test_obj.assertEqual(self.day_visits_expected, day_visits)
    self.test_obj.assertEqual(self.day_visit_parameterss_expected,
                              day_visit_parameterss)
    self.test_obj.assertEqual(self.points_left_expected, points_left)
    city_visit = CityVisit(day_visits, self.city_visit_summary)
    return CityVisitPointsLeft(city_visit, self.points_left_expected)    


class MockCityVisitFinder(CityVisitFinderInterface):

  def __init__(self, test_obj, city_visit_parameters_expected,
               day_visits_day_visit_parameterss_list, points_left,
               city_visit_points_left_generator):
    self.test_obj = test_obj
    self.city_visit_parameters_expected = city_visit_parameters_expected
    self.day_visits_day_visit_parameterss_list = (
        day_visits_day_visit_parameterss_list)
    self.points_left = points_left
    self.city_visit_points_left_generator = city_visit_points_left_generator

  def FindCityVisit(self, city_visit_parameters,
                    city_visit_accumulator_generator):
    self.test_obj.assertEqual(self.city_visit_parameters_expected,
                              city_visit_parameters)
    city_visit_accumulator = city_visit_accumulator_generator.Generate()

    for day_visits, day_visit_parameterss in (
        self.day_visits_day_visit_parameterss_list):
      city_visit_accumulator.AddDayVisits(day_visits, day_visit_parameterss)
    city_visit_accumulator.AddPointsLeft(self.points_left)

    city_visit, points_left = (
        city_visit_accumulator.Result(self.city_visit_points_left_generator))

    return city_visit


class CityVisitFinderTaskWorkerTest(unittest.TestCase):
  
  def testGeneral(self):
    city_visit_parameters = MockCityVisitParameters('city_visit_parameters')
    
    day_visit_1 = MockDayVisit('day_visit_1')
    day_visit_2 = MockDayVisit('day_visit_2')
    day_visit_3 = MockDayVisit('day_visit_3')
    day_visits = [day_visit_1, day_visit_2, day_visit_3]
    day_visit_parameters_1 = MockDayVisitParameters('day_visit_parameters_1')
    day_visit_parameters_2 = MockDayVisitParameters('day_visit_parameters_2')
    day_visit_parameters_3 = MockDayVisitParameters('day_visit_parameters_3')
    day_visit_parameterss = [
        day_visit_parameters_1, day_visit_parameters_2, day_visit_parameters_3]
    point_left_1 = MockPoint('point_left_1')
    point_left_2 = MockPoint('point_left_2')
    points_left = [point_left_1, point_left_2]
    
    city_visit_summary = MockCityVisitSummary('city_visit_summary')

    city_visit_points_left_generator = (
        MockCityVisitPointsLeftGenerator(
            self, day_visits, day_visit_parameterss, points_left,
            city_visit_summary))
    
    city_visit_finder = (
        MockCityVisitFinder(
            self,
            city_visit_parameters,
            [([day_visit_1, day_visit_2],
              [day_visit_parameters_1, day_visit_parameters_2]),
             ([day_visit_3], [day_visit_parameters_3])],
            points_left,
            city_visit_points_left_generator))

    city_visit_finder_task_worker_generator = (
        CityVisitFinderTaskWorkerGenerator(city_visit_finder))
    task_manager = TaskManager(city_visit_finder_task_worker_generator, 1.0)
    
    task_id = task_manager.Start(city_visit_parameters)
    
    time.sleep(0.25)
    day_visits_actual = list(task_manager.Read(task_id))
    self.assertEqual([[day_visit_1, day_visit_2],
                      [day_visit_3],
                      city_visit_summary],
                     day_visits_actual)


if __name__ == '__main__':
    unittest.main()
