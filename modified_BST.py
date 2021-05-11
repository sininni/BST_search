"""
File: linkedbst.py
Author: Ken Lambert
"""


from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
from math import log
from random import choices, shuffle
from time import time
from typing import List


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            tree = ""
            if node != None:
                tree += recurse(node.right, level + 1)
                tree += "| " * level
                tree += str(node.data) + "\n"
                tree += recurse(node.left, level + 1)
            return tree

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        
        node = self._root

        while node is not None:
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

        return None

    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        
        curr_node = self._root
        parent = None

        if self._root is None:
            self._root = BSTNode(item)

        else:
            while curr_node is not None:
                parent = curr_node
                if item < curr_node.data:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right

            if item < parent.data:
                parent.left = BSTNode(item)
            
            else:
                parent.right = BSTNode(item)

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        def liftMaxInLeftSubtreeToTop(top):
            """
            Helper function to adjust placement of an item.
            """
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        if self.isEmpty(): return None

        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        if item_removed == None: return None

        if not current_node.left == None \
            and not current_node.right == None:
            liftMaxInLeftSubtreeToTop(current_node)
        else:

            if current_node.left == None:
                new_child = current_node.right

            else:
                new_child = current_node.left

            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise.
        """
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        size = self._size
        return height < 2 * log(size + 1, 2) - 1

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        data_lst = [item for item in self.inorder()]
        self.clear()

        def middle_item(lst: list):
            """
            Adds middle item of the list to
            the tree.
            """
            if len(lst) == 0:
                return True
            mid_index = len(lst)//2
            left = lst[:mid_index]
            right = lst[mid_index+1:]
            self.add(lst[mid_index])
            middle_item(left)
            middle_item(right)

        middle_item(data_lst)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        data_lst = [item for item in self.inorder()]
        for data in data_lst:
            if data > item:
                return data
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        data_lst = [item for item in self.inorder()][::-1]
        for data in data_lst:
            if data < item:
                return data
        return None

    def range_find(self, num1: int, num2: int):
        """
        Gets two numbers, which establish
        range in which numbers would be found.
        """
        result_lst = [item for item in self.inorder() if num1 <= item <= num2]
        return result_lst

    def demo_bst(self, path: str):
        """
        Demonstration of efficiency binary search
        tree for the search tasks.
        """
        
        def random_words(path: str):
            """
            Return list of 10000 random words.
            """
            lst = list()
            with open(path, 'r', encoding='utf-8') as file:
                for line in file:
                    lst.append(line[:-1])
            return lst, choices(lst, k=10000)

        def search_words(dictionary, word_lst: List[str]):
            """
            Gets the path to file and list of words
            what are needed to be found.
            """
            start_time = time()

            if type(dictionary) is list:
                for item in word_lst:
                    dictionary.index(item)
            else:
                for item in word_lst:
                    dictionary.find(item)
            
            return time() - start_time

        lists_tuple = random_words(path)
        word_lst, searched_words = lists_tuple[0], lists_tuple[1]
        print('list time start')
        lst_time = search_words(word_lst, searched_words)
        print('list time finished')

        sorted_dict_tree = LinkedBST()
        for item in word_lst:
            sorted_dict_tree.add(item)
        print('sorted tree start')
        sorted_tree_time = search_words(sorted_dict_tree, searched_words)
        print('sorted tree finish')

        unsorted_dict_tree = LinkedBST()
        shuffle(word_lst)
        for item in word_lst:
            unsorted_dict_tree.add(item)
        print('unsorted tree start')
        unsorted_tree_time = search_words(unsorted_dict_tree, searched_words)
        print('unsorted tree finish')

        balanced_unsorted_tree = unsorted_dict_tree.rebalance()
        print('balanced tree start')
        balanced_tree_time = search_words(balanced_unsorted_tree, searched_words)
        
        return f"Time spent to find words in list: {lst_time}.\n\
Time spent to find words in the tree, sorted by the alphabet: {sorted_tree_time}.\n\
Time spent to find words in the unsorted tree: {unsorted_tree_time}.\n\
Time spent to find words in the balanced tree: {balanced_tree_time}."
