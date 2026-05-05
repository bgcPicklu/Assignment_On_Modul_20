import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load env
load_dotenv()

app = FastAPI()

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# ---------------- Router ----------------
router_prompt = PromptTemplate.from_template(
    """
Classify topic as:
- tech
- general

Topic: {topic}

Return only one word.
"""
)

router_chain = router_prompt | llm | StrOutputParser()

# ---------------- Tech Writer ----------------
tech_prompt = PromptTemplate.from_template(
    """
Write a LinkedIn post in {language} about: {topic}

- 2 to 4 paragraphs
- Professional tone
- End with question or CTA
"""
)

tech_chain = tech_prompt | llm | StrOutputParser()

# ---------------- General Writer ----------------
general_prompt = PromptTemplate.from_template(
    """
Write a LinkedIn post in {language} about: {topic}

- 2 to 4 paragraphs
- Professional tone
- End with question or CTA
"""
)

general_chain = general_prompt | llm | StrOutputParser()


# ---------------- Request Model ----------------
class PostRequest(BaseModel):
    topic: str
    language: str


# ---------------- API Route ----------------
@app.post("/generate-post")
def generate_post(req: PostRequest):

    category = router_chain.invoke({"topic": req.topic}).lower()

    if "tech" in category:
        result = tech_chain.invoke({
            "topic": req.topic,
            "language": req.language
        })
    else:
        result = general_chain.invoke({
            "topic": req.topic,
            "language": req.language
        })

    return {
        "topic": req.topic,
        "category": category,
        "post": result
    }