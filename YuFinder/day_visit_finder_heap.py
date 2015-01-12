from collections import namedtuple


PointsCalculator = namedtuple('PointsCalculator', 'Points Calculator')


class DayVisitFinderHeapInterface(object):
  
  def Append(self):
    raise NotImplemented()
  
  def Shrink(self):
    raise NotImplemented()
  
  def GetPointsCalculatorList(self):
    raise NotImplemented()
  
  def Size(self):
    raise NotImplemented
  
  def Clear(self):
    raise NotImplemented

class DayVisitFinderHeapGeneratorInterface(object):
  
  def Generate(self):
    raise NotImplemented()
  
  
class EverythingDayVisitFinderHeap(DayVisitFinderHeapInterface):
  
  def __init__(self):
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
    # Since we keep everything, we just set _invariant to True
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


class EverythingDayVisitFinderHeapGenerator(DayVisitFinderHeapGeneratorInterface):
  
  def Generate(self):
    return EverythingDayVisitFinderHeap()