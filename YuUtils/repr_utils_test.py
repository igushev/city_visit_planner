import unittest

from Yusi.YuUtils.repr_utils import Repr


class ReprUtilsTest(unittest.TestCase):
  
  def testGeneral(self):
    class Breakfast(object):
      def __init__(self, ham, egg):
        self._ham = ham
        self._egg = egg

    self.assertEqual(
        '_egg: scramble\n_ham: canadian',
        Repr(Breakfast('canadian', 'scramble')))


if __name__ == '__main__':
    unittest.main()
