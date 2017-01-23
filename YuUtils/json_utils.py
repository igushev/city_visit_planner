import copy
import json
import os
from datetime import datetime

    
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
MODULE_FIELD = '__module__'
CLASS_FIELD = '__class__'


class JSONObjectInterface(object):
  
  def ToSimple(self, obj):
    raise NotImplemented()
  
  def FromSimple(self, simple):
    raise NotImplemented()


class JSONSimple(JSONObjectInterface):
  
  def ToSimple(self, obj):
    return obj
  
  def FromSimple(self, simple):
    return simple
  

class JSONInt(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, int)
    return float(obj)
  
  def FromSimple(self, simple):
    assert isinstance(simple, float)
    return int(simple)


class JSONDateTime(JSONObjectInterface):
  
  def ToSimple(self, obj):
    assert isinstance(obj, datetime)
    return obj.strftime(DATETIME_FORMAT)
  
  def FromSimple(self, simple):
    assert isinstance(simple, basestring)
    return datetime.strptime(simple, DATETIME_FORMAT)


class JSONObject(JSONObjectInterface):
  
  def __init__(self, cls):
    self._cls = cls

  def ToSimple(self, obj):
    return obj.ToSimple()
  
  def FromSimple(self, simple):
    return self._cls.FromSimple(simple)

  
class JSONList(object):
  
  def __init__(self, json_obj):
    assert isinstance(json_obj, JSONObjectInterface)
    self._json_obj = json_obj
    
  def ToSimple(self, obj):
    assert isinstance(obj, list)
    return [self._json_obj.ToSimple(item) for item in obj]
  
  def FromSimple(self, simple):
    assert isinstance(simple, list)
    return [self._json_obj.FromSimple(item) for item in simple]


class JSONDict(object):
  
  def __init__(self, key_json_obj, value_json_obj):
    assert isinstance(key_json_obj, JSONObjectInterface)
    assert isinstance(value_json_obj, JSONObjectInterface)
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
  obj_cls = self.__class__
  json_default = JSONSimple()
  simple = dict()
  for key, value in self.__dict__.iteritems():
    json_obj = obj_cls.desc_dict.get(key, json_default)
    simple[key] = json_obj.ToSimple(value) if value is not None else None
  if obj_cls.inherited:
    simple[MODULE_FIELD] = obj_cls.__module__
    simple[CLASS_FIELD] = obj_cls.__name__
  return simple


def ToJSON(self):
  return json.dumps(self.ToSimple())


@classmethod
def FromSimple(cls, simple):
  if cls.inherited:
    obj_cls = getattr(os.sys.modules[simple[MODULE_FIELD]], simple[CLASS_FIELD])
  else:
    obj_cls = cls

  json_default = JSONSimple()
  obj_dict = dict()
  for key, value in simple.iteritems():
    if key in [MODULE_FIELD, CLASS_FIELD]:
      continue
    json_obj =  obj_cls.desc_dict.get(key, json_default)
    obj_dict[str(key)] = (json_obj.FromSimple(value)
                          if value is not None else None)
  obj = obj_cls.__new__(obj_cls)
  obj.__dict__ = obj_dict 
  return obj


@classmethod
def FromJSON(cls, data):
  return cls.FromSimple(json.loads(data))


class JSONDecorator(object):
  
  def __init__(self, desc_dict=None, inherited=False):
    self.desc_dict = desc_dict or {}
    self.inherited = inherited

  def __call__(self, cls):
    desc_dict = copy.copy(self.desc_dict)
    inherited = self.inherited

    curr_cls = cls
    while True:
        bases = curr_cls.__bases__
        assert len(bases) == 1, 'Multiple inheritance is not supported!'
        base = bases[0]
        if getattr(base, 'desc_dict', None) is None:
          break
        desc_dict.update(base.desc_dict)
        inherited = inherited or base.inherited
        curr_cls = base
    
    cls.desc_dict = desc_dict
    cls.inherited = inherited
    cls.ToSimple = ToSimple
    cls.ToJSON = ToJSON
    cls.FromSimple = FromSimple
    cls.FromJSON = FromJSON
    return cls
