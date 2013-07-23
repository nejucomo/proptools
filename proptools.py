__all__ = ['LazyProperty', 'TypedProperty']

import unittest
from weakref import WeakKeyDictionary


class StatefulPropertyBase (property):
    """Stores property values in an internally tracked WeakKeyDictionary, keyed on the instance.

    It is mainly useful as a base class, or when for whatever reason
    you want a property that is not stored in the instance __dict__.

    When accessed from a class, a StatefulPropertyBase returns the
    StatefulPropertyBase instance.
    """
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, _cls):
        if instance is None:
            return self
        else:
            try:
                return self._values[instance]
            except KeyError:
                return self._handleMissingValue(instance)

    def _handleMissingValue(self, instance):
        """Override this to customize missing value behavior."""
        raise AttributeError('%r object has no such attribute.' % (type(instance).__name__,))


class LazyProperty (StatefulPropertyBase):
    def __init__(self, maker):
        StatefulPropertyBase.__init__(self)
        self.maker = maker

    def _handleMissingValue(self, instance):
        value = self.maker(instance)
        self._values[instance] = value
        return value


class TypedProperty (StatefulPropertyBase):
    def __init__(self, type):
        StatefulPropertyBase.__init__(self)
        self.type = type

    def __set__(self, instance, value):
        if isinstance(value, self.type):
            self._values[instance] = value
        else:
            raise TypeError('Property values must be instances of %r; not %r' % (self.type, type(value)))

    def __delete__(self, instance):
        try:
            del self._values[instance]
        except KeyError:
            raise AttributeError('%r object has no such attribute.' % (type(instance).__name__,))


class SetOnceProperty (StatefulPropertyBase):
    def __set__(self, instance, value):
        try:
            value = self._values[instance]
        except KeyError:
            self._values[instance] = value
        else:
            raise AttributeError('SetOnceProperty already set to: %r' % (value,))



# unittests:
class LazyPropertyTests (unittest.TestCase):
    def setUp(self):
        testcase = self # For the closure
        testcase.foocount = 0

        class C (object):
            @LazyProperty
            def foo(self):
                testcase.foocount += 1
                return testcase.foocount

        testcase.C = C
        testcase.i = C()

    def test_caching(self):
        self.assertEqual(1, self.i.foo)
        self.assertEqual(1, self.i.foo)

    def test_readonly(self):
        self.assertRaises(AttributeError, setattr, self.i, 'foo', 42)

    def test_classprop(self):
        self.assertIsInstance(self.C.foo, LazyProperty)


class TypedPropertyTests (unittest.TestCase):
    def setUp(self):
        class C (object):
            i = TypedProperty(int)

        self.C = C
        self.obj = C()

    def test_set_success(self):
        self.obj.i = 42
        self.assertEqual(42, self.obj.i)

    def test_set_wrong_type(self):
        self.assertRaises(TypeError, setattr, self.obj, 'i', 'banana')

    def test_get_unset(self):
        self.assertRaises(AttributeError, getattr, self.obj, 'i')

    def test_set_then_del_then_getattr(self):
        self.obj.i = 42
        del self.obj.i
        self.assertRaises(AttributeError, getattr, self.obj, 'i')

    def test_del_twice(self):
        self.obj.i = 42

        def del_i():
            del self.obj.i

        del_i()

        self.assertRaises(AttributeError, del_i)

    def test_classprop(self):
        self.assertIsInstance(self.C.i, TypedProperty)


class SetOncePropertyTests (unittest.TestCase):
    def setUp(self):
        class C (object):
            p = SetOnceProperty()

        self.C = C
        self.obj = C()

    def test_set_once(self):
        self.assertRaises(AttributeError, getattr, self.obj, 'p')
        self.obj.p = 42
        self.assertEqual(42, self.obj.p)
        self.assertRaises(AttributeError, setattr, self.obj, 'p', "foo")
        self.assertEqual(42, self.obj.p)



if __name__ == '__main__':
    unittest.main()


