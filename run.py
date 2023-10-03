from app import create_app


if __name__ == "__main__":
    # Create the Flask app
    app = create_app()
    # Run the Flask app
    app.run(host="0.0.0.0",port=5000)
