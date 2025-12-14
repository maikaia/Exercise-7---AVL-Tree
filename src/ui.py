#!/usr/bin/env python3

# Nils-Olov Olsson, Samuel Grafström

import bst
import avl
import logging

log = logging.getLogger(__name__)

class TerminalUI:
    def __init__(self, mode):
        if mode == "bst":
            logging.info("running in BST mode")
            self._tree = bst.BST()
        else:
            logging.info("running in AVL mode")
            self._tree = avl.AVL()

    def run(self):
        self.display_menu()
        while True:
            opt, err = self.get_choice()
            if err is not None:
                self.display_error(err)
                continue
            
            if opt == "m":
                self.display_menu()
            elif opt == "t":
                self.display_tree()
            elif opt == "a":
                self.add_value()
            elif opt == "d":
                self.delete_value()
            elif opt == "f":
                self.is_member()
            elif opt == "q":
                break
            else:
                log.error("menu case '{}' is missing, aborting".format(opt))
                return 1

    def display_menu(self):
        print(self.menu_rule("top", self.menu_width()))
        for opt in self.menu_options():
            print("\t{}".format(opt))
        print(self.menu_rule("bot", self.menu_width()))

    def display_error(self, err):
        print("error> {}".format(err))

    def display_tree(self):
        if self._tree.is_empty():
            print("\n  Tree is empty\n")
            return

        self.show_2d()
        print("")
        print("Size:      {}".format(self._tree.size()))
        print("Height:    {}".format(self._tree.height()))
        print("Inorder:   {}".format(self._tree.inorder()))
        print("Preorder:  {}".format(self._tree.preorder()))
        print("Postorder: {}".format(self._tree.postorder()))
        print("BFS star:  {}".format([
            v if v is not None else "*" for v in self._tree.bfs_order_star()
        ]))
        print("")

    def add_value(self):
        value, err = self.get_int("Enter value to be added")
        if err is not None:
            self.display_error(err)
            return
        self._tree = self._tree.add(value)

    def delete_value(self):
        value, err = self.get_int("Enter value to be deleted")
        if err is not None:
            self.display_error(err)
            return
        self._tree = self._tree.delete(value)

    def is_member(self):
        value, err = self.get_int("Enter search value")
        if err is not None:
            self.display_error(err)
            return

        print("\n  {} is a {}member\n".format(
            value,
            "" if self._tree.is_member(value) is True else "non-"),
        )

    def menu_rule(self, pos, width):
        return ("*" if pos == "top" else "~") * width

    def menu_width(self):
        return 32

    def menu_options(self):
        return [
            "m: menu",
            "t: display tree",
            "",
            "a: add value",
            "d: delete value",
            "f: test membership",
            "",
            "q: quit",
        ]

    def menu_hotkeys(self):
        opts = self.menu_options()
        return [ o.split(":")[0] for o in opts if len(o.split(":")[0]) == 1 ]

    def get_choice(self):
        buf = input("menu> ")
        if len(buf) != 1:
            return None, "input must be a a single character"
        if buf[0] not in self.menu_hotkeys():
            return None, "invalid choice"
        print(buf)
        return buf[0], None

    def get_int(self, message):
        buf = input("{}> ".format(message))
        try:
            buf = int(buf)
            print(buf)
            return buf, None
        except ValueError:
            return None, "invalid input (not an integer)"

    def show_2d(self):
        bfs_list = self._tree.bfs_order_star()
        height = self._tree.height()

        if height == 0:
            print("")
            return

        # convert values to strings, replacing None by "*"
        tokens = []
        for i in bfs_list:
            if i is None:
                tokens.append("*")
            else:
                tokens.append(str(i))

        if len(tokens) == 0:
            print("")
            return

        # figure out cell width
        max_len = 0
        for t in tokens:
            if len(t) > max_len:
                max_len = len(t)
        cell = max_len + 2

        i = 0
        level = 0
        while level < height:
            count = 2 ** level

            # spaces before first node on the level
            first = (2 ** (height - level - 1) - 1) * cell
            # spaces between nodes on the level
            between = (2 ** (height - level) - 1) * cell

            line = " " * first

            j = 0
            while j < count:
                if i < len(tokens):
                    item = tokens[i]
                else:
                    item = "*"

                line += item.center(cell)

                if j != count - 1:
                    line += " " * between

                i += 1
                j += 1

            print(line.rstrip())
            level += 1

if __name__ == "__main__":
    logging.critical("ui contains no main module")
    sys.exit(1)
