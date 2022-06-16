import json
import unittest

from module_chaining_orchestrator import ModuleChainingOrchestrator, QueueTask
from utility.data_structure_utils import TreeUtility


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        file_path = "../trigger_task.json"
        with open(file_path) as json_file:
            input_json = json.load(json_file)

        tree_util = TreeUtility()
        self.tree1 = tree_util.create_tree_from_dict(input_json['taskChain'])
        self.tree2 = tree_util.create_tree_from_dict(input_json['taskChain2'])

    def test_module_chaining_orchestrator(self):
        module_chaining_orchestrator = ModuleChainingOrchestrator()
        self.assertTrue(isinstance(module_chaining_orchestrator, ModuleChainingOrchestrator))

    def test_add_to_tree_collection(self):
        orchestrator = ModuleChainingOrchestrator()
        orchestrator.add_tree_to_orchestrator(self.tree1)
        self.assertDictEqual(orchestrator.job_tree_collection, {self.tree1.identifier: self.tree1})

    def test_add_to_ready_queue(self):
        orchestrator = ModuleChainingOrchestrator()
        orchestrator.add_tree_to_orchestrator(self.tree1)
        first_node: QueueTask = orchestrator.ready_queue.get_nowait()
        self.assertEqual(first_node.tree_id, self.tree1.identifier)
        self.assertEqual(first_node.node.identifier, self.tree1.root)

    def test_add_to_ready_queue_2_tree(self):
        orchestrator = ModuleChainingOrchestrator()
        orchestrator.add_tree_to_orchestrator(self.tree1)
        orchestrator.add_tree_to_orchestrator(self.tree2)

        first_node: QueueTask = orchestrator.ready_queue.get_nowait()
        self.assertEqual(first_node.tree_id, self.tree1.identifier)
        self.assertEqual(first_node.node.identifier, self.tree1.root)

        second_node: QueueTask = orchestrator.ready_queue.get_nowait()
        self.assertEqual(second_node.tree_id, self.tree2.identifier)
        self.assertEqual(second_node.node.identifier, self.tree2.root)

    def test_trigger_task_in_ready_queue_sleep(self):
        orchestrator = ModuleChainingOrchestrator()
        orchestrator.add_tree_to_orchestrator(self.tree1)
        orchestrator.trigger_task_in_ready_queue()


if __name__ == '__main__':
    unittest.main()
