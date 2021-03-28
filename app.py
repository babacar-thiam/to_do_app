from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DATABASE Configuration
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Routes of the App
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['task']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except ConnectionError:
            return 'There is an issue!'
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<pk>')
def delete(pk):
    task = Todo.query.get_or_404(pk)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except ConnectionError:
        return 'There is a problem while deleting!'


@app.route('/update/<pk>', methods=['POST', 'GET'])
def update(pk):
    task = Todo.query.get_or_404(pk)
    if request.method == 'POST':
        task.content = request.form['task']
        try:
            db.session.commit()
            return redirect('/')
        except ConnectionError:
            return 'There is an issue!'
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()
        return render_template('index.html', update_task=task, tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
