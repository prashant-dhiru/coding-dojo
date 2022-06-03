from flask import Flask, jsonify, request

tasks = {
    "tasks": [
        {
            "task_name": "COC",
            "parameters": {
                "param1": "string"
            }
        },
        {
            "task_name": "PRACH",
            "parameters": {
                "param1": "string"
            }
        }
    ]
}

chain_tasks = {
    "chain_tasks": [
        {
            "taskChainId": "TC001",
            "status": "Success",
            "runTime": "2022-06-02:14:42"
        },
        {
            "taskChainId": "TC002",
            "status": "Failed",
            "runTime": "2022-06-02:14:42"
        }
    ]
}

chain_task_details = [{
    "taskChain": {
        "taskChainId": "TC001",
        "status": "Success",
        "task": {
            "task_name": "COC",
            "status": "Success",
            "children": [
                {
                    "task": {
                        "task_name": "PRACH",
                        "status": "success"
                    }
                },
                {
                    "task": {
                        "task_name": "CCCO",
                        "status": "success",
                        "children": [
                            {
                                "task_name": "ANR",
                                "status": "success"
                            }
                        ]
                    }
                }
            ]
        }
    }
}]

app = Flask(__name__)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/triggerChainTask', methods=['POST'])
def trigger_task():
    task_chain = request.json.get("taskChain")
    print(task_chain)
    return jsonify({"status": "success"})


@app.route('/getChainTasks', methods=['GET'])
def get_chain_tasks():
    return jsonify(chain_tasks)


@app.route('/getChainTaskDetails/<string:task_chain_id>', methods=['GET'])
def get_chain_task_details(task_chain_id):
    for chain_task_detail in chain_task_details:
        if chain_task_detail.get("taskChain").get("taskChainId") == task_chain_id:
            return jsonify(chain_task_detail)
        else:
            return jsonify({"status": "404 - could not find chain task details for taskChainId = " + task_chain_id})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
