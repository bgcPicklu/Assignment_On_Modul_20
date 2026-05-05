from fastapi import FastAPI
from pydantic import BaseModel

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

# ---------------- FASTAPI ----------------
app = FastAPI(title="LinkedIn Generator (Ollama)")

# ---------------- LOCAL LLM (NO API KEY) ----------------
llm = ChatOllama(
    model="mistral",   # or llama3, llama2, etc.
    temperature=0.7
)

# ---------------- ROUTER ----------------
router_prompt = PromptTemplate.from_template(
    """
Classify the topic into:
- tech
- general

Topic: {topic}

Return only one word.
"""
)

router_chain = router_prompt | llm | StrOutputParser()

# ---------------- TECH WRITER ----------------
tech_prompt = PromptTemplate.from_template(
    """
Write a professional LinkedIn post in {language}.

Topic: {topic}

Requirements:
- 2 to 4 short paragraphs
- Professional tone
- Include tech insights
- End with question or CTA
"""
)

tech_chain = tech_prompt | llm | StrOutputParser()

# ---------------- GENERAL WRITER ----------------
general_prompt = PromptTemplate.from_template(
    """
Write a professional LinkedIn post in {language}.

Topic: {topic}

Requirements:
- 2 to 4 short paragraphs
- Professional tone
- Relatable content
- End with question or CTA
"""
)

general_chain = general_prompt | llm | StrOutputParser()

# ---------------- REQUEST MODEL ----------------
class PostRequest(BaseModel):
    topic: str
    language: str

# ---------------- API ENDPOINT ----------------
@app.post("/generate-post")
def generate_post(req: PostRequest):

    category = router_chain.invoke({"topic": req.topic}).lower()

    if "tech" in category:
        post = tech_chain.invoke({
            "topic": req.topic,
            "language": req.language
        })
    else:
        post = general_chain.invoke({
            "topic": req.topic,
            "language": req.language
        })

    return {
        "topic": req.topic,
        "category": category,
        "post": post
    }