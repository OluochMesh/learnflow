import openai
import json
from flask import current_app

def analyze_with_ai(user_text):
    system_prompt = """You are a supportive tutor. Analyze the user's learning summary.
    1. Correct factual inaccuracies.
    2. Identify 2-3 key gaps.
    3. Ask one clarifying question.
    4. Assess understanding as 'SOLID', 'PARTIAL', or 'NEEDS_REVIEW'.
    Return JSON with: corrections, gaps, question, confidenceScore."""
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        response_format={ "type": "json_object" }
    )
    
    return json.loads(response.choices[0].message.content)