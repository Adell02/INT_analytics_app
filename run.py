from app import create_app
from flask import session

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the Flask app - Development Environment
    app.run(host="127.0.0.1", port=5500, debug=True)

