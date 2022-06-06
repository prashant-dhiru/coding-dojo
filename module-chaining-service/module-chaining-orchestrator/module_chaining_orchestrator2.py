import asyncio
import random
import time
from asyncio import Future
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime

import future
from treelib import Tree, Node
from typing import Dict, List

from module_chaining_queue import Module_Chaining_Queue


class Module_Chaining_Orchestrator:

    def __init__(self):
        self.ready_queue = Module_Chaining_Queue(maxsize=100)
        self.job_tree_collection: Dict[str, Tree] = dict()
        self.running_tasks_promise: List[Future] = list()
        self.process_pool_executor = ThreadPoolExecutor(max_workers=10)

    def add_job_tree(self, job_tree: Tree):
        self.job_tree_collection.update({job_tree.identifier: job_tree})
        print(f"\njob tree {job_tree.identifier} added")
        job_tree.show()
        self.insert_root_to_read_queue(job_tree)

    def insert_root_to_read_queue(self, job_tree: Tree):
        try:
            task = {"tree_id": job_tree.identifier, "node": job_tree.get_node(job_tree.root)}
            self.ready_queue.submit_job_to_queue(task)
        except RuntimeError as error:
            raise RuntimeError("Cannot insert the new jobs to the queue")

    # TODO  make it async with while loop of 1 min
    def run_task(self):
        self.run_task_in_ready_queue()
        time.sleep(2)
        for task_promise in self.running_tasks_promise:
            tree_id, node_id = None, None
            if task_promise.done():
                try:
                    tree_id, node_id = task_promise.result()
                    print()
                except Exception as e:
                    tree_id, node_id = e  # TODO write test cases
                finally:
                    tree = self.job_tree_collection[tree_id]
                    node = tree.get_node(node_id)
                    child_nodes = tree.children(node.identifier)
                    for child_node in child_nodes:
                        self.ready_queue.submit_job_to_queue({"tree_id": tree_id, "node": child_node})

    def run_task_in_ready_queue(self):
        while not self.ready_queue.is_empty():
            task = self.ready_queue.fetch_job_from_queue()
            self.running_tasks_promise.append(self.process_pool_executor.submit(self.run_process_from_tree_node, task))

    def run_process_from_tree_node(self, task: Dict[str, Node]):
        task_node = task["node"]
        task_tree_identifier = task["tree_id"]
        runnable_task = RunnableModule(task_node)
        try:
            runnable_task.run_module()
            task_node.data["status"] = "successful"
            return task_tree_identifier, task_node.identifier
        except Exception:
            task_node.data["status"] = "failed"
            raise RuntimeError(task_tree_identifier, task_node.identifier)


class RunnableModule:
    def __init__(self, tree_node: Node):
        self.task_name = tree_node.data.get('task_name')
        self.scope = tree_node.data.get('scope')
        self.isMandatory = tree_node.data.get('isMandatory')
        self.parameters = tree_node.data.get('parameters')

    def run_module(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        print(
            f"starting {self.task_name} module at {current_time} with scope of cells {self.scope} and config {self.parameters}")
        print(
            f"completed {self.task_name} module at {current_time} with scope of cells {self.scope} and config {self.parameters}")
