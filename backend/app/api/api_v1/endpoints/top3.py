from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json
import logging

from app.core.database import get_db
from app.core.cache import get_redis_client
from app.core.config import settings
from app.schemas.top3 import KeywordRequest, Top3Response
from app.services.search import call_serper_api
from app.services.llm import call_llm_api, extract_tool_use_from_llm_response
from app.utils.config_loader import load_app_config

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Top3Response)
async def get_top3_recommendations(
    request: KeywordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get Top 3 product recommendations based on keyword
    """
    try:
        # 1. Check cache first
        cache_key = f"query:{request.keyword}"
        cache_client = get_redis_client()
        cached_result = await cache_client.get(cache_key)
        
        if cached_result:
            logger.info(f"Cache hit for keyword: {request.keyword}")
            return Top3Response(
                status="success",
                data=json.loads(cached_result)
            )
        
        # 2. Load configuration from database
        logger.info(f"Loading configuration for keyword: {request.keyword}")
        config = await load_app_config(db, cache_client)
        
        # 3. Search phase
        logger.info(f"Searching for keyword: {request.keyword}")
        search_query = f"best {request.keyword} reviews 2024"
        search_results = await call_serper_api(
            query=search_query,
            api_key=config.get("SERPER_API_KEY")
        )
        
        # 4. Prepare prompt
        logger.info(f"Preparing LLM prompt for keyword: {request.keyword}")
        system_prompt = config.get("LLM_SYSTEM_PROMPT")
        tool_definition = json.loads(config.get("LLM_TOOL_DEFINITION"))
        
        user_prompt_template = config.get("LLM_USER_PROMPT_TEMPLATE")
        user_prompt = user_prompt_template.replace(
            "[USER_KEYWORD]", request.keyword
        ).replace(
            "[SEARCH_RESULTS]", json.dumps(search_results, indent=2)
        )
        
        # 5. LLM analysis phase
        logger.info(f"Calling LLM for keyword: {request.keyword}")
        llm_response_json = await call_llm_api(
            provider=config.get("LLM_PROVIDER"),
            api_key=config.get("LLM_API_KEY"),
            model=config.get("LLM_MODEL_NAME"),
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            tools=[tool_definition],
            tool_choice={ "type": "tool", "name": "report_top3_products" }
        )
        
        # 6. Extract results
        logger.info(f"Extracting results for keyword: {request.keyword}")
        final_data = extract_tool_use_from_llm_response(llm_response_json)
        
        # 7. Cache results (6 hours TTL)
        await cache_client.set(
            cache_key, 
            json.dumps(final_data), 
            ex=21600  # 6 hours
        )
        
        logger.info(f"Successfully processed keyword: {request.keyword}")
        return Top3Response(
            status="success",
            data=final_data
        )
        
    except Exception as e:
        logger.error(f"Error processing keyword {request.keyword}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )