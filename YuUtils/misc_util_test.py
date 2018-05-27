import sys
import unittest
import threading

from YuUtils import misc_util


class Spam(object):

  spam_count = 0

  def __init__(self):
    Spam.spam_count += 1
  
  def Method(self, a, b):
    return a + b

  def __del__(self):
    Spam.spam_count -= 1


class WeakBoundMethodUtilsTest(unittest.TestCase):
  
  def testGeneral(self):
    # No objects.
    self.assertEqual(0, Spam.spam_count)
    # Create an object.
    spam = Spam()
    self.assertEqual(1, Spam.spam_count)
    self.assertEqual(2, sys.getrefcount(spam))
    # Create a bound method.
    spam_method = spam.Method
    self.assertEqual(1, Spam.spam_count)
    self.assertEqual(3, sys.getrefcount(spam))
    self.assertEqual(5, spam_method(3, b=2))
    # Create a weak bound method.
    spam_method_weak = misc_util.WeakBoundMethod(spam, Spam.Method)
    self.assertEqual(1, Spam.spam_count)
    self.assertEqual(3, sys.getrefcount(spam))
    self.assertEqual(7, spam_method_weak(4, b=3))
    # Delete spam_method.
    del spam_method
    self.assertEqual(1, Spam.spam_count)
    self.assertEqual(2, sys.getrefcount(spam))
    # Do not delete spam_method_weak.
    # Delete object itself.
    del spam
    self.assertEqual(0, Spam.spam_count)


class Ham(object):
  
  def __init__(self, test_case):
    self.test_lock = threading.Lock()
    self.test_case = test_case
  
  @misc_util.Synchronized('test_lock')
  def Method1(self):
    self.test_case.assertTrue(self.test_lock.locked())

  def Method2(self):
    self.test_case.assertFalse(self.test_lock.locked())


class SynchronizedUtilsTest(unittest.TestCase):
  
  def testGeneral(self):
    ham = Ham(self)
    self.assertFalse(ham.test_lock.locked())
    ham.Method1()
    self.assertFalse(ham.test_lock.locked())
    ham.Method2()
    self.assertFalse(ham.test_lock.locked())


if __name__ == '__main__':
    unittest.main()
