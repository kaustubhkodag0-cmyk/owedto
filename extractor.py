import anthropic
import json
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are a commitment extraction engine. Given a meeting transcript,
extract every explicit commitment — a statement where one person 
promises to deliver something to another person by a specific time.

Return ONLY valid JSON, no explanation, no markdown. Format:
{
  "commitments": [
    {
      "owner": "name of person who made the commitment",
      "recipient": "name of person they made it to",
      "deliverable": "what they committed to do, specific",
      "deadline": "ISO 8601 date if mentioned, else null"
    }
  ]
}

If no commitments exist, return {"commitments": []}.
"""

def extract_commitments(transcript: str) -> list:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": transcript}
        ]
    )
    raw = response.content[0].text
    data = json.loads(raw)
    return data.get("commitments", [])