from flask import Flask, jsonify, abort, request, make_response, url_for
 
app = Flask(__name__, static_url_path = "")

tasks = [
    {
        'id': 1,
        'title': u' ',
        'description': u' ', 
        'done': False
    },
    {
        'id': 2,
        'title': u' ',
        'description': u'', 
        'done': False
    }
]
 
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task
    
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))


 
@app.route('/todo/api/v1.0/tasks', methods = ['POST'])

def create_task():
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify( { 'task': make_public_task(task) } ), 201
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])

def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])

def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    tasks.remove(task[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)
