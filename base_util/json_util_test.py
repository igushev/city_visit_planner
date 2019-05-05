import unittest
import datetime

import data_util
import json_util


@json_util.JSONDecorator(
    {'_int_field': json_util.JSONInt(),
     'float_field': json_util.JSONFloat(),
     '_string_field': json_util.JSONString(),
     '_bool_value': json_util.JSONBool(),
     'date_field': json_util.JSONDate(),
     'datetime_field': json_util.JSONDateTime()})
class BasicFields(data_util.AbstractObject):
  
  def __init__(self, int_field, float_field, string_field, bool_value, date_field, datetime_field):
    if int_field is not None:
      assert isinstance(int_field, int)
    if float_field is not None:
      assert isinstance(float_field, float)
    if string_field is not None:
      assert isinstance(string_field, str)
    if bool_value is not None:
      assert isinstance(bool_value, bool)
    if date_field is not None:
      assert isinstance(date_field, datetime.date)
    if datetime_field is not None:
      assert isinstance(datetime_field, datetime.datetime)
    self._int_field = int_field  # With underscore.
    self.float_field = float_field
    self._string_field = string_field  # With underscore.
    self._bool_value = bool_value  # With underscore.
    self.date_field = date_field
    self.datetime_field = datetime_field


@json_util.JSONDecorator(
    {'nested_list': json_util.JSONList(json_util.JSONObject(BasicFields)),
     'nested_dict': json_util.JSONDict(json_util.JSONString(),
                                      json_util.JSONObject(BasicFields))})
class NestedListAndDict(data_util.AbstractObject):
  
  def __init__(self, nested_list, nested_dict):
    assert isinstance(nested_list, list)
    assert isinstance(nested_dict, dict)
    self.nested_list = nested_list
    self.nested_dict = nested_dict


@json_util.JSONDecorator(
    {'_basic_fields': json_util.JSONObject(BasicFields),
     '_nested_list_and_dict': json_util.JSONObject(NestedListAndDict)})
class NestedObjects(data_util.AbstractObject):

  def __init__(self, basic_fields, nested_list_and_dict):
    if basic_fields is not None:
      assert isinstance(basic_fields, BasicFields)
    if nested_list_and_dict is not None:
      assert isinstance(nested_list_and_dict, NestedListAndDict)
    # With underscore.
    self._basic_fields = basic_fields
    # With underscore.
    self._nested_list_and_dict = nested_list_and_dict


@json_util.JSONDecorator(
    {'var1': json_util.JSONFloat()},
    inherited=True)
class Inheritance_Base(data_util.AbstractObject):

  def __init__(self, var1):
    assert isinstance(var1, float)
    self.var1 = var1


@json_util.JSONDecorator(
    {'var2': json_util.JSONFloat()})
class Inheritance_Level2(Inheritance_Base):

  def __init__(self, var1, var2):
    super(Inheritance_Level2, self).__init__(var1)
    assert isinstance(var2, float)
    self.var2 = var2


@json_util.JSONDecorator(
    {'var3': json_util.JSONFloat()})
class Inheritance_Level3A(Inheritance_Level2):

  def __init__(self, var1, var2, var3):
    super(Inheritance_Level3A, self).__init__(var1, var2)
    assert isinstance(var3, float)
    self.var3 = var3


@json_util.JSONDecorator(
    {'var3': json_util.JSONString()})
class Inheritance_Level3B(Inheritance_Level2):

  def __init__(self, var1, var2, var3):
    super(Inheritance_Level3B, self).__init__(var1, var2)
    assert isinstance(var3, str)
    self.var3 = var3


@json_util.JSONDecorator(
    {'diff_level_list': json_util.JSONList(json_util.JSONObject(Inheritance_Base))})
class NestedBaseList(data_util.AbstractObject):
  
  def __init__(self, diff_level_list):
    assert isinstance(diff_level_list, list)
    self.diff_level_list = diff_level_list


@json_util.JSONDecorator(
    {'var1': json_util.JSONString(),
     'var2': json_util.JSONString(),
     'var3': json_util.JSONString()})
class ThreeStringFields(data_util.AbstractObject):
  
  def __init__(self, var1, var2):
    self.var1 = var1
    self.var2 = var2


@json_util.JSONDecorator(
    {'var1': json_util.JSONFloat()},
    inherited=True)
class MultipleBase_BaseA(data_util.AbstractObject):

  def __init__(self, var1):
    assert isinstance(var1, float)
    self.var1 = var1


@json_util.JSONDecorator(
    {'var2': json_util.JSONFloat()},
    inherited=True)
class MultipleBase_BaseB(data_util.AbstractObject):

  def __init__(self, var2):
    assert isinstance(var2, float)
    self.var2 = var2


@json_util.JSONDecorator(
    {'var3': json_util.JSONFloat()},
    inherited=True)
class MultipleBase_BaseAB(MultipleBase_BaseA, MultipleBase_BaseB):

  def __init__(self, var1, var2, var3):
    MultipleBase_BaseA.__init__(self, var1)
    MultipleBase_BaseB.__init__(self, var2)
    assert isinstance(var3, float)
    self.var3 = var3


@json_util.JSONDecorator(
    {'var4': json_util.JSONFloat()},
    inherited=True)
class MultipleBase_Derived(MultipleBase_BaseAB):

  def __init__(self, var1, var2, var3, var4):
    MultipleBase_BaseAB.__init__(self, var1, var2, var3)
    assert isinstance(var4, float)
    self.var4 = var4


class ClassWithMethod(data_util.AbstractObject):

  def __init__(self, var1):
    self.var1 = var1

  def Method(self, var2):
    return self.var1 + var2


def SumFunction(var1, var2):
  return var1 + var2


@json_util.JSONDecorator(
    {'func': json_util.JSONFunction()})
class ClassWithFunctionField(data_util.AbstractObject):
  
  def __init__(self, func):
    self.func = func


@json_util.JSONDecorator(
    {'float_field': json_util.JSONFloat()})
class FloatField(data_util.AbstractObject):

  def __init__(self, float_field):
    assert isinstance(float_field, float)
    self.float_field = float_field


@json_util.JSONDecorator(
    {'nested_list': json_util.JSONList(json_util.JSONTuple([json_util.JSONInt(),
                                                            json_util.JSONObject(FloatField)]))})
class NestedListOfTuples(data_util.AbstractObject):
  
  def __init__(self, nested_list):
    self.nested_list = nested_list


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

  def testNestedObjects(self):
    date_1 = datetime.date(1986, 5, 22)
    date_2 = datetime.date(1986, 8, 21)
    date_3 = datetime.date(2014, 1, 3)
    datetime_1 = datetime.datetime(1986, 5, 22, 13, 0, 0)
    datetime_2 = datetime.datetime(1986, 8, 21, 13, 0, 0)
    datetime_3 = datetime.datetime(2014, 1, 3, 9, 54, 0)
    obj = NestedObjects(
        BasicFields(3, 5., u'seven', True, date_1, datetime_1),
        NestedListAndDict(
            [BasicFields(2, 4., u'six', True, date_2, datetime_2),
             BasicFields(8, 10., u'twelve', False, date_2, datetime_2)],
            {u'one': BasicFields(15, 17., u'nineteen', True, date_3, datetime_3),
             u'two': BasicFields(21, 23., u'twenty five', False, date_3, datetime_3)}))
    self.AssertToFrom(obj, NestedObjects)

  def testInheritance(self):
    level3a = Inheritance_Level3A(1., 3., 5.)
    self.AssertToFrom(level3a, Inheritance_Level3A)
    # Can call using parent class.
    self.AssertToFrom(level3a, Inheritance_Base)
    level3b = Inheritance_Level3B(2., 4., u'six')
    self.AssertToFrom(level3b, Inheritance_Level3B)
    # Can call using parent class.
    self.AssertToFrom(level3b, Inheritance_Base)

    # List of mixed instances of derivative classes.    
    level3a_2 = Inheritance_Level3A(7., 9., 11.)
    level3b_2 = Inheritance_Level3B(8., 10., u'twelve')
    obj = NestedBaseList(
        [level3a, level3b, level3a_2, level3b_2])
    self.AssertToFrom(obj, NestedBaseList)

  def testNestedObjectsNone(self):
    date_1 = datetime.date(1986, 5, 22)
    date_2 = datetime.date(1986, 8, 21)
    date_3 = datetime.date(2014, 1, 3)
    datetime_1 = datetime.datetime(1986, 5, 22, 13, 0, 0)
    datetime_2 = datetime.datetime(1986, 8, 21, 13, 0, 0)
    datetime_3 = datetime.datetime(2014, 1, 3, 9, 54, 0)
    basic_fields = BasicFields(3, 5., u'seven', True, date_1, datetime_1)
    nested_list_and_dict = NestedListAndDict(
        [BasicFields(2, 4., u'six', True, date_2, datetime_2),
         BasicFields(8, 10., u'twelve', False, date_2, datetime_2)],
        {u'one': BasicFields(15, 17., u'nineteen', True, date_3, datetime_3),
         u'two': BasicFields(21, 23., u'twenty five', False, date_3, datetime_3)})
    
    # Both fields are set.
    obj = NestedObjects(basic_fields, nested_list_and_dict)
    self.AssertToFrom(obj, NestedObjects)
    
    # First field is None.
    obj = NestedObjects(None, nested_list_and_dict)
    self.AssertToFrom(obj, NestedObjects)

    # Second field is None.
    obj = NestedObjects(basic_fields, None)
    self.AssertToFrom(obj, NestedObjects)

    # Both fields are None.
    obj = NestedObjects(None, None)
    self.AssertToFrom(obj, NestedObjects)

  def testNestedFieldWithNone(self):
    date_1 = datetime.date(1986, 5, 22)
    date_2 = datetime.date(1986, 8, 21)
    date_3 = datetime.date(2014, 1, 3)
    datetime_1 = datetime.datetime(1986, 5, 22, 13, 0, 0)
    datetime_2 = datetime.datetime(1986, 8, 21, 13, 0, 0)
    datetime_3 = datetime.datetime(2014, 1, 3, 9, 54, 0)
    basic_fields_1 = BasicFields(None, 5., None, True, None, datetime_1)
    basic_fields_2 = BasicFields(3, None, u'seven', None, date_1, None)
    nested_list_and_dict = NestedListAndDict(
        [BasicFields(2, 4., u'six', True, date_2, datetime_2),
         None],
        {u'one': None,
         u'two': BasicFields(21, 23., u'twenty five', False, date_3, datetime_3)})

    obj = NestedObjects(basic_fields_1, nested_list_and_dict)
    self.AssertToFrom(obj, NestedObjects)

    obj = NestedObjects(basic_fields_2, None)
    self.AssertToFrom(obj, NestedObjects)

  def testStateFull(self):
    state_not_full = ThreeStringFields(u'one', u'two')
    # No member in state.
    self.assertFalse(hasattr(state_not_full, u'var3'))
    # Convert to simple.
    state_full_simple = state_not_full.ToSimple()
    # Assigned None when converted to simple.
    self.assertIn(u'var3', state_full_simple)
    self.assertIsNone(state_full_simple[u'var3'])
    
    # Delete from simple.
    del state_full_simple[u'var3']
    self.assertNotIn(u'var3', state_full_simple)
    # Recreate object.
    state_full_from_simple = ThreeStringFields.FromSimple(state_full_simple)
    # Assigned None when converted from simple.
    self.assertTrue(hasattr(state_full_from_simple, u'var3'))
    self.assertIsNone(state_full_from_simple.var3)
    
    # Original and recreated objects are not equal.
    self.assertNotEqual(state_not_full.HashKey(),
                        state_full_from_simple.HashKey())
    self.assertNotEqual(repr(state_not_full), repr(state_full_from_simple))
    self.assertNotEqual(state_not_full, state_full_from_simple)

  def testMultipleInheritance(self):
    obj = MultipleBase_Derived(var1=11., var2=12., var3=13., var4=14.)
    self.AssertToFrom(obj, MultipleBase_BaseAB)

  def testClassWithMethod(self):
    class_with_method = ClassWithMethod(3)
    class_with_function_field = ClassWithFunctionField(ClassWithMethod.Method)
    self.AssertToFrom(class_with_function_field, ClassWithFunctionField)
    class_with_function_field_from_simple = (
        ClassWithFunctionField.FromSimple(class_with_function_field.ToSimple()))
    self.assertEqual(4, class_with_function_field_from_simple.func(class_with_method, 1))
    self.assertEqual(7, class_with_function_field_from_simple.func(class_with_method, 4))

  def testClassWithFunctionField(self):
    class_with_function_field = ClassWithFunctionField(SumFunction)
    self.AssertToFrom(class_with_function_field, ClassWithFunctionField)
    class_with_function_field_from_simple = (
        ClassWithFunctionField.FromSimple(class_with_function_field.ToSimple()))
    self.assertEqual(4, class_with_function_field_from_simple.func(3, 1))
    self.assertEqual(7, class_with_function_field_from_simple.func(3, 4))

  def testNestedListOfTuples(self):
    obj = NestedListOfTuples([(1, FloatField(0.1)),
                              (2, FloatField(0.2)),
                              (3, FloatField(0.3))])
    self.AssertToFrom(obj, NestedListOfTuples)

  def testNestedListOfTuplesWithNone(self):
    obj = NestedListOfTuples([(1, None),
                              (None, FloatField(0.2)),
                              (None, None)])
    self.AssertToFrom(obj, NestedListOfTuples)
    

if __name__ == '__main__':
    unittest.main()
