import enum
import json
from dataclasses import dataclass

import treelib


class TaskStatusType(enum.Enum):
    NOT_STARTED = "yet to start"
    RUNNING = "running"
    SUCCESS = "successfully closed"
    FAILED = "failed"


@dataclass
class TaskData:
    task_name: str
    scope: list[str]
    isMandatory: bool
    parameters: any
    status: TaskStatusType = TaskStatusType.NOT_STARTED


class TreeUtility:
    def create_tree_from_dict(self, input_dict) -> treelib.Tree:
        task_tree = treelib.Tree(identifier=input_dict["taskChainId"])
        self.create_tree_using_recursion(input_dict, task_tree)
        return task_tree

    def create_tree_using_recursion(self, input_dict, task_tree, parent=None):
        task = input_dict["task"]
        data = TaskData(
            task_name=task["task_name"],
            scope=task["scope"],
            isMandatory=task["isMandatory"],
            parameters=task["parameters"],
        )
        # TODO add random value for report name task under same tree
        task_id = data.task_name + "_" + task_tree.identifier

        if task_tree.root is None:
            task_tree.create_node(task_id, task_id, data=data)
        else:
            task_tree.create_node(task_id, task_id, data=data, parent=parent)

        list_of_child = task.get("children")
        if not list_of_child:
            return

        for child_task in list_of_child:
            self.create_tree_using_recursion(child_task, task_tree, task_id)


if __name__ == "__main__":
    file_path = "../trigger_task.json"
    with open(file_path) as json_file:
        input_json = json.load(json_file)

    tree_util = TreeUtility()
    tree = tree_util.create_tree_from_dict(input_json['taskChain'])
    for child in tree.children("COC_TC001"):
        print(child)
