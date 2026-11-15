
import os
import json
from google import genai
from google.genai import types


def generate_quiz(topic, grade, difficulty, question_count):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Gemini API key is not configured.")

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=120000,
            retry_options=types.HttpRetryOptions(
                attempts=1
            )
        )
    )

    prompt = f"""
    Create exactly {question_count} educational multiple-choice questions.

    Topic: {topic}
    Student's academic level: {grade}
    Difficulty: {difficulty}

    IMPORTANT:
    - Adapt every question to the selected grade level.
    - Use vocabulary, concepts and explanations appropriate for {grade}.
    - Do not make questions unnecessarily advanced or too elementary.
    - Match the requested difficulty while staying within the student's grade-level curriculum.
    - Test understanding and application, not just memorisation.

    Return a JSON object with this structure:
    {{
        "questions": [
            {{
                "question": "Question text",
                "options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D"
                ],
                "answer": "Exact correct option",
                "explanation": "Short explanation"
            }}
        ]
    }}

    Rules:
    - Exactly four options per question.
    - Only one correct answer.
    - The answer must exactly match one of the options.
    - Questions must be factually accurate.
    - Match the requested difficulty.
    - Keep explanations short and understandable.
    - Do not include markdown or text outside the JSON.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.4
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    result = json.loads(response.text)

    questions = result.get("questions", [])

    if not isinstance(questions, list):
        raise ValueError("Gemini returned an invalid question list.")

    if len(questions) != question_count:
        raise ValueError("AI returned an incorrect number of questions.")

    for question in questions:

        if not isinstance(question, dict):
            raise ValueError("An invalid question was returned.")

        if not isinstance(question.get("options"), list) or len(question["options"]) != 4:
            raise ValueError("A question does not have four options.")

        if question.get("answer") not in question["options"]:
            raise ValueError("A question has an invalid correct answer.")

        if not question.get("question") or not question.get("explanation"):
            raise ValueError("A question is missing required information.")

    return questions
