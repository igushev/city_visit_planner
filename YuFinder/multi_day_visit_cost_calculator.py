import Yusi
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface,\
  DayVisitCostCalculatorGeneratorInterface


class MultiDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  """Calculates the best among DayVisitCostCalculators.
  
  Keeps track of several DayVisitCostCalculators and chooses the best.
  """

  def __init__(self, calculators):
    self.calculators = calculators

  def Copy(self):
    return self.__class__(
        [calculator.Copy() for calculator in self.calculators])

  def PushPoint(self, point):
    # Must create a list since any() would skip all calculator after first
    # successful push.
    return any([calculator.PushPoint(point) for calculator in self.calculators])

  def FinalizedCost(self):
    return min(calculator.FinalizedCost() for calculator in self.calculators)

  def _GetMinIndex(self):
    # Get index of calculator with minimum FinalizedCost().
    min_index, _ = min(enumerate(self.calculators),
                       key=lambda (_, calculator): calculator.FinalizedCost())
    return min_index

  def FinalizedDayVisit(self):
    min_index = self._GetMinIndex()
    return self.calculators[min_index].FinalizedDayVisit()

  def GetPointsLeft(self):
    min_index = self._GetMinIndex()
    return self.calculators[min_index].GetPointsLeft()


class MultiDayVisitCostCalculatorGenerator(
    DayVisitCostCalculatorGeneratorInterface):
  
  def __init__(self, calculator_generators):
    self.calculator_generators = calculator_generators
    
  def Generate(self, day_visit_parameters):
    return MultiDayVisitCostCalculator(
        [calculator_generator.Generate(day_visit_parameters)
         for calculator_generator in self.calculator_generators])
