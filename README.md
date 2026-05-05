#### Project Title: AI-Powered LinkedIn Post Generator

This project is an AI-powered system built using LangChain + Ollama + Python that generates professional LinkedIn posts based on a user-provided topic and language.

The system uses a conditional routing agent to decide whether a topic is related to Technology (Tech) or General (Non-Tech), and then forwards the request to the appropriate writer agent.

#### Tech Stack
* Python
* FastAPI
* LangChain
* Ollama (LLM backend)
* Uvicorn (server)

### Agent Workflow Explanation
1. User Input Agent

The system accepts:

Topic (e.g., "AI in Healthcare")
Language (e.g., English, Bengali)

2. Routing Agent (Classifier)

The routing agent analyzes the topic and classifies it into:

TECH → AI, ML, Blockchain, Software, Data Science, Cybersecurity
GENERAL → Productivity, Career, Motivation, Leadership, Life Skills

#### Routing Logic:

If topic is technology-related → TECH
Else → GENERAL

The classifier returns only one label: TECH or GENERAL

3. Conditional Routing (Handover System)

Based on classification:

✔ If TECH:
Request is forwarded to Tech Writer Agent

✔ If GENERAL:
Request is forwarded to General Writer Agent

4. Tech Writer Agent

This agent generates LinkedIn posts for technical topics.

Features:
Professional tone
Includes tech insights
Explains trends or innovations
Ends with a question or CTA
2–4 short paragraphs

5. General Writer Agent

This agent generates LinkedIn posts for non-technical topics.

Features:
Professional and motivational tone
Focus on career, productivity, or life skills
Engaging storytelling style
Ends with reflection question or CTA
2–4 short paragraphs

6. Final Output

The system returns a structured LinkedIn post:

{
  "topic": "AI in Healthcare",
  "category": "TECH",
  "post": "Generated LinkedIn post text..."
}

### How to Run the Project
1. Install dependencies
pip install -r requirements.txt
2. Run server
uvicorn linkedin_post_generator:app --host 127.0.0.1 --port 8000 --reload
3. Open API docs
http://127.0.0.1:8000/docs

### Conclusion

This project demonstrates a real-world AI agent system using LangChain with conditional routing and specialized writer agents. It simulates how intelligent systems can dynamically delegate tasks based on input context.