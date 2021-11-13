from flask import Flask
from flask_restful import Resource, Api, reqparse,abort,fields,marshal_with
from flask_mongoengine import MongoEngine
app = Flask(__name__)
api = Api(app)


app.config['MONGODB_SETTINGS'] = {
    'db': 'todomodel',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine(app)


class TodoModel(db.Document):
    num = db.IntField()
    task = db.StringField()
    summary = db.StringField()


resource_fields = {
    'num' : fields.Integer,
    'task': fields.String,
    'summary': fields.String

}

# db.create_all()

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, required=True, help="Task is required")
task_post_args.add_argument("summary", type=str, required=True, help="Summary is required")

task_update_args = reqparse.RequestParser()
task_update_args.add_argument("task",type=str)
task_update_args.add_argument("summary",type=str)


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self,todo_id):
        task = TodoModel.objects.get(num=todo_id)
        if not task:
            abort(404, message="Is not there!!")
        return task

    @marshal_with(resource_fields)
    def post(self,todo_id):
        args = task_post_args.parse_args()
        TodoModel(num=todo_id,task=args['task'],summary=args['summary']).save()
        return todo_id, 201

    @marshal_with(resource_fields)
    def put(self,todo_id):
        args = task_update_args.parse_args()
        task = TodoModel.objects.get(num=todo_id)
        if not task:
            abort(404,message="task doesn't exist ,cannot update.")

        if args['task']:
            task.update(task=args['task'])
        if args['summary']:
            task.update(summary=args['summary'])
        return task

    def delete(self,todo_id):
        TodoModel.objects.get(num=todo_id).delete()
        return 'todo deleted', 204


class Todos(Resource):
    def get(self):
        task = TodoModel.query.all()
        todos = {}
        for t in task:
            todos[t.id] = {"task":t.task,"summary":t.summary}
        return todos




api.add_resource(Todo,'/todo/<int:todo_id>')
api.add_resource(Todos,'/todo')
if __name__ == "__main__":
    app.run(debug=True)
