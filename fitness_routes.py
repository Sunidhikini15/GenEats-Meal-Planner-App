from flask import Blueprint, request, jsonify

fitness_bp = Blueprint("fitness", __name__)

@fitness_bp.route("/track", methods=["POST"])
def track_fitness():
    data = request.json
    user_id = data["user_id"]
    steps = data["steps"]
    calories_burned = data["calories"]

    return jsonify({"message": "Fitness data saved", "steps": steps, "calories": calories_burned}), 200
