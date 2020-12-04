from flask import Flask, jsonify, request

app = Flask(__name__)

from tasks import tasks

# List Tasks
@app.route('/tasks')
def getTasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>')
def getTask(task_id):
    tasksFound = [
        task for task in tasks if task['id'] == task_id]
    if (len(tasksFound) > 0):
        return jsonify({'task': tasksFound[0]})
    return jsonify({'message': 'Task Not found'})

# Create New Task
@app.route('/tasks', methods=['POST'])
def addTask():
    new_task = {
        'name': request.json['name'],
        'description': request.json['description']
    }
    tasks.append(new_task)
    return jsonify({'tasks': tasks})

# Update Task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def editTask(task_id):
    tasksFound = [task for task in tasks if task['id'] == task_id]
    if (len(tasksFound) > 0):
        tasksFound[0]['name'] = request.json['name']
        tasksFound[0]['description'] = request.json['description']
        return jsonify({
            'message': 'Task Updated!',
            'task': tasksFound[0]
        })
    return jsonify({'message': 'Task Not found'})

# Delete Task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def deleteTask(task_id):
    tasksFound = [task for task in tasks if task['id'] == task_id]
    if len(tasksFound) > 0:
        tasks.remove(tasksFound[0])
        return jsonify({
            'message': 'Task Deleted!',
            'tasks': tasks
        })
    return jsonify({'message': 'Task Not found'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)