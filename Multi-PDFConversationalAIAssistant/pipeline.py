# =========================
# RESEARCH PIPELINE
# =========================
from tools import web_search, scrape_url
from agents import writer_chain, critic_chain
def run_research_pipeline(topic: str):

    # ---------------------------------
    # STEP 1 — SEARCH
    # ---------------------------------

    print("\n" + "=" * 60)
    print("STEP 1 - SEARCHING WEB...")
    print("=" * 60)

    urls = web_search(topic)

    if not urls:
        print("No URLs found.")
        return

    print("\nFound URLs:\n")

    for i, url in enumerate(urls, start=1):
        print(f"{i}. {url}")

    # ---------------------------------
    # STEP 2 — SCRAPE ARTICLES
    # ---------------------------------

    print("\n" + "=" * 60)
    print("STEP 2 - SCRAPING ARTICLES...")
    print("=" * 60)

    scraped_articles = []

    for url in urls:

        print(f"\nScraping: {url}")

        content = scrape_url(url)

        scraped_articles.append(content)

    # Combine all scraped research
    research = "\n\n".join(scraped_articles)

    # ---------------------------------
    # STEP 3 — WRITE REPORT
    # ---------------------------------

    print("\n" + "=" * 60)
    print("STEP 3 - WRITING REPORT...")
    print("=" * 60)

    report = writer_chain.invoke({
        "topic": topic,
        "research": research
    })

    print("\n")
    print(report)

    # ---------------------------------
    # STEP 4 — CRITIC REVIEW
    # ---------------------------------

    print("\n" + "=" * 60)
    print("STEP 4 - CRITIC REVIEW...")
    print("=" * 60)

    critique = critic_chain.invoke({
        "report": report
    })

    print("\n")
    print(critique)

    # ---------------------------------
    # RETURN EVERYTHING
    # ---------------------------------

    return {
        "topic": topic,
        "urls": urls,
        "research": research,
        "report": report,
        "critique": critique
    }


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    topic = input("Enter research topic: ")

    result = run_research_pipeline(topic)