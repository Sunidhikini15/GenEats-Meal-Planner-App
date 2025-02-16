from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML Template for GenEats website and InfoBot
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GenEats</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    @keyframes fadeInLeft {
      from { opacity: 0; transform: translateX(-20px); }
      to { opacity: 1; transform: translateX(0); }
    }
    .fade-in-left { animation: fadeInLeft 1.5s ease-in-out forwards; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .fade-in { animation: fadeIn 2s ease-in-out forwards; }
    .home-bg { background-image: url('/static/images/background.png'); background-size: cover; background-position: center; }
    .menu-bg { background-image: url('/static/images/background.png'); background-size: cover; background-position: center; }
    .about-bg { background-image: url('/static/images/background.png'); background-size: cover; background-position: center; }
  </style>
</head>
<body class="bg-gray-50">
  <!-- Header -->
  <header class="bg-white shadow-sm sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <a href="/" class="flex items-center space-x-2">
          <span class="text-2xl font-bold text-gray-900">GenEats</span>
        </a>
        <nav class="flex space-x-8">
          <a href="#home" class="text-gray-700 hover:text-blue-600 transition-colors">HOME</a>
          <a href="#menu" class="text-gray-700 hover:text-blue-600 transition-colors">MENU</a>
          <a href="#about" class="text-gray-700 hover:text-blue-600 transition-colors">ABOUT</a>
        </nav>
      </div>
    </div>
  </header>

  <!-- Home Section -->
  <section id="home" class="home-bg py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-center justify-between gap-8">
        <div class="flex-1">
          <h1 class="text-4xl font-bold mb-4 text-gray-900 fade-in-left">Generative AI for Smarter Eating</h1>
          <p class="text-lg mb-6 text-gray-600 fade-in-left" style="animation-delay: 0.5s;">
            Empowering healthier lifestyles with AI-driven personalized nutrition. Let our smart system craft the perfect meal plan for you.
          </p>
        </div>
        <div class="flex-1">
          <img 
            src="/static/images/profile.png"
            alt="Healthy meal"
            class="rounded-lg shadow-lg w-85 h-auto fade-in"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Menu Section -->
  <section id="menu" class="menu-bg py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="relative">
            <img src="https://images.unsplash.com/photo-1512058564366-18510be2db19?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60" alt="Smart Protein Bowl" class="w-full h-48 object-cover">
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold mb-2">Smart Protein Bowl</h3>
            <p class="text-gray-600 text-sm mb-4">AI-optimized protein mix with lean meats</p>
            <div class="flex justify-between items-center">
              <div class="space-y-1">
                <div class="text-sm text-gray-600">550 calories</div>
                <div class="text-sm text-gray-600">20 min</div>
              </div>
              <button class="p-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors">
                <img src="https://lucide.dev/icons/plus" alt="Plus Icon" class="h-5 w-5">
              </button>
            </div>
          </div>
        </div>
        <!-- Other Meal Cards... -->
      </div>
    </div>
  </section>

  <!-- About Section -->
  <section id="about" class="about-bg py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">About GenEats</h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Revolutionizing nutrition through artificial intelligence, making healthy eating personalized and effortless.
        </p>
      </div>
      <!-- Features and Mission Statement... -->
    </div>
  </section>

  <!-- InfoBot Section -->
  <section id="infobot" class="py-12 bg-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">InfoBot</h2>
      <form method="POST">
        <input type="text" name="user_input" placeholder="Enter your info here..." required class="p-2 border rounded-md">
        <button type="submit" class="p-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">Submit</button>
      </form>
      {% if response %}
      <h3 class="mt-4 text-lg font-semibold">InfoBot says:</h3>
      <p class="text-gray-600">{{ response }}</p>
      {% endif %}
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <p class="text-gray-600">© 2025 GenEats. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        # Process user input (e.g., store in a database or file)
        response = f"Thank you for sharing: {user_input}"
    return render_template_string(HTML_TEMPLATE, response=response)

if __name__ == "__main__":
    app.run(debug=True)
