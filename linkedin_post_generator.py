import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# ---------------------------
# 1. Router (Classifier)
# ---------------------------
router_prompt = PromptTemplate.from_template(
    """
Classify the following topic into one of two categories:
- tech
- general

Topic: {topic}

Only return one word: tech or general.
"""
)

router_chain = router_prompt | llm | StrOutputParser()

# ---------------------------
# 2. Tech Writer Agent
# ---------------------------
tech_prompt = PromptTemplate.from_template(
    """
Write a professional LinkedIn post in {language} about a technology topic.

Topic: {topic}

Requirements:
- 2 to 4 short paragraphs
- Professional and engaging tone
- Include insights or trends
- End with a thoughtful question or call-to-action
"""
)

tech_chain = tech_prompt | llm | StrOutputParser()

# ---------------------------
# 3. General Writer Agent
# ---------------------------
general_prompt = PromptTemplate.from_template(
    """
Write a professional LinkedIn post in {language} about a general topic.

Topic: {topic}

Requirements:
- 2 to 4 short paragraphs
- Professional and engaging tone
- Relatable and thoughtful
- End with a question or call-to-action
"""
)

general_chain = general_prompt | llm | StrOutputParser()

# ---------------------------
# 4. Conditional Routing
# ---------------------------
def route(info):
    topic = info["topic"]
    category = router_chain.invoke({"topic": topic}).strip().lower()

    if "tech" in category:
        return tech_chain
    else:
        return general_chain


final_chain = RunnableBranch(
    (lambda x: "tech" in router_chain.invoke({"topic": x["topic"]}).lower(), tech_chain),
    general_chain
)

# ---------------------------
# 5. Main Function
# ---------------------------
def generate_post(topic, language):
    result = final_chain.invoke({
        "topic": topic,
        "language": language
    })
    return result


# ---------------------------
# 6. Run Examples
# ---------------------------
if __name__ == "__main__":
    print("\n--- Tech Example (English) ---\n")
    print(generate_post("AI in Healthcare", "English"))

    print("\n--- General Example (Bengali) ---\n")
    print(generate_post("Remote Work Productivity", "Bengali"))