#!/usr/bin/env python3

# Nils-Olov Olsson, Samuel Grafström

import sys
import bst
import logging

log = logging.getLogger(__name__)

class AVL(bst.BST):
    def __init__(self, value=None):
        self.set_value(value)
        if not self.is_empty():
            self.cons(AVL(), AVL())

    def add(self, v):
        if self.is_empty():
            self.__init__(value=v)
            return self

        if v < self.value():
            self.cons(self.lc().add(v), self.rc())
        elif v > self.value():
            self.cons(self.lc(), self.rc().add(v))
        return self.balance()

    def delete(self, v):
        t = bst.BST.delete(self, v)
        if t is None or t.is_empty():
            return t
        return t.balance()

    def _bf(self):
        # balance factor
        if self.is_empty():
            return 0
        hl = self.lc().height() if self.lc() is not None else 0
        hr = self.rc().height() if self.rc() is not None else 0
        return hl - hr

    def balance(self):
        if self.is_empty():
            return self

        bf = self._bf()

        # left heavy
        if bf > 1:
            child_bf = self.lc()._bf() if self.lc() is not None else 0
            if child_bf >= 0:
                return self.srr()
            else:
                return self.drr()

        # right heavy
        if bf < -1:
            child_bf = self.rc()._bf() if self.rc() is not None else 0
            if child_bf <= 0:
                return self.slr()
            else:
                return self.dlr()

        return self

    def slr(self):
        n2 = self
        if n2.is_empty() or n2.rc() is None or n2.rc().is_empty():
            return n2

        n1 = n2.rc()
        n1_left = n1.lc()

        new_n2 = self.__class__(n2.value()).cons(n2.lc(), n1_left)

        new_n1 = self.__class__(n1.value()).cons(new_n2, n1.rc())

        return new_n1

    def srr(self):
        n2 = self
        if n2.is_empty() or n2.lc() is None or n2.lc().is_empty():
            return n2

        n1 = n2.lc()
        n1_right = n1.rc()

        new_n2 = self.__class__(n2.value()).cons(n1_right, n2.rc())

        new_n1 = self.__class__(n1.value()).cons(n1.lc(), new_n2)

        return new_n1

    def dlr(self):
        n2 = self
        if n2.is_empty() or n2.rc() is None or n2.rc().is_empty():
            return n2

        new_right = n2.rc().srr()
        n2_fixed = self.__class__(n2.value()).cons(n2.lc(), new_right)

        return n2_fixed.slr()

    def drr(self):
        n2 = self
        if n2.is_empty() or n2.lc() is None or n2.lc().is_empty():
            return n2

        new_left = n2.lc().slr()
        n2_fixed = self.__class__(n2.value()).cons(new_left, n2.rc())

        return n2_fixed.srr()

if __name__ == "__main__":
    log.critical("module contains no main module")
    sys.exit(1)
