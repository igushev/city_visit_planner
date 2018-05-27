import unittest

from YuPoint import city_visit as city_visit_
from YuRouter import city_visit_heap as city_visit_heap_
from YuRouter import city_visit_points_left


class MockDayVisitParameters(city_visit_.DayVisitParametersInterface):
  
  def __init__(self, hash_key):
    assert isinstance(hash_key, str)
    self.hash_key = hash_key

  def DatelessHashKey(self):
    return self.hash_key


class MockDayVisit(city_visit_.DayVisitInterface):
  
  def __init__(self, hash_key):
    assert isinstance(hash_key, str)
    self.hash_key = hash_key

  def DatelessHashKey(self):
    return self.hash_key


def MockCityVisitPointsLeft(day_visit_hash_keys, cost):
  assert isinstance(day_visit_hash_keys, list)
  assert isinstance(cost, float)

  city_visit = city_visit_.CityVisit(
      [MockDayVisit(day_visit_hash_key)
       for day_visit_hash_key in day_visit_hash_keys],
      city_visit_.CityVisitSummary(cost, 0.))
  return city_visit_points_left.CityVisitPointsLeft(city_visit, [])
  

class CityVisitHeapTest(unittest.TestCase):

  def testGeneral(self):
    city_visit_heap = city_visit_heap_.CityVisitHeap(3, [MockDayVisitParameters('par')])
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisitPointsLeftList())

    visit_a = MockCityVisitPointsLeft(['a'], 10.)
    city_visit_heap.PushCityVisit(visit_a)
    self.assertEqual(1, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_b = MockCityVisitPointsLeft(['b'], 5.)
    city_visit_heap.PushCityVisit(visit_b)
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_c = MockCityVisitPointsLeft(['c'], 7.)
    city_visit_heap.PushCityVisit(visit_c)
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_b, visit_c, visit_a],
                     city_visit_heap.GetCityVisitPointsLeftList())

    visit_d = MockCityVisitPointsLeft(['d'], 3.)
    city_visit_heap.PushCityVisit(visit_d)
    self.assertEqual(4, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    visit_e = MockCityVisitPointsLeft(['e'], 15.)
    city_visit_heap.PushCityVisit(visit_e)
    self.assertEqual(5, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_d, visit_b, visit_c],
                     city_visit_heap.GetCityVisitPointsLeftList())

    city_visit_heap.Clear()
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisitPointsLeftList())

  def testAddingSameOrderlessHashKeyShrink(self):
    city_visit_heap = city_visit_heap_.CityVisitHeap(3, [MockDayVisitParameters('par')])
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisitPointsLeftList())

    visit_a = MockCityVisitPointsLeft(['adf'], 10.)
    city_visit_heap.PushCityVisit(visit_a)
    self.assertEqual(1, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_b = MockCityVisitPointsLeft(['bc'], 5.)
    city_visit_heap.PushCityVisit(visit_b)
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_c = MockCityVisitPointsLeft(['bc'], 7.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_c)  # cost higher.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    city_visit_heap.Shrink()
    self.assertEqual(2, city_visit_heap.Size())
    self.assertEqual([visit_b, visit_a],
                     city_visit_heap.GetCityVisitPointsLeftList())

    visit_d = MockCityVisitPointsLeft(['adf'], 3.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_d)  # const lower.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    city_visit_heap.Shrink()
    self.assertEqual(2, city_visit_heap.Size())
    self.assertEqual([visit_d, visit_b],
                     city_visit_heap.GetCityVisitPointsLeftList())

    visit_e = MockCityVisitPointsLeft(['eg'], 15.)
    city_visit_heap.PushCityVisit(visit_e)
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_d, visit_b, visit_e],
                     city_visit_heap.GetCityVisitPointsLeftList())

    visit_f = MockCityVisitPointsLeft(['adf'], 1.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_f)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_g = MockCityVisitPointsLeft(['eg'], 12.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_g)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)    

    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_f, visit_b, visit_g],
                     city_visit_heap.GetCityVisitPointsLeftList())    

    city_visit_heap.Clear()
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisitPointsLeftList())

  def testAddingSameOrderlessHashKeyNoShrink(self):
    city_visit_heap = city_visit_heap_.CityVisitHeap(3, [MockDayVisitParameters('par')])
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisitPointsLeftList())

    visit_a = MockCityVisitPointsLeft(['adf'], 10.)
    city_visit_heap.PushCityVisit(visit_a)
    self.assertEqual(1, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_b = MockCityVisitPointsLeft(['bc'], 5.)
    city_visit_heap.PushCityVisit(visit_b)
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_c = MockCityVisitPointsLeft(['bc'], 7.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_c)  # cost higher.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    visit_d = MockCityVisitPointsLeft(['adf'], 3.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_d)  # const lower.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    visit_e = MockCityVisitPointsLeft(['eg'], 15.)
    city_visit_heap.PushCityVisit(visit_e)
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)
    
    visit_f = MockCityVisitPointsLeft(['adf'], 1.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_f)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)

    visit_g = MockCityVisitPointsLeft(['eg'], 12.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_g)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError,
                      city_visit_heap.GetCityVisitPointsLeftList)    

    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_f, visit_b, visit_g],
                     city_visit_heap.GetCityVisitPointsLeftList())

    city_visit_heap.Clear()
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisitPointsLeftList())


  def testCityVisitOrderlessHashKey(self):
    city_visit_heap_a = city_visit_heap_.CityVisitHeap(3, [
        MockDayVisitParameters('parX'), MockDayVisitParameters('parY')])
    city_visit_heap_b = city_visit_heap_.CityVisitHeap(3, [
        MockDayVisitParameters('parY'), MockDayVisitParameters('parX')])
    visit_a = MockCityVisitPointsLeft(['dayX', 'dayY'], 10.)
    visit_b = MockCityVisitPointsLeft(['dayY', 'dayX'], 10.)
    # Same pairs of day_visit_parameters and day_visit, but different order.
    self.assertEqual(city_visit_heap_a._CityVisitDatelessHashKey(visit_a),
                     city_visit_heap_b._CityVisitDatelessHashKey(visit_b))
    # Same here.
    self.assertEqual(city_visit_heap_a._CityVisitDatelessHashKey(visit_b),
                     city_visit_heap_b._CityVisitDatelessHashKey(visit_a))
    # Parameterss are different for the same day_visits.
    self.assertNotEqual(city_visit_heap_a._CityVisitDatelessHashKey(visit_a),
                        city_visit_heap_b._CityVisitDatelessHashKey(visit_a))
    # Day_visits are different for the same parameterss.
    self.assertNotEqual(city_visit_heap_a._CityVisitDatelessHashKey(visit_a),
                        city_visit_heap_a._CityVisitDatelessHashKey(visit_b))
    


if __name__ == '__main__':
    unittest.main()

