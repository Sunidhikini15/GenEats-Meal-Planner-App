from flask import Blueprint, request, jsonify
import requests

grocery_bp = Blueprint("grocery", __name__)

@grocery_bp.route("/generate-list", methods=["POST"])
def generate_grocery_list():
    data = request.json
    meal_plan = data["meal_plan"]

    # Mock API call to generate grocery list
    ingredients = meal_plan.split(", ")  # Mock logic
    grocery_list = {item: 1 for item in ingredients}  # Default quantity 1

    return jsonify({"grocery_list": grocery_list}), 200
