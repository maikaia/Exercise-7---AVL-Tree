#!/usr/bin/env python3

# Nils-Olov Olsson, Samuel Grafström

import bt
import sys
import logging

log = logging.getLogger(__name__)

class BST(bt.BT):
    def __init__(self, value=None):
        self.set_value(value)
        if not self.is_empty():
            self.cons(BST(), BST())

    def is_member(self, v):
        if self.is_empty():
            return False
        if v == self.value():
            return True
        if v < self.value():
            return self.lc().is_member(v)
        else:
            return self.rc().is_member(v)

    def size(self):
        if self.is_empty():
            return 0
        return 1 + self.lc().size() + self.rc().size()

    def height(self):
        height = 0
        if self.is_empty(): 
            return 0
        else: 
            left_height = self.lc().height()
            right_height = self.rc().height()
            height = max(left_height, right_height) + 1
        return height

    def preorder(self):
        if self.is_empty():
            return []
        return [self.value()] + self.lc().preorder() + self.rc().preorder()

    def inorder(self):
        if self.is_empty():
            return []
        return self.lc().inorder() + [self.value()] + self.rc().inorder()

    def postorder(self):
        if self.is_empty():
            return []
        return self.lc().postorder() + self.rc().postorder() + [self.value()]

    def bfs_order_star(self):
        if self.is_empty():
            return []

        height = self.height()
        out = []
        # queue items are (node, level)
        queue = [(self, 1)]
        while len(queue) > 0:
            node, lvl = queue.pop(0)
            if node is None or node.is_empty():
                out.append(None)
                if lvl < height:
                    # keep expanding placeholders until we reach the last level
                    queue.append((self.__class__(), lvl + 1))
                    queue.append((self.__class__(), lvl + 1))
            else:
                out.append(node.value())
                if lvl < height:
                    # enqueue children
                    queue.append((node.lc() if node.lc() is not None else self.__class__(), lvl + 1))
                    queue.append((node.rc() if node.rc() is not None else self.__class__(), lvl + 1))
        return out
    
    def add(self, v):
        if self.is_empty():
            self.__init__(value=v)
            return self
        if v < self.value():
            return self.cons(self.lc().add(v), self.rc())
        if v > self.value():
            return self.cons(self.lc(), self.rc().add(v))
        return self
    
    def _min_value(self):
        node = self
        while node is not None and not node.is_empty() and node.lc() is not None and not node.lc().is_empty():
            node = node.lc()
        return node.value()

    def _max_value(self):
        node = self
        while node is not None and not node.is_empty() and node.rc() is not None and not node.rc().is_empty():
            node = node.rc()
        return node.value()

    def delete(self, v):
        if self.is_empty():
            return self

        if v < self.value():
            return self.cons(self.lc().delete(v), self.rc())
        if v > self.value():
            return self.cons(self.lc(), self.rc().delete(v))

        # v == self.value(): delete this node
        left_empty = self.lc().is_empty()
        right_empty = self.rc().is_empty()

        # no children
        if left_empty and right_empty:
            return self.__class__()

        # one child
        if left_empty and not right_empty:
            return self.rc()
        if right_empty and not left_empty:
            return self.lc()

        # two children: pick replacement to avoid making it more unbalanced
        left_height = self.lc().height()
        right_height = self.rc().height()

        if left_height >= right_height:
            # use predecessor (max of left subtree)
            rep = self.lc()._max_value()
            new_lc = self.lc().delete(rep)
            return self.set_value(rep).cons(new_lc, self.rc())
        else:
            # use successor (min of right subtree)
            rep = self.rc()._min_value()
            new_rc = self.rc().delete(rep)
            return self.set_value(rep).cons(self.lc(), new_rc)
        
if __name__ == "__main__":
    log.critical("module contains no main module")
    sys.exit(1)
