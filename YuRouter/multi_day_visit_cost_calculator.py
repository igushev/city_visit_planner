import Yusi
from Yusi.YuRouter.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface,\
  DayVisitCostCalculatorGeneratorInterface
from Yusi.YuPoint.point import PointInterface
from Yusi.YuPoint.city_visit import DayVisitParametersInterface


class MultiDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  """Calculates the best among DayVisitCostCalculators.
  
  Keeps track of several DayVisitCostCalculators and chooses the best.
  """

  def __init__(self, calculators):
    for calculator in calculators:
      assert isinstance(calculator, DayVisitCostCalculatorInterface)

    self.calculators = calculators

  def Copy(self):
    return self.__class__(
        [calculator.Copy() for calculator in self.calculators])

  def PushPoint(self, point):
    assert isinstance(point, PointInterface)

    # Must create a list since any() would skip all calculator after first
    # successful push.
    return any([calculator.PushPoint(point) for calculator in self.calculators])

  def FinalizedCost(self):
    return min(calculator.FinalizedCost() for calculator in self.calculators)

  def _GetMinIndex(self):
    # Get index of calculator with minimum FinalizedCost().
    min_index, _ = min(enumerate(self.calculators),
                       key=lambda index_calculator: index_calculator[1].FinalizedCost())
    return min_index

  def FinalizedDayVisit(self):
    min_index = self._GetMinIndex()
    return self.calculators[min_index].FinalizedDayVisit()

  def GetPointsLeft(self):
    min_index = self._GetMinIndex()
    return self.calculators[min_index].GetPointsLeft()


class MultiDayVisitCostCalculatorGenerator(
    DayVisitCostCalculatorGeneratorInterface):
  """Returns every time new clean instance of MultiDayVisitCostCalculator."""
  
  def __init__(self, calculator_generators):
    for calculator_generator in calculator_generators:
      assert isinstance(calculator_generator,
                        DayVisitCostCalculatorGeneratorInterface)

    self.calculator_generators = calculator_generators
    
  def Generate(self, day_visit_parameters):
    assert isinstance(day_visit_parameters, DayVisitParametersInterface)

    return MultiDayVisitCostCalculator(
        [calculator_generator.Generate(day_visit_parameters)
         for calculator_generator in self.calculator_generators])
