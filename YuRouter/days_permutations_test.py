import unittest


import Yusi
from Yusi.YuRouter.days_permutations import DaysPermutations


class MockPoint(object):
  pass


class DaysPermutationsTest(unittest.TestCase):
  
  def testOnePoint(self):
    a = MockPoint()
    actual = DaysPermutations([a], [True, True, True])
    self.assertEqual(3, len(actual))
    self.assertEqual({0: [a]}, dict(actual[0]))
    self.assertEqual({1: [a]}, dict(actual[1]))
    self.assertEqual({2: [a]}, dict(actual[2]))

  def testTwoPoint(self):
    a, b = MockPoint(), MockPoint()
    actual = DaysPermutations([a, b], [True, True, True])
    self.assertEqual(9, len(actual))
    self.assertEqual({0: [a, b]}, dict(actual[0]))
    self.assertEqual({0: [a], 1: [b]}, dict(actual[1]))
    self.assertEqual({0: [a], 2: [b]}, dict(actual[2]))
    self.assertEqual({1: [a], 0: [b]}, dict(actual[3]))
    self.assertEqual({1: [a, b]}, dict(actual[4]))
    self.assertEqual({1: [a], 2: [b]}, dict(actual[5]))
    self.assertEqual({2: [a], 0: [b]}, dict(actual[6]))
    self.assertEqual({2: [a], 1: [b]}, dict(actual[7]))
    self.assertEqual({2: [a, b]}, dict(actual[8]))

  def testThreePoints(self):
    a, b, c = MockPoint(), MockPoint(), MockPoint()
    actual = DaysPermutations([a, b, c], [True, False, True])
    self.assertEqual(8, len(actual))
    self.assertEqual({0: [a, b, c]}, dict(actual[0]))
    self.assertEqual({0: [a, b], 2: [c]}, dict(actual[1]))
    self.assertEqual({0: [a, c], 2: [b]}, dict(actual[2]))
    self.assertEqual({0: [a], 2: [b, c]}, dict(actual[3]))
    self.assertEqual({0: [b, c], 2: [a]}, dict(actual[4]))
    self.assertEqual({0: [b], 2: [a, c]}, dict(actual[5]))
    self.assertEqual({0: [c], 2: [a, b]}, dict(actual[6]))
    self.assertEqual({2: [a, b, c]}, dict(actual[7]))
    

if __name__ == '__main__':
    unittest.main()
