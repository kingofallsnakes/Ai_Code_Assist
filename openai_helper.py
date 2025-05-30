# openai_helper.py
from openai import OpenAI

client = OpenAI(
    api_key="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"
)

def ask_code_assistant(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
