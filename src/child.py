#!/usr/bin/env python3
# coding: utf8
from parent import Parent
class Child(Parent): pass
if __name__ == '__main__':
    c = Child()
    c.parent_only(1)
    c.parent_only('A')
