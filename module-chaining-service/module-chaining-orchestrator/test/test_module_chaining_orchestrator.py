import asyncio
import time
import unittest

from treelib import Tree, Node

from module_chaining_orchestrator2 import Module_Chaining_Orchestrator


class MyTestCase(unittest.TestCase):
    def test_module_chaining_queue(self):
        tree = Tree()
        tree.add_node(
            Node('1', '1', data={"task_name": 1, "scope": 1, "isMandatory": 1, "parameters": 1, "status": "pending"}))
        tree.add_node(
            Node('2', '2', data={"task_name": 2, "scope": 2, "isMandatory": 2, "parameters": 2, "status": "pending"}),
            parent='1')
        tree.add_node(
            Node('3', '3', data={"task_name": 3, "scope": 3, "isMandatory": 3, "parameters": 3, "status": "pending"}),
            parent='1')
        tree.add_node(
            Node('4', '4', data={"task_name": 4, "scope": 4, "isMandatory": 4, "parameters": 4, "status": "pending"}),
            parent='3')

        module_chaining_orchestrator = Module_Chaining_Orchestrator()
        module_chaining_orchestrator.add_job_tree(tree)



if __name__ == '__main__':
    unittest.main()
