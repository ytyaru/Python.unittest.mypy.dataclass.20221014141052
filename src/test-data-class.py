#!/usr/bin/env python3
# coding: utf8
import unittest
import dataclasses
from dataclasses import dataclass, field, Field
from decimal import Decimal
from datetime import datetime, date, time
import types
@dataclass
class Record:
    item_ids: list[int]
class TestDataClass(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass
    def test_init_args_0(self):
        item_ids = [1, 2, 3]
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_1(self):
        args = [[1, 2, 3]]
        r = Record(*args)
        self.assertEqual(args[0], r.item_ids)
    def test_init_kwargs_0(self):
        kwargs = {'item_ids': [1, 2, 3]}
        r = Record(**kwargs)
        self.assertEqual(kwargs['item_ids'], r.item_ids)
    def test_init_args_error_generic_type_0(self): # これパスされちゃ困るんだが……
        item_ids = [1, 2, 'A']
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_generic_type_1(self): # これパスされちゃ困るんだが……
        item_ids = ['A', 'B', 'C']
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_type_int(self): # これパスされちゃ困るんだが……
        item_ids = 1
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_type_str(self): # これパスされちゃ困るんだが……
        item_ids = 'A'
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_type_str_direct(self): # これパスされちゃ困るんだが……
        r = Record('A')
        self.assertEqual('A', r.item_ids)
     

if __name__ == '__main__':
    unittest.main()
