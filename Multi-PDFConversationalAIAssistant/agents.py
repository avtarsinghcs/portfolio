from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from tools import web_search, scrape_url

import os

load_dotenv()

# GROQ MODEL
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

# =========================
# WRITER PROMPT
# =========================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an elite investigative research analyst.

Write highly analytical reports.

Rules:
- explain WHY events matter
- include evidence
- include examples
- synthesize information
- avoid generic summaries
- avoid repetition
- think critically
- write professionally
"""
    ),
    (
        "human",
        """
Topic:
{topic}

Research:
{research}

Write a detailed report with:

1. Executive Summary
2. Background
3. Key Findings
4. Detailed Analysis
5. Implications
6. Risks and Challenges
7. Conclusion
8. Sources

Requirements:
- minimum 1200 words
- highly analytical
- evidence-driven
- professional quality
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# =========================
# CRITIC PROMPT
# =========================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior academic reviewer.

Critically evaluate:
- depth
- evidence
- originality
- structure
- clarity
- source quality
- analytical rigor

Be extremely strict.
"""
    ),
    (
        "human",
        """
Report:
{report}

Respond in EXACT format:

Score: X/10

Strengths:
- ...
- ...

Weaknesses:
- ...
- ...

Missing Elements:
- ...
- ...

Final Verdict:
...
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()

# =========================
# MAIN EXECUTION
# =========================

if __name__ == "__main__":

    topic = input("Enter research topic: ")

    print("\n" + "=" * 60)
    print("STEP 1 - SEARCHING WEB...")
    print("=" * 60)

    urls = web_search(topic)

    for i, url in enumerate(urls, start=1):
        print(f"{i}. {url}")

    print("\n" + "=" * 60)
    print("STEP 2 - SCRAPING ARTICLES...")
    print("=" * 60)

    scraped_articles = []

    for url in urls:

        print(f"\nScraping: {url}")

        content = scrape_url(url)

        scraped_articles.append(content)

    research = "\n\n".join(scraped_articles)

    print("\n" + "=" * 60)
    print("STEP 3 - WRITING REPORT...")
    print("=" * 60)

    report = writer_chain.invoke({
        "topic": topic,
        "research": research
    })

    print("\n")
    print(report)

    print("\n" + "=" * 60)
    print("STEP 4 - CRITIC REVIEW...")
    print("=" * 60)

    critique = critic_chain.invoke({
        "report": report
    })

    print("\n")
    print(critique)