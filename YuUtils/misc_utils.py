import weakref


def WeakBoundMethod(obj, unbound_method):
  """Creates a bound method using weak reference to an object."""
  obj_weak = weakref.ref(obj)
  def bound_method_weak(*args, **kwargs):
    return unbound_method(obj_weak(), *args, **kwargs)
  return bound_method_weak


def Synchronized(lock_name='lock'):
  """Synchronizes method my lock with given name."""

  def wrap_method(method):
    def wrapper_method(self, *args, **kwargs):
      lock = getattr(self, lock_name)
      lock.acquire()
      try:
        return method(self, *args, **kwargs)
      finally:
        lock.release()
    return wrapper_method
  return wrap_method
