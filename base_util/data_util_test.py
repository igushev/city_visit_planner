import unittest

import data_util


class ReprTest(unittest.TestCase):
  
  def testGeneral(self):
    class Breakfast(object):
      def __init__(self, ham, egg):
        self._ham = ham
        self._egg = egg

    self.assertEqual(
        '_egg: scramble\n_ham: canadian',
        data_util.Repr(Breakfast('canadian', 'scramble')))


class HashKeyTest(unittest.TestCase):
  
  def testWithDict(self):
    class Breakfast(object):
      def __init__(self, ham):
        self._ham = ham

    # An object with __dict__.        
    self.assertIsNotNone(data_util.HashKey(Breakfast('egg')))

  def testList(self):
    # A list.
    self.assertIsNotNone(data_util.HashKey(['spam', 'egg', 'ham']))

  def testSet(self):
    # A set.
    self.assertIsNotNone(data_util.HashKey({'spam', 'egg', 'ham'}))
    
  def testDict(self):
    # A dict.
    self.assertIsNotNone(data_util.HashKey({1: 'spam', 3: 'egg', 5: 'ham'}))

  def testWithRepr(self):
    # A simple object with repr.
    self.assertIsNotNone(data_util.HashKey('spam'))
    self.assertIsNotNone(data_util.HashKey(1))
    self.assertIsNotNone(data_util.HashKey(3.))


if __name__ == '__main__':
    unittest.main()
