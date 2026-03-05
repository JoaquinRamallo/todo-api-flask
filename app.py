from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "To-Do API running ✅",
        "endpoints": [
            "GET /tasks",
            "POST /tasks",
            "PATCH /tasks/<id>",
            "DELETE /tasks/<id>"
        ]
    }), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()

    if not title:
        return jsonify({"error": "title is required"}), 400

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": False
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({"error": "Task not found"}), 404
    tasks = new_tasks
    return jsonify({"deleted": True, "id": task_id}), 200


if __name__ == "__main__":
    app.run(debug=True)