import Yusi
from Yusi.YuFinder.day_visit_cost_calculator_interface import DayVisitCostCalculatorInterface,\
  DayVisitCostCalculatorGeneratorInterface


class MultiDayVisitCostCalculator(DayVisitCostCalculatorInterface):
  """Calculates the best among DayVisitCostCalculators.
  
  Keeps track of several DayVisitCostCalculators and chooses the best.
  """

  def __init__(self, calculators):
    self.calculators = calculators

  def PushPoint(self, point):
    assert self.calculators
    self.calculators = [calculator
                        for calculator in self.calculators
                        if calculator.PushPoint(point)]
    return bool(self.calculators)

  def CanFinalize(self):
    assert self.calculators
    return any(calculator.CanFinalize() for calculator in self.calculators)
  
  def FinalizedCost(self):
    assert self.CanFinalize()
    return min(calculator.FinalizedCost()
               for calculator in self.calculators
               if calculator.CanFinalize())

  def FinalizedDayVisit(self):
    assert self.CanFinalize()
    # Get calculators that can be finalized.
    calculators = [calculator
                   for calculator in self.calculators
                   if calculator.CanFinalize()]
    # Get index of calculator with minimum FinalizedCost().
    min_index, _ = min(enumerate(calculators),
                       key=lambda (_, calculator): calculator.FinalizedCost())
    # Get finalized DayVisit.
    return calculators[min_index].FinalizedDayVisit()
  
  def Count(self):
    assert self.calculators
    return len(self.calculators)


class MultiDayVisitCostCalculatorGenerator(DayVisitCostCalculatorGeneratorInterface):
  
  def __init__(self, calculator_generators):
    self.calculator_generators = calculator_generators
    
  def Generate(self, day_visit_parameters):
    return MultiDayVisitCostCalculator(
        [calculator_generator.Generate(day_visit_parameters)
         for calculator_generator in self.calculator_generators])
