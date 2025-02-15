from flask import Blueprint, request, jsonify
import ollama
from models import MealPlan

meal_bp = Blueprint("meal", __name__)

@meal_bp.route("/generate", methods=["POST"])
def generate_meal_plan():
    data = request.json
    user_id = data["user_id"]
    health_goals = data["health_goals"]

    # Call Ollama AI to generate meal plan
    prompt = f"Create a meal plan for a person with {health_goals}."
    try:
        response = ollama.chat("gpt-4", prompt)
        meal_plan = response['message']
        MealPlan.save_meal_plan(user_id, meal_plan)
        return jsonify({"meal_plan": meal_plan}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@meal_bp.route("/get", methods=["GET"])
def get_meals():
    user_id = request.args.get("user_id")
    meals = list(MealPlan.get_meal_plans(user_id))
    return jsonify(meals), 200
