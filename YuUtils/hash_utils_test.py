import unittest

from Yusi.YuUtils.hash_utils import HashKey


class HashUtilsTest(unittest.TestCase):
  
  def testWithDict(self):
    class Breakfast(object):
      def __init__(self, ham):
        self._ham = ham

    # An object with __dict__.        
    self.assertIsNotNone(HashKey(Breakfast('egg')))

  def testList(self):
    # A list.
    self.assertIsNotNone(HashKey(['spam', 1, 3]))

  def testSet(self):
    # A set.
    self.assertIsNotNone(HashKey({'spam', 1, 3}))
    
  def testDict(self):
    # A dict.
    self.assertIsNotNone(HashKey({1: 'spam', 3: 'egg', 5: 'ham'}))

  def testWithRepr(self):
    # A simple object with repr.
    self.assertIsNotNone(HashKey('spam'))
    self.assertIsNotNone(HashKey(1))
    self.assertIsNotNone(HashKey(3.))


if __name__ == '__main__':
    unittest.main()
