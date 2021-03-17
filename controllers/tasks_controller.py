from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import task_repository, user_repository
from models.task import Task

tasks_blueprint = Blueprint("tasks", __name__)

@tasks_blueprint.route('/tasks')
def tasks():
    # Get all the tasks
    tasks = task_repository.select_all()
    # Return an html view of a list of all tasks
    return render_template("tasks/index.html", all_tasks = tasks)

@tasks_blueprint.route('/tasks/new')
def new_task():
    # return some html which displays a form to create a new task
    users = user_repository.select_all()
    return render_template('tasks/new.html', all_users = users)

@tasks_blueprint.route('/tasks', methods=["POST"])
def create_task():
    description = request.form["description"]
    user_id = request.form["user"]
    duration = request.form["duration"]
    completed = request.form["completed"]

    user = user_repository.select(user_id)

    new_task = Task(description, user, duration, completed)
    task_repository.save(new_task)

    return redirect('/tasks')

@tasks_blueprint.route('/tasks/<id>')
def show_task(id):
    # Find the right task in the db by the id
    task = task_repository.select(id)
    # Render an html view with the task details
    return render_template('/tasks/show.html', task = task)


# Edit - Bring up form for editing
@tasks_blueprint.route('/tasks/<id>/edit')
def edit_task(id):
    task = task_repository.select(id)
    users = user_repository.select_all()

    return render_template('/tasks/edit.html', task = task, all_users = users)

# Update - Save changes
@tasks_blueprint.route('/tasks/<id>', methods=['POST'])
def update_task(id):
    new_description = request.form["description"]
    new_user_id = request.form["user_id"]
    new_duration = request.form["duration"]
    new_completed = request.form["completed"]

    new_user = user_repository.select(new_user_id)
    updated_task = Task(new_description, new_user, new_duration, new_completed, id)
    task_repository.update(updated_task)

    return redirect(f'/tasks/{id}')

# Destroy - Delete item
@tasks_blueprint.route('/tasks/<id>/delete', methods=['POST'])
def destroy_task(id):
    task_repository.delete(id)
    return redirect('/tasks')