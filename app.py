
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request
from api import api

app = Flask(__name__)

# Register API
app.register_blueprint(api)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/studio")
def studio():
    avatar_files = [
        "01_star_girl.png",
        "02_headphone_boy.png",
        "03_bow_girl.png",
        "04_varsity_boy.png",
        "05_book_girl.png",
        "06_dark_coat_boy.png",
        "07_pink_headphone_girl.png",
        "08_glasses_student.png",
        "09_lavender_dress_girl.png",
        "10_cap_boy.png"
    ]

    return render_template(
        "studio.html",
        avatar_files=avatar_files
    )


@app.route("/generate", methods=["POST"])
def generate():
    topic = request.form.get("topic")
    grade = request.form.get("grade")
    print("RECEIVED GRADE:", repr(grade))
    difficulty = request.form.get("difficulty")
    question_count = request.form.get("question_count")

    return render_template(
        "quiz.html",
        topic=topic,
        grade=grade,
        difficulty=difficulty,
        question_count=question_count
    )

if __name__ == "__main__":
    app.run(debug=True)
