import asyncio
from concurrent.futures import ProcessPoolExecutor

import future
from treelib import Tree
from typing import Dict, List

from module_chaining_queue import Module_Chaining_Queue


class Module_Chaining_Orchestrator:

    def __init__(self):
        self.ready_queue = Module_Chaining_Queue(maxsize=100)
        self.job_tree_collection: Dict[str, Tree] = dict()
        self.running_queue = List[future]
        self.process_pool_executor = ProcessPoolExecutor(max_workers=10)

    def add_job_tree(self, job_tree: Tree):
        self.job_tree_collection.update({job_tree.identifier: job_tree})
        print(f"job tree {job_tree.identifier}")
        job_tree.show()
        self.insert_root_to_read_queue(job_tree)

    def insert_root_to_read_queue(self, job_tree: Tree):
        try:
            self.ready_queue.submit_job_to_queue(job_tree.get_node(job_tree.root))
        except RuntimeError as error:
            raise RuntimeError("Cannot insert the new jobs to the queue")

    # make it async with while loop of 1 min
    def run_task(self):

        while self.ready_queue.is_empty():
            task_node = self.ready_queue.fetch_job_from_queue()
            self.process_pool_executor.submit(self.run_process_from_tree_node, task_node)

    def run_process_from_tree_node(self):
        pass

