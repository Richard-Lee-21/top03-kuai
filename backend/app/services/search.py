import httpx
import json
import logging

logger = logging.getLogger(__name__)

async def call_serper_api(query: str, api_key: str) -> dict:
    """
    Call Serper.dev API for web search
    """
    if not api_key:
        raise ValueError("SERPER_API_KEY is required")
    
    url = "https://google.serper.dev/search"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key
    }
    
    payload = {
        "q": query,
        "gl": "us",
        "hl": "en",
        "num": 10
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Format results for LLM
            formatted_results = []
            for result in data.get("organic", []):
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
            
            logger.info(f"Serper API returned {len(formatted_results)} results for query: {query}")
            return formatted_results
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error calling Serper API: {e}")
        raise Exception(f"Search API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error calling Serper API: {e}")
        raise Exception(f"Search API error: {str(e)}")

async def call_google_custom_search_api(query: str, api_key: str, search_engine_id: str) -> dict:
    """
    Call Google Custom Search API (alternative to Serper)
    """
    if not api_key or not search_engine_id:
        raise ValueError("GOOGLE_API_KEY and SEARCH_ENGINE_ID are required")
    
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "num": 10
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Format results for LLM
            formatted_results = []
            for result in data.get("items", []):
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
            
            logger.info(f"Google Custom Search returned {len(formatted_results)} results for query: {query}")
            return formatted_results
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error calling Google Custom Search API: {e}")
        raise Exception(f"Search API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error calling Google Custom Search API: {e}")
        raise Exception(f"Search API error: {str(e)}")