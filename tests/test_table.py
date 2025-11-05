import unittest
from teeny.runner import run_code
from teeny.value import makeObject, Error, Nil

class TestTable(unittest.TestCase):
    def test_table_create(self):
        self.assertEqual(makeObject(run_code('[1, 2, 3]', False, False, False)), [1, 2, 3])
        self.assertEqual(makeObject(run_code('[a: 1, b: 2]', False, False, False)), {'a': 1, 'b' : 2})
        self.assertEqual(makeObject(run_code('[a: 1, "b": 2, 3]', False, False, False)), {'a': 1, 'b' : 2, '0': 3})
    def test_table_get_and_set(self):
        self.assertEqual(makeObject(run_code('a := [1, 2, 3]; a[0]', False, False, False)), 1)
        self.assertEqual(makeObject(run_code('a := [a: 1, b: 2]; a.b', False, False, False)), 2)
        self.assertEqual(makeObject(run_code('a := [1, 2, 3]; a[0] = 2; a', False, False, False)), [2, 2, 3])
        self.assertEqual(makeObject(run_code('a := [a: 1, b: 2]; a.b = 3; a', False, False, False)), {'a': 1, 'b' : 3})
        self.assertEqual(makeObject(run_code('a := []; [a[0], a[1]] := [2, 3]', False, False, False)), [2, 3])
        self.assertEqual(makeObject(run_code('a := []; [a.b, a.a] := [3, 4]; a', False, False, False)), {'a': 4, 'b' : 3})
        self.assertEqual(makeObject(run_code('a := [1, nil]; [a[0], a[1]] ?= [2, 3]', False, False, False)), [1, 3])
        self.assertEqual(makeObject(run_code('a := [a: nil, b: 1]; [a.b, a.a] ?= [3, 4]; a', False, False, False)), {'a': 4, 'b' : 1})

if __name__ == "__main__":
    unittest.main()