def Repr(obj):
  return '\n'.join(['%s: %s' % (key, value)
                    for key, value in sorted(obj.__dict__.items())])
