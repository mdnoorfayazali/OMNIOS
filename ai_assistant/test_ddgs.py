try:
    from duckduckgo_search import DDGS
    print("Import from duckduckgo_search: SUCCESS")
    with DDGS() as ddgs:
        print("Instantiation: SUCCESS")
except Exception as e:
    print(f"Import from duckduckgo_search failed: {e}")

try:
    from ddgs import DDGS
    print("Import from ddgs: SUCCESS")
except Exception as e:
    print(f"Import from ddgs failed: {e}")
