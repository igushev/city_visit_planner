import hashlib
import unittest

from Yusi.YuUtils import json_utils


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
    m.update(str(obj).encode('utf-8'))
    return m.hexdigest()    


def Repr(obj):
  return '\n'.join(['%s: %s' % (key.replace('_', ' ').title(), value)
                    for key, value in sorted(obj.__dict__.iteritems())])


@json_utils.JSONDecorator(
    {'_int_field': json_utils.JSONInt()})
class WithFields(object):
  
  def __init__(self, int_field, float_field, string_field=5):
    assert isinstance(int_field, int)
    assert isinstance(float_field, float)
    assert isinstance(string_field, basestring)
    self._int_field = int_field  # With underscore.
    self.float_field = float_field
    self._string_field = string_field  # With underscore.

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_utils.JSONDecorator(
    {'nested_list': json_utils.JSONList(json_utils.JSONObject(WithFields)),
     'nest_dict': json_utils.JSONDict(json_utils.JSONSimple(),
                                      json_utils.JSONObject(WithFields))})
class WithListAndDict(object):
  
  def __init__(self, nested_list, nest_dict):
    assert isinstance(nested_list, list)
    assert isinstance(nest_dict, dict)
    self.nested_list = nested_list
    self.nest_dict = nest_dict

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_utils.JSONDecorator(
    {'_nested_with_fields': json_utils.JSONObject(WithFields),
     '_nested_with_list_and_dict': json_utils.JSONObject(WithListAndDict)})
class WithNestedFields(object):

  def __init__(self, nested_with_fields, nested_with_list_and_dict,
               none_value, bool_value):
    assert isinstance(nested_with_fields, WithFields)
    assert isinstance(nested_with_list_and_dict, WithListAndDict)
    # With underscore.
    self._nested_with_fields = nested_with_fields
    # With underscore.
    self._nested_with_list_and_dict = nested_with_list_and_dict
    self._none_value = none_value
    self._bool_value = bool_value

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class JSONUtilsTest(unittest.TestCase):
  
  def testGeneral(self):
    obj = WithNestedFields(
        WithFields(3, 5., u'seven'),
        WithListAndDict(
            [WithFields(2, 4., u'six'),
             WithFields(8, 10., u'twelve')],
            {u'one': WithFields(15, 17., u'nineteen'),
             u'two': WithFields(21, 23., u'twenty five')}),
        None, True)
    obj_simple = obj.ToSimple()
    obj_from_simple = WithNestedFields.FromSimple(obj_simple)
    self.assertEqual(obj.HashKey(), obj_from_simple.HashKey())
    self.assertEqual(str(obj), str(obj_from_simple))
    self.assertEqual(obj, obj_from_simple)
    
    obj_json = obj.ToJSON()
    obj_from_json = WithNestedFields.FromJSON(obj_json)
    self.assertEqual(obj.HashKey(), obj_from_json.HashKey())
    self.assertEqual(str(obj), str(obj_from_json))
    self.assertEqual(obj, obj_from_json)


if __name__ == '__main__':
    unittest.main()
