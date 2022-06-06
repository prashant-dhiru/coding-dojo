import treelib
import json


class TreeUtility:
    def create_tree_from_dict(self, input_dict) -> treelib.Tree:
        task_tree = treelib.Tree(identifier=input_dict["taskChainId"])
        self.create_tree_using_recursion(input_dict, task_tree)
        return task_tree

    def create_tree_using_recursion(self, input_dict, task_tree, parent=None):
        task = input_dict["task"]
        node_data = {
            "task_name": task["task_name"],
            "scope": task["scope"],
            "isMandatory": task["isMandatory"],
            "parameters": task["parameters"],
            "status": "yet to run"
        }

        if task_tree.root is None:
            task_tree.create_node(task["task_name"], task["task_name"], data=node_data)
        else:
            task_tree.create_node(task["task_name"], task["task_name"], parent=parent, data=node_data)

        list_of_child = task.get("children")
        if not list_of_child:
            return

        for child_task in list_of_child:
            self.create_tree_using_recursion(child_task, task_tree, task["task_name"])


if __name__ == "__main__":
    file_path = "/home/pdhirend/repos/coding-dojo/module-chaining-service/module-chaining-orchestrator/trigger_task.json"
    with open(file_path) as json_file:
        input_json = json.load(json_file)

    tree_util = TreeUtility()
    tree = tree_util.create_tree_from_dict(input_json['taskChain'])
    for child in tree.children("COC"):
        print(child.data)
