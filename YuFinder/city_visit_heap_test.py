import unittest

from Yusi.YuFinder.city_visit_heap import CityVisitHeap


class MockObjectWithHashKey(object):
  
  def __init__(self, hash_key):
    assert isinstance(hash_key, str)
    self.hash_key = hash_key

  def HashKey(self):
    return self.hash_key

class MockCityVisit(object):

  def __init__(self, name, day_visit_hash_keys, cost):
    assert isinstance(name, str)
    assert isinstance(day_visit_hash_keys, list)
    assert isinstance(cost, float)
    
    self.name = name
    self.day_visits = [MockObjectWithHashKey(day_visit_hash_key)
                       for day_visit_hash_key in day_visit_hash_keys]
    self.cost = cost
  
  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class CityVisitHeapTest(unittest.TestCase):

  def testGeneral(self):
    city_visit_heap = CityVisitHeap(3, [MockObjectWithHashKey('par')])
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisits())

    visit_a = MockCityVisit('a', ['a'], 10.)
    city_visit_heap.PushCityVisit(visit_a)
    self.assertEqual(1, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_b = MockCityVisit('b', ['b'], 5.)
    city_visit_heap.PushCityVisit(visit_b)
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_c = MockCityVisit('c', ['c'], 7.)
    city_visit_heap.PushCityVisit(visit_c)
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_b, visit_c, visit_a], city_visit_heap.GetCityVisits())

    visit_d = MockCityVisit('d', ['d'], 3.)
    city_visit_heap.PushCityVisit(visit_d)
    self.assertEqual(4, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    visit_e = MockCityVisit('e', ['e'], 15.)
    city_visit_heap.PushCityVisit(visit_e)
    self.assertEqual(5, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_d, visit_b, visit_c], city_visit_heap.GetCityVisits())

    city_visit_heap.Clear()
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisits())

  def testAddingSameOrderlessHashKeyShrink(self):
    city_visit_heap = CityVisitHeap(3, [MockObjectWithHashKey('par')])
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisits())

    visit_a = MockCityVisit('a', ['adf'], 10.)
    city_visit_heap.PushCityVisit(visit_a)
    self.assertEqual(1, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_b = MockCityVisit('b', ['bc'], 5.)
    city_visit_heap.PushCityVisit(visit_b)
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_c = MockCityVisit('c', ['bc'], 7.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_c)  # cost higher.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    city_visit_heap.Shrink()
    self.assertEqual(2, city_visit_heap.Size())
    self.assertEqual([visit_b, visit_a], city_visit_heap.GetCityVisits())

    visit_d = MockCityVisit('d', ['adf'], 3.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_d)  # const lower.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    city_visit_heap.Shrink()
    self.assertEqual(2, city_visit_heap.Size())
    self.assertEqual([visit_d, visit_b], city_visit_heap.GetCityVisits())

    visit_e = MockCityVisit('e', ['eg'], 15.)
    city_visit_heap.PushCityVisit(visit_e)
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_d, visit_b, visit_e], city_visit_heap.GetCityVisits())

    visit_f = MockCityVisit('f', ['adf'], 1.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_f)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_g = MockCityVisit('g', ['eg'], 12.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_g)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)    

    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_f, visit_b, visit_g], city_visit_heap.GetCityVisits())    

    city_visit_heap.Clear()
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisits())

  def testAddingSameOrderlessHashKeyNoShrink(self):
    city_visit_heap = CityVisitHeap(3, [MockObjectWithHashKey('par')])
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisits())

    visit_a = MockCityVisit('a', ['adf'], 10.)
    city_visit_heap.PushCityVisit(visit_a)
    self.assertEqual(1, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_b = MockCityVisit('b', ['bc'], 5.)
    city_visit_heap.PushCityVisit(visit_b)
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_c = MockCityVisit('c', ['bc'], 7.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_c)  # cost higher.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    visit_d = MockCityVisit('d', ['adf'], 3.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_d)  # const lower.
    self.assertEqual(2, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    visit_e = MockCityVisit('e', ['eg'], 15.)
    city_visit_heap.PushCityVisit(visit_e)
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)
    
    visit_f = MockCityVisit('f', ['adf'], 1.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_f)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)

    visit_g = MockCityVisit('g', ['eg'], 12.)  # Same day_visit_hash_keys.
    city_visit_heap.PushCityVisit(visit_g)  # const lower.
    self.assertEqual(3, city_visit_heap.Size())
    self.assertRaises(AssertionError, city_visit_heap.GetCityVisits)    

    city_visit_heap.Shrink()
    self.assertEqual(3, city_visit_heap.Size())
    self.assertEqual([visit_f, visit_b, visit_g], city_visit_heap.GetCityVisits())

    city_visit_heap.Clear()
    self.assertEqual(0, city_visit_heap.Size())
    self.assertEqual([], city_visit_heap.GetCityVisits())


  def testCityVisitOrderlessHashKey(self):
    city_visit_heap_a = CityVisitHeap(3, [
        MockObjectWithHashKey('parX'), MockObjectWithHashKey('parY')])
    city_visit_heap_b = CityVisitHeap(3, [
        MockObjectWithHashKey('parY'), MockObjectWithHashKey('parX')])
    visit_a = MockCityVisit('a', ['dayX', 'dayY'], 10.)
    visit_b = MockCityVisit('a', ['dayY', 'dayX'], 10.)
    # Same pairs of day_visit_parameters and day_visit, but different order.
    self.assertEqual(city_visit_heap_a._CityVisitOrderlessHashKey(visit_a),
                     city_visit_heap_b._CityVisitOrderlessHashKey(visit_b))
    # Same here.
    self.assertEqual(city_visit_heap_a._CityVisitOrderlessHashKey(visit_b),
                     city_visit_heap_b._CityVisitOrderlessHashKey(visit_a))
    # Parameterss are different for the same day_visits.
    self.assertNotEqual(city_visit_heap_a._CityVisitOrderlessHashKey(visit_a),
                        city_visit_heap_b._CityVisitOrderlessHashKey(visit_a))
    # Day_visits are different for the same parameterss.
    self.assertNotEqual(city_visit_heap_a._CityVisitOrderlessHashKey(visit_a),
                        city_visit_heap_a._CityVisitOrderlessHashKey(visit_b))
    


if __name__ == '__main__':
    unittest.main()

