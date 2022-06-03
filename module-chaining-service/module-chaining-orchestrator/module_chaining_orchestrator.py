import json
import random
import time
from datetime import datetime
from queue import Queue
from threading import Thread
from typing import Set, List

from treelib import Tree, Node

from utility.data_structure_utils import TreeUtility


class Module_Chaining_Orchestrator:
    def __init__(self, input_dict):
        tree_utility = TreeUtility()
        self.initial_dict = input_dict['taskChain']
        self.task_tree = tree_utility.create_tree_from_dict(self.initial_dict)
        self.running_job_pool: Set[Task_Thread] = set()
        self.completed_job_list: List[Task_Thread] = list()

    def trigger_chain_task(self):
        root_thread = self._get_thread_from_tree_node(self.task_tree.get_node(self.task_tree.root))
        root_thread.start()
        self.running_job_pool.add(root_thread)
        self.update_chain_task_after_every_timeout(5)
        print()

    def update_chain_task_after_every_timeout(self, timeout=10):
        while time.sleep(timeout) or self.jobs_in_running_job_pool():
            self.update_chain_task()

    def update_chain_task(self):
        self.completed_job_list: List[Task_Thread] = list()

        # find all the task completed
        for task_thread in self.running_job_pool:
            if not task_thread.is_alive():
                self.completed_job_list.append(task_thread)

        # find child, run and add into the pool
        for completed_thread in self.completed_job_list:
            completed_node = self.task_tree.get_node(completed_thread.task_name)
            child_nodes_of_completed_thread = self.task_tree.children(completed_node.data.get('name_of_task'))
            child_threads_of_completed_thread = [self._get_thread_from_tree_node(child_node) for child_node in
                                                 child_nodes_of_completed_thread]
            # run and update the pool
            for child_thread in child_threads_of_completed_thread:
                child_thread.start()

            self.running_job_pool.update(child_threads_of_completed_thread)

        # remove the task from the pool
        for thread in self.completed_job_list:
            self.running_job_pool.remove(thread)

    @staticmethod
    def _get_thread_from_tree_node(node: Node):
        data = node.data
        task_name = data['name_of_task']
        scope = data['scope']
        config = data['parameters_list']
        return Task_Thread(task_name, scope, config)

    def jobs_in_running_job_pool(self) -> bool:
        return bool(self.running_job_pool)


class Task_Thread(Thread):
    def __init__(self, task_name, scope, config):
        Thread.__init__(self)
        self.task_name = task_name
        self.scope = scope
        self.config = config

    def run(self) -> None:
        self.start_module_on_edennet(self.task_name, self.scope, self.config)

    @staticmethod
    def start_module_on_edennet(name, scope, config):
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"starting {name} module at {current_time} with scope of cells {scope} and config {config}")
        time.sleep(random.randint(30, 60))
        print(f"completed {name} module at {current_time} with scope of cells {scope} and config {config}")


if __name__ == "__main__":
    file_path = "/home/pdhirend/repos/coding-dojo/module-chaining-service/module-chaining-orchestrator/trigger_task.json"
    with open(file_path) as json_file:
        input_json = json.load(json_file)

    module_chaining_orchestrator = Module_Chaining_Orchestrator(input_json)
    module_chaining_orchestrator.trigger_chain_task()
    print()
