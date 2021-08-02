from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import sqlite3
import sys
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    complete = db.Column(db.Boolean)


@ app.route('/')
def index():
    # Show all todo items
    todo_list = Todo.query.all()

    return render_template('index.html', todo_list=todo_list)


@ app.route('/add', methods=['POST'])
def add():
    # add a new todo item
    new_todo = Todo(title=request.form.get('title'),
                    description=request.form.get('description'), complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@ app.route('/update/<int:todo_id>')
def update(todo_id):
    # update item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))


@ app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # update item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    search = request.form.get('search')
    data = Todo.query.filter_by(title=search).all()
    if len(data) == 0:
        return render_template('index.html', todo_list=Todo.query.all())
    return render_template('index.html', todo_list=data)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
