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



if __name__ == '__main__':
    unittest.main()


