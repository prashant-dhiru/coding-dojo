import asyncio
import json
import time
import unittest

from treelib import Tree, Node

from module_chaining_orchestrator2 import Module_Chaining_Orchestrator
from utility.data_structure_utils import TreeUtility


class MyTestCase(unittest.TestCase):
    def test_module_chaining_queue(self):
        # tree = Tree()
        # tree.add_node( Node('A', 'A', data={"task_name": "A", "scope": "cell1, cell2", "isMandatory": True, "parameters": 1, "status": "pending"}))
        # tree.add_node(Node('B', 'B', data={"task_name": "B", "scope": "cell1, cell2", "isMandatory": False, "parameters": 2, "status": "pending"}), parent='A')
        # tree.add_node(Node('C', 'C', data={"task_name": "C", "scope": "cell3, cell4", "isMandatory": True, "parameters": 3, "status": "pending"}), parent='A')
        # tree.add_node(Node('D', 'D', data={"task_name": "D", "scope": "cell1, cell2", "isMandatory": True, "parameters": 4, "status": "pending"}), parent='C')

        file_path = "/home/pdhirend/repos/coding-dojo/module-chaining-service/module-chaining-orchestrator/trigger_task.json"
        with open(file_path) as json_file:
            input_json = json.load(json_file)

        tree_util = TreeUtility()
        tree = tree_util.create_tree_from_dict(input_json['taskChain'])

        module_chaining_orchestrator = Module_Chaining_Orchestrator()
        module_chaining_orchestrator.add_job_tree(tree)
        module_chaining_orchestrator.start_module_trigger()


if __name__ == '__main__':
    unittest.main()
