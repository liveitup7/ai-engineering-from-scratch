"""Small Flask server for the Docker port-mapping exercise.

Lesson: phases/00-setup-and-tooling/07-docker-for-ai/docs/en.md
Reference: https://flask.palletsprojects.com/en/stable/quickstart/
Run inside the container: python app.py
"""

from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return {"message": "Hello from Docker!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
