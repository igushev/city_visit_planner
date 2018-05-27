import hashlib

from Yusi.YuPoint import city_visit
from Yusi.YuRouter import city_visit_points_left


class CityVisitHeap(object):
  """Keeps track of the best CityVisits.""" 

  def __init__(self, max_count, day_visit_parameterss):
    assert isinstance(max_count, int)
    for day_visit_parameters in day_visit_parameterss:
      assert isinstance(day_visit_parameters, city_visit.DayVisitParametersInterface)

    self.max_count = max_count
    self.day_visit_parameterss = day_visit_parameterss
    self.cvpls = dict()
    self.invariant = True
    self.cvpls_sorted = []
  
  def PushCityVisit(self, add_city_visit_points_left):
    assert isinstance(add_city_visit_points_left, city_visit_points_left.CityVisitPointsLeft)

    add_hash_key = self._CityVisitDatelessHashKey(add_city_visit_points_left)
    # If we already has this city_visit_points_left in our list.
    if add_hash_key in self.cvpls:
      # If new one is more expensive than existing,
      # just return False and don't reset invariant.
      if (add_city_visit_points_left.city_visit.city_visit_summary.cost >=
          self.cvpls[add_hash_key].city_visit.city_visit_summary.cost):
        return False
      # Else remove information about old one.
      else:
        del self.cvpls[add_hash_key]
    # Add information about new one.
    self.cvpls[add_hash_key] = add_city_visit_points_left
    self.invariant = False
    return True

  def Shrink(self):
    # Sort by cost and take first max_count.
    self.cvpls_sorted = (
        sorted(self.cvpls.values(),
               key=lambda cvpl: cvpl.city_visit.city_visit_summary.cost)
        [:self.max_count])
    # Recompute hashes and indices.
    self.cvpls = {
        self._CityVisitDatelessHashKey(cvpl) : cvpl
        for cvpl in self.cvpls_sorted}
    # Set invariant. 
    self.invariant = True

  def GetCityVisitPointsLeftList(self):
    assert self.invariant, (
        'CityVisit list cannot be returned. Please call Shrink first.')
    return self.cvpls_sorted

  def Size(self):
    return len(self.cvpls)

  def Clear(self):
    self.cvpls = dict()
    self.invariant = True
    self.cvpls_sorted = []
    
  def _CityVisitDatelessHashKey(self, cvpl):
    hash_keys = []
    for day_visit_parameters, day_visit in (
        zip(self.day_visit_parameterss, cvpl.city_visit.day_visits)):
      m_day = hashlib.md5()
      m_day.update(day_visit_parameters.DatelessHashKey().encode('utf-8'))
      m_day.update(day_visit.DatelessHashKey().encode('utf-8'))
      hash_keys.append(m_day.hexdigest())

    m = hashlib.md5()
    # Order of days doesn't matter.
    for hash_key in sorted(hash_keys):
      m.update(hash_key.encode('utf-8'))
    return m.hexdigest()
