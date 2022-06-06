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
        self.process_pool_executor = ThreadPoolExecutor(max_workers=10)

    def add_job_tree(self, job_tree: Tree):
        self.job_tree_collection.update({job_tree.identifier: job_tree})
        print(f"\njob tree {job_tree.identifier} added")
        job_tree.show()
        self.insert_node_to_ready_queue({"tree_id": job_tree.identifier, "node": job_tree.get_node(job_tree.root)})

    def insert_node_to_ready_queue(self, task: Dict[str, Node]):
        try:
            self.ready_queue.submit_job_to_queue(task)
        except RuntimeError as error:
            raise RuntimeError("Cannot insert the new jobs to the queue")

    def start_module_trigger(self, runs=20):
        count = 0
        while count < runs:
            count += 1
            time.sleep(random.randint(0, 4))

            while not self.ready_queue.is_empty():
                self.process_pool_executor.submit(self.run_module_with_task, self.ready_queue.fetch_job_from_queue())

    def run_module_with_task(self, task):
        tree_id = task["tree_id"]
        task_node = task["node"]
        task_node.data["status"] = "passed"
        runnable_task = RunnableModule(task_node)
        child_tasks = self.job_tree_collection.get(tree_id).children(task_node.identifier)
        try:
            runnable_task.run_module()
            for child_task in child_tasks:
                self.insert_node_to_ready_queue({"tree_id": tree_id, "node": child_task})
        except Exception as e:
            if not task_node.data.get("isMandatory"):
                for child_task in child_tasks:
                    self.insert_node_to_ready_queue({"tree_id": tree_id, "node": child_task})

    # add to ready queue


class RunnableModule:
    def __init__(self, tree_node: Node):
        self.task_name = tree_node.data.get('task_name')
        self.scope = tree_node.data.get('scope')
        self.isMandatory = tree_node.data.get('isMandatory')
        self.parameters = tree_node.data.get('parameters')

    def run_module(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        print(
            f"starting module {self.task_name} module at {current_time} with scope of cells {self.scope} and config {self.parameters}")
        time.sleep(random.randint(1, 20))
        print(
            f"completed module {self.task_name} module at {current_time} with scope of cells {self.scope} and config {self.parameters}")
