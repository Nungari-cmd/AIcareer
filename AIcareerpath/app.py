import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Configure the new GenAI client
genai.api_key = GEMINI_API_KEY

app = Flask(__name__)

# Build the AI prompt for the student
def build_prompt(p):
    tech = ", ".join(p.get("techSkills", [])) or "None"
    soft = ", ".join(p.get("softSkills", [])) or "None"
    return f"""You are a career advisor. Analyse this student and return ONLY valid JSON. Do not include any explanation, markdown, or backticks. Output must be directly parseable by json.loads().

Student: Education={p.get("educationLevel","")}, Field={p.get("fieldOfStudy","")}, Experience={p.get("experience","")}, Location={p.get("location","")}, WorkStyle={p.get("workStyle","")}, Salary={p.get("salaryGoal","")}, Interests={p.get("interests","")}, TechSkills={tech}, SoftSkills={soft}

Return exactly this structure:
{{"paths":[{{"title":"str","icon":"emoji","fitPercent":90,"description":"str","isTop":true}}],"courses":[{{"name":"str","platform":"str","duration":"str"}}],"skillsToLearn":[{{"skill":"str","priority":"must"}}],"roadmap":[{{"phase":"Month 1-2","title":"str","description":"str"}}]}}

Rules: 3 paths (one isTop true, fitPercent 85-97, others 65-84), 5 courses, 6 skills (must and good mix), 4 roadmap phases. Be specific to this student."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyse", methods=["POST"])
def analyse():
    p = request.get_json()
    if not p:
        return jsonify({"error": "No data received"}), 400

    try:
        # Generate AI response using the new GenAI library
        response = genai.text.generate(
            model="gemini-1.5-pro",  # or "gemini-1.5-flash"
            prompt=build_prompt(p),
            temperature=0.7,
            max_output_tokens=2048
        )

        # Extract the text output
        raw = response.result[0].content[0].text.strip()

        # Remove any triple-backticks if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1]
        if raw.endswith("```"):
            raw = raw.rsplit("```", 1)[0]

        # Return AI output as JSON
        return jsonify(json.loads(raw))

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("\n  CareerAI running at http://localhost:5000\n")
    app.run(debug=True, port=5000)