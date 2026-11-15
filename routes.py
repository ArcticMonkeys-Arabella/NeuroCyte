\
from flask import jsonify, request, current_app
from api import api
from api.validator import validate_quiz_request
from api.quiz_engine import generate_quiz


@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "name": "NeuroCyte API",
        "version": "1.0.0",
        "status": "online"
    })


@api.route("/generate", methods=["POST"])
def generate_quiz_route():

    data = request.get_json(silent=True)
    print("API RECEIVED DATA:", repr(data))
    validated_data, error = validate_quiz_request(data)

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 400

    try:
        questions = generate_quiz(
            topic=validated_data["topic"],
            grade=validated_data["grade"],
            difficulty=validated_data["difficulty"],
            question_count=validated_data["question_count"]
        )

        return jsonify({
            "success": True,
            "quiz": {
                "topic": validated_data["topic"],
                "grade": validated_data["grade"],
                "difficulty": validated_data["difficulty"],
                "question_count": validated_data["question_count"],
                "questions": questions
            }
        })

    except RuntimeError:
        return jsonify({
            "success": False,
            "error": "Gemini API key is not configured."
        }), 503

    except Exception:
        current_app.logger.exception("Quiz generation failed")

        return jsonify({
            "success": False,
            "error": "Quiz generation failed. Please try again."
        }), 502
