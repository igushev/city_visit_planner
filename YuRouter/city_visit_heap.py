import hashlib
from Yusi.YuPoint.city_visit import DayVisitParametersInterface
from Yusi.YuRouter.city_visit_cost_calculator import CityVisitCostCalculatorInterface


class CityVisitHeap(object):
  """Keeps track of the best CityVisits.""" 

  def __init__(self, max_count, day_visit_parameterss):
    assert isinstance(max_count, int)
    for day_visit_parameters in day_visit_parameterss:
      assert isinstance(day_visit_parameters, DayVisitParametersInterface)

    self.max_count = max_count
    self.day_visit_parameterss = day_visit_parameterss
    self.calculators = dict()
    self.invariant = True
    self.calculators_sorted = []
  
  def PushCalculator(self, add_calculator):
    assert isinstance(add_calculator, CityVisitCostCalculatorInterface)

    add_hash_key = self._CityVisitDatelessHashKey(add_calculator)
    # If we already has this calculator in our list.
    if add_hash_key in self.calculators:
      # If new one is more expensive than existing,
      # just return False and don't reset invariant.
      if add_calculator.Cost() >= self.calculators[add_hash_key].Cost():
        return False
      # Else remove information about old one.
      else:
        del self.calculators[add_hash_key]
    # Add information about new one.
    self.calculators[add_hash_key] = add_calculator
    self.invariant = False
    return True

  def Shrink(self):
    # Sort by cost and take first max_count.
    self.calculators_sorted = (
        sorted(self.calculators.values(),
               key=lambda calculator: calculator.Cost())
        [:self.max_count])
    # Recompute hashes and indices.
    self.calculators = {
        self._CityVisitDatelessHashKey(calculator) : calculator
        for calculator in self.calculators_sorted}
    # Set invariant. 
    self.invariant = True

  def GetCalculators(self):
    assert self.invariant, (
        'CityVisit list cannot be returned. Please call Shrink first.')
    return self.calculators_sorted

  def Size(self):
    return len(self.calculators)

  def Clear(self):
    self.calculators = dict()
    self.invariant = True
    self.calculators_sorted = []
    
  def _CityVisitDatelessHashKey(self, calculator):
    hash_keys = []
    for day_visit_parameters, day_visit in (
        zip(self.day_visit_parameterss, calculator.day_visits)):
      m_day = hashlib.md5()
      m_day.update(day_visit_parameters.DatelessHashKey())
      m_day.update(day_visit.DatelessHashKey())
      hash_keys.append(m_day.hexdigest())

    m = hashlib.md5()
    # Order of days doesn't matter.
    for hash_key in sorted(hash_keys):
      m.update(hash_key.encode('utf-8'))
    return m.hexdigest()
