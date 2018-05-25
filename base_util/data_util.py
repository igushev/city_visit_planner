import hashlib


def Repr(obj):
  return '\n'.join(['%s: %s' % (key, value)
                    for key, value in sorted(obj.__dict__.items())])


def HashKey(obj):
  if hasattr(obj, 'HashKey'):
    return obj.HashKey()
  elif hasattr(obj, '__dict__'):
    return HashKey(obj.__dict__)
  elif isinstance(obj, (list, tuple)):
    m = hashlib.md5()
    for item in obj:
      m.update(HashKey(item).encode('utf-8'))
    return m.hexdigest()
  elif isinstance(obj, set):
    m = hashlib.md5()
    for item in sorted(obj):
      m.update(HashKey(item).encode('utf-8'))
    return m.hexdigest()
  elif isinstance(obj, dict):
    m = hashlib.md5()
    for key, value in sorted(obj.items()):
      m.update(HashKey(key).encode('utf-8'))
      m.update(HashKey(value).encode('utf-8'))
    return m.hexdigest()
  else:
    m = hashlib.md5()
    m.update(repr(obj).encode('utf-8'))
    return m.hexdigest()


class AbstractObject(object):

  def __str__(self):
    return Repr(self)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    if other is None:
      return False
    return self.__dict__ == other.__dict__

  def __hash__(self):
    return int(HashKey(self.__dict__), 16)

  def HashKey(self):
    return HashKey(self.__dict__)
