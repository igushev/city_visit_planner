import unittest

from Yusi.YuUtils import json_utils
from Yusi.YuUtils.hash_utils import HashKey
from Yusi.YuUtils.repr_utils import Repr
from datetime import datetime


@json_utils.JSONDecorator(
    {'_int_field': json_utils.JSONInt(),
     'datetime_field': json_utils.JSONDateTime()})
class WithFields(object):
  
  def __init__(self, int_field, float_field, string_field, datetime_field):
    assert isinstance(int_field, int)
    assert isinstance(float_field, float)
    assert isinstance(string_field, basestring)
    assert isinstance(datetime_field, datetime)
    self._int_field = int_field  # With underscore.
    self.float_field = float_field
    self._string_field = string_field  # With underscore.
    self.datetime_field = datetime_field

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


# We declare _nested_with_fields_2 to be WithFields but allow None.
@json_utils.JSONDecorator(
    {'_nested_with_fields_1': json_utils.JSONObject(WithFields),
     '_nested_with_fields_2': json_utils.JSONObject(WithFields)})
class WithNestedNoneObjectsFields(object):

  def __init__(self, nested_with_fields_1, nested_with_fields_2):
    assert isinstance(nested_with_fields_1, WithFields)
    if nested_with_fields_2 is not None:
      assert isinstance(nested_with_fields_2, WithFields)
    # With underscore.
    self._nested_with_fields_1 = nested_with_fields_1
    # With underscore.
    self._nested_with_fields_2 = nested_with_fields_2

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_utils.JSONDecorator(inherited=True)
class Level1(object):

  def __init__(self, var1):
    assert isinstance(var1, float)
    self.var1 = var1

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_utils.JSONDecorator()
class Level2(Level1):

  def __init__(self, var1, var2):
    super(Level2, self).__init__(var1)
    assert isinstance(var2, float)
    self.var2 = var2

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_utils.JSONDecorator()
class Level3A(Level2):

  def __init__(self, var1, var2, var3):
    super(Level3A, self).__init__(var1, var2)
    assert isinstance(var3, float)
    self.var3 = var3

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_utils.JSONDecorator()
class Level3B(Level2):

  def __init__(self, var1, var2, var3):
    super(Level3B, self).__init__(var1, var2)
    assert isinstance(var3, basestring)
    self.var3 = var3

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


@json_utils.JSONDecorator(
    {'diff_level_list': json_utils.JSONList(json_utils.JSONObject(Level1))})
class WithDifferentLevelList(object):
  
  def __init__(self, diff_level_list):
    assert isinstance(diff_level_list, list)
    self.diff_level_list = diff_level_list

  def HashKey(self):
    return HashKey(self.__dict__)

  def __repr__(self):
    return Repr(self)

  def __eq__(self, other):
    return self.__dict__ == other.__dict__


class JSONUtilsTest(unittest.TestCase):

  def AssertToFrom(self, obj, obj_cls):
    obj_simple = obj.ToSimple()
    obj_from_simple = obj_cls.FromSimple(obj_simple)
    self.assertEqual(obj.HashKey(), obj_from_simple.HashKey())
    self.assertEqual(repr(obj), repr(obj_from_simple))
    self.assertEqual(obj, obj_from_simple)
    
    obj_json = obj.ToJSON()
    obj_from_json = obj_cls.FromJSON(obj_json)
    self.assertEqual(obj.HashKey(), obj_from_json.HashKey())
    self.assertEqual(repr(obj), repr(obj_from_json))
    self.assertEqual(obj, obj_from_json)

  def testGeneral(self):
    datetime_1 = datetime(1986, 5, 22, 13, 0, 0)
    datetime_2 = datetime(1986, 8, 21, 13, 0, 0)
    datetime_3 = datetime(2014, 1, 3, 9, 54, 0)
    obj = WithNestedFields(
        WithFields(3, 5., u'seven', datetime_1),
        WithListAndDict(
            [WithFields(2, 4., u'six', datetime_2),
             WithFields(8, 10., u'twelve', datetime_2)],
            {u'one': WithFields(15, 17., u'nineteen', datetime_3),
             u'two': WithFields(21, 23., u'twenty five', datetime_3)}),
        None, True)
    self.AssertToFrom(obj, WithNestedFields)

  def testInheritance(self):
    level3a = Level3A(1., 3., 5.)
    self.AssertToFrom(level3a, Level3A)
    # Can call using parent class.
    self.AssertToFrom(level3a, Level1)
    level3b = Level3B(2., 4., u'six')
    self.AssertToFrom(level3b, Level3B)
    # Can call using parent class.
    self.AssertToFrom(level3b, Level1)

    # List of mixed instances of derivative classes.    
    level3a_2 = Level3A(7., 9., 11.)
    level3b_2 = Level3B(8., 10., u'twelve')
    obj = WithDifferentLevelList(
        [level3a, level3b, level3a_2, level3b_2])
    self.AssertToFrom(obj, WithDifferentLevelList)

  def testNestedObjectNone(self):
    datetime_1 = datetime(1986, 5, 22, 13, 0, 0)
    datetime_2 = datetime(1986, 8, 21, 13, 0, 0)
    datetime_3 = datetime(2014, 1, 3, 9, 54, 0)
    # Both fields are set.
    obj = WithNestedNoneObjectsFields(
        WithFields(3, 5., u'seven', datetime_1),
        WithFields(2, 4., u'six', datetime_2))
    self.AssertToFrom(obj, WithNestedNoneObjectsFields)

    # Second field is None.
    obj = WithNestedNoneObjectsFields(
        WithFields(15, 17., u'nineteen', datetime_3), None)
    self.AssertToFrom(obj, WithNestedNoneObjectsFields)
    

if __name__ == '__main__':
    unittest.main()
