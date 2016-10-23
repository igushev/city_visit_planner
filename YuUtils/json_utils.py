import json
    
    
class JSONObjectInterface(object):
  
  def ToSimple(self, obj):
    raise NotImplemented()
  
  def FromSimple(self, simple):
    raise NotImplemented()


class JSONSimple(object):
  
  def ToSimple(self, obj):
    return obj
  
  def FromSimple(self, simple):
    return simple
  

class JSONInt(object):
  
  def ToSimple(self, obj):
    assert isinstance(obj, int)
    return float(obj)
  
  def FromSimple(self, simple):
    assert isinstance(simple, float)
    return int(simple)


class JSONObject(object):
  
  def __init__(self, cls):
    self._cls = cls

  def ToSimple(self, obj):
    return obj.ToSimple()
  
  def FromSimple(self, simple):
    return self._cls.FromSimple(simple)

  
class JSONList(object):
  
  def __init__(self, json_obj):
    self._json_obj = json_obj
    
  def ToSimple(self, obj):
    assert isinstance(obj, list)
    return [self._json_obj.ToSimple(item) for item in obj]
  
  def FromSimple(self, simple):
    assert isinstance(simple, list)
    return [self._json_obj.FromSimple(item) for item in simple]


class JSONDict(object):
  
  def __init__(self, key_json_obj, value_json_obj):
    self._key_json_obj = key_json_obj
    self._value_json_obj = value_json_obj
  
  def ToSimple(self, obj):
    assert isinstance(obj, dict)
    return {self._key_json_obj.ToSimple(key):
            self._value_json_obj.ToSimple(value)
            for key, value in obj.iteritems()}
  
  def FromSimple(self, simple):
    assert isinstance(simple, dict)
    return {self._key_json_obj.FromSimple(key):
            self._value_json_obj.FromSimple(value)
            for key, value in simple.iteritems()}


def ToSimple(self):
  cls = self.__class__
  json_default = JSONSimple()
  simple = dict()
  for key, value in self.__dict__.iteritems():
    json_obj = cls.desc_dict.get(key, json_default)
    simple[key] = json_obj.ToSimple(value)
  return simple


def ToJSON(self):
  return json.dumps(self.ToSimple())


@classmethod
def FromSimple(cls, simple):
  json_default = JSONSimple()
  obj_dict = dict()
  for key, value in simple.iteritems():
    json_obj =  cls.desc_dict.get(key, json_default)
    obj_dict[key] = json_obj.FromSimple(value)
  obj = cls.__new__(cls)
  obj.__dict__ = obj_dict 
  return obj


@classmethod
def FromJSON(cls, data):
  return cls.FromSimple(json.loads(data))


class JSONDecorator(object):
  
  def __init__(self, desc_dict=None):
    self.desc_dict = desc_dict or {}

  def __call__(self, cls):
    cls.desc_dict = self.desc_dict
    cls.ToSimple = ToSimple
    cls.ToJSON = ToJSON
    cls.FromSimple = FromSimple
    cls.FromJSON = FromJSON
    return cls
