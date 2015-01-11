import hashlib

from collections import namedtuple


# TODO(igushev): Rename to CityVisitFinderHeap
class CityVisitHeap(object):

  def __init__(self, max_count, day_visit_parameterss):
    self.max_count = max_count
    self.day_visit_parameterss = day_visit_parameterss
    self.city_visits = dict()
    self.invariant = True
    self.city_visits_sorted = []
  
  def PushCityVisit(self, add_city_visit):
    add_hash_key = self._CityVisitOrderlessHashKey(add_city_visit)
    # If we already has this city_visit in our list.
    if add_hash_key in self.city_visits:
      # If new one is more expensive than existing,
      # just return False and don't reset invariant.
      if add_city_visit.cost >= self.city_visits[add_hash_key].cost:
        return False
      # Else remove information about old one.
      else:
        del self.city_visits[add_hash_key]
    # Add information about new one.
    self.city_visits[add_hash_key] = add_city_visit
    self.invariant = False
    return True

  def Shrink(self):
    # Sort by cost and take first max_count.
    self.city_visits_sorted = (
        sorted(self.city_visits.values(),
               key=lambda city_visit: city_visit.cost)
        [:self.max_count])
    # Recompute hashes and indices.
    self.city_visits = {
        self._CityVisitOrderlessHashKey(city_visit) : city_visit
        for city_visit in self.city_visits_sorted}
    # Set invariant. 
    self.invariant = True

  def GetCityVisits(self):
    assert self.invariant, (
        'CityVisit list cannot be returned. Please call Shrink first.')
    return self.city_visits_sorted

  def Size(self):
    return len(self.city_visits)

  def Clear(self):
    self.city_visits = dict()
    self.invariant = True
    self.city_visits_sorted = []
    
  def _CityVisitOrderlessHashKey(self, city_visit):
    hash_keys = []
    for day_visit_parameters, day_visit in (
        zip(self.day_visit_parameterss, city_visit.day_visits)):
      m_day = hashlib.md5()
      m_day.update(day_visit_parameters.HashKey().encode('utf-8'))
      m_day.update(day_visit.HashKey().encode('utf-8'))
      hash_keys.append(m_day.hexdigest())

    m = hashlib.md5()
    # Order of days doesn't matter.
    for hash_key in sorted(hash_keys):
      m.update(hash_key.encode('utf-8'))
    return m.hexdigest()
