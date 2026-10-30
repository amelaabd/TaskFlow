
from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary storage for tasks
tasks = []


# Home endpoint
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to TaskFlow API!",
        "status": "success"
    })


# Health check endpoint
@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "TaskFlow API"
    })


# GET - Retrieve all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


# POST - Create a new task
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    new_task = {
        "id": len(tasks) + 1,
        "title": data.get("title"),
        "completed": False
    }

    tasks.append(new_task)

    return jsonify(new_task), 201


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return jsonify({
                "message": "Task deleted successfully"
            }), 200

    return jsonify({
        "message": "Task not found"
    }), 404


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:

            task["title"] = data.get("title", task["title"])
            task["completed"] = data.get(
                "completed",
                task["completed"]
            )

            return jsonify(task), 200

    return jsonify({
        "message": "Task not found"
    }), 404