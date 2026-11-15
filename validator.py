
def validate_quiz_request(data):

    if not isinstance(data, dict):
        return None, "Request must contain JSON data."

    topic = data.get("topic")

    if not isinstance(topic, str) or not topic.strip():
        return None, "Please provide a topic."

    topic = topic.strip()

    if len(topic) > 120:
        return None, "Topic must be under 120 characters."

    grade = data.get("grade")

    if not isinstance(grade, str):
        return None, "Please select a valid grade."

    grade = grade.strip()

    valid_grades = [f"Grade {i}" for i in range(1, 13)]

    if grade not in valid_grades:
        return None, "Grade must be between Grade 1 and Grade 12."

    difficulty = data.get("difficulty")

    if not isinstance(difficulty, str):
        return None, "Please provide a valid difficulty."

    difficulty = difficulty.strip().capitalize()

    if difficulty not in ["Easy", "Medium", "Hard"]:
        return None, "Difficulty must be Easy, Medium or Hard."

    question_count = data.get("question_count")

    if isinstance(question_count, bool):
        return None, "Question count must be a number."

    try:
        question_count = int(question_count)
    except (ValueError, TypeError):
        return None, "Question count must be a valid number."

    if not 1 <= question_count <= 20:
        return None, "Question count must be between 1 and 20."

    return {
        "topic": topic,
        "grade": grade,
        "difficulty": difficulty,
        "question_count": question_count
    }, None
