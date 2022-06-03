import time
from datetime import datetime
from queue import Queue
from threading import Thread
from treelib import Tree, Node
from utility.data_structure_utils import TreeUtility
from typing import Set, List


class Module_Chaining_Orchestrator:
    def __init__(self, json_file):
        tree_utility = TreeUtility()
        self.initial_json = json_file['taskChain']
        self.task_tree = tree_utility.create_tree_from_dict(self.initial_json)
        self.running_job_pool: Set[Task_Thread] = set()
        self.completed_job_after_each_timeout = Queue()

    def trigger_chain_task(self, task_tree: Tree):
        root_thread = self._get_thread_from_tree_node(task_tree.root)
        root_thread.start()
        self.running_job_pool.add(root_thread)
        print()

    def update_chain_task_after_every_timeout(self, timeout=10):
        while time.sleep(timeout) or self.jobs_in_running_job_pool():
            self.update_chain_task()

    def update_chain_task(self):
        for task_thread in self.running_job_pool:
            if task_thread.is_alive():
                continue

            self.running_job_pool.remove(task_thread)
            self.completed_job_after_each_timeout.put(task_thread)

        raise NotImplementedError
        # while not self.completed_job_after_each_timeout.empty():

    @staticmethod
    def _get_thread_from_tree_node(self, node: Node):
        data = node.data
        task_name = data['name_of_task']
        scope = data['scope']
        config = data['parameters_list']
        return Task_Thread(task_name, scope, config)

    def jobs_in_running_job_pool(self) -> bool:
        raise NotImplementedError


class Task_Thread(Thread):
    def __init__(self, task_name, scope, config):
        Thread.__init__(self)
        self.task_name = task_name
        self.scope = scope
        self.config = config

    def run(self) -> None:
        self.start_module_on_edennet(self.scope, self.config)

    @staticmethod
    def start_module_on_edennet(name, scope, config):
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"starting {name} module at {current_time} with scope of cells {scope} and config {config}")
        time.sleep(60 * 10)
        print(f"stopping {name} module at {current_time} with scope of cells {scope} and config {config}")


if __name__ == "__main__":
    module_chaining_orchestrator = Module_Chaining_Orchestrator()
