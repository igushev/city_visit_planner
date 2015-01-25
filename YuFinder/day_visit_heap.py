from collections import namedtuple


PointsCalculator = namedtuple('PointsCalculator', 'Points Calculator')


class DayVisitHeap(object):
  
  def __init__(self, max_count):
    self.max_count = max_count
    self._points_calculator_list = []
    self._invariant = True

  def Append(self, points_calculator):
    assert isinstance(points_calculator, PointsCalculator)
    if self._points_calculator_list:
      assert (len(self._points_calculator_list[0].Points) ==
              len(points_calculator.Points)), (
                  'Points count must be the same in the all heap')
    self._points_calculator_list.append(points_calculator)
    self._invariant = False

  def Shrink(self):
    self._points_calculator_list = (
        sorted(self._points_calculator_list,
           key=lambda points_calculator: (
               points_calculator.Calculator.FinalizedCost()))[:self.max_count])
    self._invariant = True

  def GetPointsCalculatorList(self):
    assert self._invariant, (
        'PointsCalculator list cannot be returned. Please call Shrink first.')
    return self._points_calculator_list

  def Size(self):
    return len(self._points_calculator_list)

  def Clear(self):
    self._points_calculator_list = []
    self._invariant = True    
