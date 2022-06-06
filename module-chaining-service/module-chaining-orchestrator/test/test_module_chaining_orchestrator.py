import asyncio
import unittest

from treelib import Tree, Node

from module_chaining_orchestrator2 import Module_Chaining_Orchestrator


class MyTestCase(unittest.TestCase):
    def test_module_chaining_queue(self):
        tree = Tree()
        tree.add_node(Node('1', '1', data="1"))
        tree.add_node(Node('2', '2', data="2"), parent='1')
        tree.add_node(Node('3', '3', data="3"), parent='1')
        tree.add_node(Node('4', '4', data="4"), parent='3')

        module_chaining_orchestrator = Module_Chaining_Orchestrator()
        module_chaining_orchestrator.add_job_tree(tree)
        self.assertEqual(tree.get_node(tree.root), module_chaining_orchestrator.ready_queue.fetch_job_from_queue())


if __name__ == '__main__':
    unittest.main()
