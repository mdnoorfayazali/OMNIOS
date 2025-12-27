from ddgs import DDGS
from ai_assistant.utils.logger import setup_logger

logger = setup_logger(__name__)

def search_web(query: str, max_results: int = 3) -> str:
    """
    Searches the web using DuckDuckGo and returns a summary of results.
    """
    try:
        results = []
        # Using DDGS as a context manager is correct for recent versions
        with DDGS() as ddgs:
            # text() method is correct for >= 4.0
            search_gen = ddgs.text(query, max_results=max_results)
            for r in search_gen:
                if r:
                    results.append(f"Title: {r.get('title', 'N/A')}\nURL: {r.get('href', 'N/A')}\nSnippet: {r.get('body', 'N/A')}\n")
        
        if not results:
            logger.warning(f"Web search returned no results for query: {query}")
            return "No results found. (The search engine might be rate-limiting or the query is too specific.)"
            
        return "\n---\n".join(results)
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return f"Error performing web search: {str(e)}"
