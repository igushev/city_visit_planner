import hashlib


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
    for key, value in sorted(obj.iteritems()):
      m.update(HashKey(key).encode('utf-8'))
      m.update(HashKey(value).encode('utf-8'))
    return m.hexdigest()
  else:
    m = hashlib.md5()
    m.update(repr(obj).encode('utf-8'))
    return m.hexdigest()    
