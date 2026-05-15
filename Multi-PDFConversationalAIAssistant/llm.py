from groq import Groq

from config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "llama-3.3-70b-versatile"


def generate_answer(
    question: str,
    contexts: list[str]
):

    context_block = "\n\n".join(
        contexts
    )

    prompt = f"""
You are an elite AI hiring analyst and advanced multi-document reasoning system.

The uploaded documents may include:
- resumes
- CVs
- job descriptions
- portfolios
- research papers

You MUST:
- analyze ALL uploaded documents
- identify every candidate separately
- compare candidates accurately
- compare resumes against job descriptions
- identify missing skills
- evaluate technical fit
- explain strengths and weaknesses
- reason across ALL documents together

IMPORTANT:
- NEVER assume only one document exists
- ALWAYS mention all detected resumes/documents
- compare candidates explicitly
- use document names while reasoning
- synthesize information across all PDFs

DOCUMENT CONTEXT:
{context_block}

QUESTION:
{question}

DETAILED ANALYSIS:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are an expert multi-document RAG reasoning engine."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=3000
    )

    return response.choices[0].message.content