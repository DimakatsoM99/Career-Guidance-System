from flask import Flask, jsonify, request
from flask_cors import CORS 
import cohere

app = Flask(__name__)
CORS(app) 

# Initialize Cohere (replace with your API key)
co = cohere.Client("fod9A7gJIY3W1lJ7dHAU07jXg37ukuOy2Rmdf5Qf") 

@app.route('/')
def home():
    return "Welcome to the Career Guidance System!"

@app.route('/api/careers', methods=['POST'])
def suggest_career():
    data = request.json
    interests = data.get('interests', '').lower()
    skills = data.get('skills', '').lower()
    subject = data.get('favorite_subject', '').lower()

    text = f"{interests} {skills} {subject}"

    keyword_to_careers = {
        "AI Engineer or ML Researcher": ["ai", "artificial intelligence", "machine learning", "deep learning", "neural networks"],
        "Data Analyst": ["math", "calculation", "analysis", "statistics"],
        "Doctor or Nurse": ["biology", "medicine", "health", "nursing", "care", "anatomy"],
        "Mechanical Engineer": ["physics", "engineering", "mechanics", "construction"],
        "Pharmacist or Chemist": ["chemistry", "pharmacy", "labs", "drugs", "research"],
        "Software Developer": ["computers", "technology", "software", "programming", "coding"],
        "Business Analyst or Accountant": ["business", "economics", "finance", "accounting"],
        "Teacher or Education Specialist": ["education", "teaching", "learning", "pedagogy"],
        "Graphic Designer or Illustrator": ["art", "design", "creativity", "drawing", "illustration"],
        "Content Writer or Journalist": ["writing", "english", "language", "journalism", "communication"],
        "Lawyer or Legal Advisor": ["law", "justice", "politics", "debate"],
        "Financial Advisor or Banker": ["finance", "investment", "banking", "money", "markets"],
        "Environmental Scientist": ["environment", "nature", "geography", "earth"],
        "Historian or Anthropologist": ["history", "social science", "archaeology"],
        "Psychologist or Counselor": ["psychology", "mental health", "behavior"],
        "Fitness Trainer or Sports Coach": ["sports", "fitness", "coaching"],
        "Musician or Music Producer": ["music", "instruments", "singing", "composition"],
        "Actor or Director": ["drama", "acting", "film", "stage"],
        "Marketing Specialist": ["marketing", "sales", "advertising", "promotion"],
        "Project Manager or Entrepreneur": ["leadership", "organization", "management"]
    }

    scores = {}
    for career, keywords in keyword_to_careers.items():
        score = sum(word in text for word in keywords)
        if score > 0:
            scores[career] = score

    if not scores:
        suggested = ["General Consultant"]
    else:
        suggested = [career for career, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)]

    return jsonify({"suggested_careers": suggested})

@app.route('/api/ai-suggest', methods=['POST'])
def ai_suggest():
    data = request.json
    query = f"{data.get('interests', '')}, {data.get('skills', '')}, {data.get('favorite_subject', '')}"

    careers = [
        "Software Developer", "AI Engineer", "Data Scientist", "Doctor",
        "Teacher", "Lawyer", "Graphic Designer", "Psychologist", "Accountant"
    ]

    response = co.rerank(
        model="rerank-english-v2.0",
        query=query,
        documents=careers,
        top_n=5
    )

    return jsonify({"suggested_careers": [r.document for r in response.results]})

if __name__ == '__main__':
    app.run(debug=True, port=9000)
