from flask import Flask
from flask_cors import CORS
from database import mongo
from routes.auth_routes import auth_bp
from routes.meal_routes import meal_bp
from routes.grocery_routes import grocery_bp
from routes.fitness_routes import fitness_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load MongoDB Config
app.config.from_object("config.Config")

# Initialize MongoDB
mongo.init_app(app)

# Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(meal_bp, url_prefix="/api/meals")
app.register_blueprint(grocery_bp, url_prefix="/api/grocery")
app.register_blueprint(fitness_bp, url_prefix="/api/fitness")

# Add a default homepage route
@app.route("/")
def home():
    return "Meal Planner API is running!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
