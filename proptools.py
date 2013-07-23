import unittest
from weakref import WeakKeyDictionary


class LazyProperty (property):
    def __init__(self, maker):
        self._values = WeakKeyDictionary()
        self._maker = maker

    def __get__(self, instance, _cls):
        try:
            return self._values[instance]
        except KeyError:
            value = self._maker(instance)
            self._values[instance] = value
            return value


class TypedProperty (property):
    def __init__(self, type):
        self._values = WeakKeyDictionary()
        self.type = type

    def __get__(self, instance, _cls):
        try:
            return self._values[instance]
        except KeyError:
            raise AttributeError('%r object has no such attribute.' % (type(instance).__name__,))

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



if __name__ == '__main__':
    unittest.main()


