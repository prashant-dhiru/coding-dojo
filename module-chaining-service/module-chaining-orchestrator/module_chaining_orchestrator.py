import random
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from queue import Queue, Full
from typing import Dict

from treelib import Tree, Node

from utility.data_structure_utils import TaskStatusType, TaskData

IS_RUNNING = True
WAIT_TO_CHECK_READY_QUEUE_SECS = 30


@dataclass
class QueueTask:
    tree_id: str
    node: Node


class ModuleChainingOrchestrator:
    def __init__(self):
        self.ready_queue = Queue(maxsize=100)
        self.job_tree_collection: Dict[str, Tree] = dict()
        self.process_pool_executor = ThreadPoolExecutor(max_workers=10)

    def add_tree_to_orchestrator(self, task_tree: Tree):
        self._update_task_tree_collection(task_tree)
        task = self._create_queue_task_from_node(task_tree, task_tree.get_node(task_tree.root))
        self._insert_task_to_ready_queue(task)

    def _update_task_tree_collection(self, task_tree: Tree):
        self.job_tree_collection.update({task_tree.identifier: task_tree})
        print(f"job tree {task_tree.identifier} added to orchestrator")
        task_tree.show()

    @staticmethod
    def _create_queue_task_from_node(task_tree: Tree, node: Node):
        return QueueTask(
            tree_id=task_tree.identifier,
            node=node
        )

    def _insert_task_to_ready_queue(self, task: QueueTask):
        try:
            self.ready_queue.put_nowait(task)
            print(f"task {task.node.identifier} added to ready queue")
        except Full:
            raise RuntimeError("ready queue full: can not add task right now")

    def trigger_task_in_ready_queue(self):
        if self.ready_queue.empty():
            print(f"no jobs in ready queue, will check again in {WAIT_TO_CHECK_READY_QUEUE_SECS} secs")
            time.sleep(WAIT_TO_CHECK_READY_QUEUE_SECS)
        while not self.ready_queue.empty():
            task: QueueTask = self.ready_queue.get_nowait()
            self.process_pool_executor.submit(self.run_module_with_task, task)
        print("all task completed...")

    def run_module_with_task(self, task: QueueTask):
        print(f"running task {task.node.identifier} from ready queue")
        tree_id = task.tree_id
        task_node = task.node
        task_data: TaskData = task_node.data
        task_data.status = TaskStatusType.SUCCESS
        runnable_task = RunnableModule(task_data)
        child_tasks = self.job_tree_collection.get(tree_id).children(task_node.identifier)
        # try:
        #     runnable_task.run_module()
        #     for child_task in child_tasks:
        #         self._insert_task_to_ready_queue({"tree_id": tree_id, "node": child_task})
        # except Exception as e:
        #     if not task_node.data.get("isMandatory"):
        #         for child_task in child_tasks:
        #             self._insert_task_to_ready_queue({"tree_id": tree_id, "node": child_task})

    # add to ready queue


class RunnableModule:
    def __init__(self, task_data: TaskData):
        self.task_name = task_data.task_name
        self.scope = task_data.scope
        self.isMandatory = task_data.isMandatory
        self.parameters = task_data.parameters

    def run_module(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"starting module {self.task_name} module at {current_time} with scope of cells {self.scope} and config {self.parameters}")
        time.sleep(random.randint(1, 20))
        print(f"completed module {self.task_name} module at {current_time} with scope of cells {self.scope} and config {self.parameters}")
