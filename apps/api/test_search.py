from src.services.search_service import get_search_tool
import asyncio

async def test():
    tool = get_search_tool()
    results = tool.web_search("is Narendra modi died?")
    print(f"RESULTS: {results}")

if __name__ == "__main__":
    import sys
    import os
    # Add project root to sys.path
    sys.path.append(os.getcwd())
    asyncio.run(test())
