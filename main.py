from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import json

client = OpenAI()

app = FastAPI()

class Problem(BaseModel):
    problem_id: str
    problem: str

@app.post("/")
def solve(req: Problem):

    prompt = f"""
You are a careful math solver.

Solve the following arithmetic word problem.

Ignore irrelevant numbers.

Return STRICT JSON only:

{{
 "reasoning":"at least 80 characters",
 "answer": integer
}}

Problem:
{req.problem}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}],
        response_format={"type":"json_object"}
    )

    data=json.loads(response.choices[0].message.content)

    data["answer"]=int(data["answer"])

    return {
        "reasoning":data["reasoning"],
        "answer":data["answer"]
    }
