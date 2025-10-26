import httpx
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def call_llm_api(
    provider: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    tools: list = None,
    tool_choice: dict = None
) -> dict:
    """
    Call LLM API (Claude or OpenAI)
    """
    if not api_key:
        raise ValueError(f"{provider.upper()}_API_KEY is required")
    
    if provider.lower() == "anthropic":
        return await call_anthropic_api(api_key, model, system_prompt, user_prompt, tools, tool_choice)
    elif provider.lower() == "openai":
        return await call_openai_api(api_key, model, system_prompt, user_prompt, tools, tool_choice)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

async def call_anthropic_api(
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    tools: list = None,
    tool_choice: dict = None
) -> dict:
    """
    Call Anthropic Claude API
    """
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0.7,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }
    
    if tools:
        payload["tools"] = tools
    if tool_choice:
        payload["tool_choice"] = tool_choice
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Anthropic API call successful for model: {model}")
            return data
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error calling Anthropic API: {e}")
        raise Exception(f"LLM API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error calling Anthropic API: {e}")
        raise Exception(f"LLM API error: {str(e)}")

async def call_openai_api(
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    tools: list = None,
    tool_choice: dict = None
) -> dict:
    """
    Call OpenAI API
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }
    
    if tools:
        payload["tools"] = tools
    if tool_choice:
        payload["tool_choice"] = tool_choice
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"OpenAI API call successful for model: {model}")
            return data
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error calling OpenAI API: {e}")
        raise Exception(f"LLM API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error calling OpenAI API: {e}")
        raise Exception(f"LLM API error: {str(e)}")

def extract_tool_use_from_llm_response(llm_response: dict) -> list:
    """
    Extract tool use results from LLM response
    Handles both Claude and OpenAI response formats
    """
    try:
        content = llm_response.get("content", [])
        
        # Handle Claude format
        if isinstance(content, list):
            for item in content:
                if item.get("type") == "tool_use" and item.get("name") == "report_top3_products":
                    return item.get("input", {}).get("recommendations", [])
        
        # Handle OpenAI format
        tool_calls = llm_response.get("choices", [{}])[0].get("message", {}).get("tool_calls", [])
        for tool_call in tool_calls:
            if tool_call.get("function", {}).get("name") == "report_top3_products":
                return json.loads(tool_call.get("function", {}).get("arguments", "{}")).get("recommendations", [])
        
        # Fallback: try to parse from text content
        text_content = ""
        if isinstance(content, list):
            text_content = " ".join([item.get("text", "") for item in content if item.get("type") == "text"])
        else:
            text_content = str(content)
        
        # Try to find JSON in text content
        import re
        json_match = re.search(r'\{.*"recommendations".*\}', text_content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            return parsed.get("recommendations", [])
        
        raise ValueError("Could not extract recommendations from LLM response")
        
    except Exception as e:
        logger.error(f"Error extracting tool use from LLM response: {e}")
        raise Exception(f"Failed to parse LLM response: {str(e)}")

async def test_llm_connection(provider: str, api_key: str, model: str) -> bool:
    """
    Test LLM API connection
    """
    try:
        if provider.lower() == "anthropic":
            await call_anthropic_api(
                api_key=api_key,
                model=model,
                system_prompt="You are a helpful assistant.",
                user_prompt="Hello, test connection.",
                tools=None,
                tool_choice=None
            )
        elif provider.lower() == "openai":
            await call_openai_api(
                api_key=api_key,
                model=model,
                system_prompt="You are a helpful assistant.",
                user_prompt="Hello, test connection.",
                tools=None,
                tool_choice=None
            )
        return True
    except Exception as e:
        logger.error(f"LLM connection test failed: {e}")
        return False