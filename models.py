from database import mongo

class User:
    @staticmethod
    def create_user(username, email, password):
        user = {"username": username, "email": email, "password": password}
        return mongo.db.users.insert_one(user)

    @staticmethod
    def find_user(email):
        return mongo.db.users.find_one({"email": email})

class MealPlan:
    @staticmethod
    def save_meal_plan(user_id, meal_plan):
        meal_plan_data = {"user_id": user_id, "meal_plan": meal_plan}
        return mongo.db.meal_plans.insert_one(meal_plan_data)

    @staticmethod
    def get_meal_plans(user_id):
        return mongo.db.meal_plans.find({"user_id": user_id})
