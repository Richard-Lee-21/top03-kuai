import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache import get_redis_client
from app.models.configuration import Configuration

logger = logging.getLogger(__name__)

async def load_app_config(db: AsyncSession, cache_client) -> dict:
    """
    Load application configuration from database with caching
    """
    cache_key = "app:config"
    
    # Try to get from cache first
    cached_config = await cache_client.get(cache_key)
    if cached_config:
        logger.debug("Loading configuration from cache")
        return json.loads(cached_config)
    
    # Load from database
    logger.info("Loading configuration from database")
    result = await db.execute("SELECT key, value FROM configuration WHERE value IS NOT NULL")
    config_data = result.fetchall()
    
    # Convert to dictionary
    config = {}
    for key, value in config_data:
        config[key] = value
    
    # Cache for 5 minutes
    await cache_client.setex(cache_key, 300, json.dumps(config))
    
    logger.info(f"Loaded {len(config)} configuration items")
    return config

async def get_default_config() -> dict:
    """
    Get default configuration values
    """
    return {
        # API Configuration
        "SEARCH_PROVIDER": "serper",
        "LLM_PROVIDER": "anthropic",
        "LLM_MODEL_NAME": "claude-3-opus-20240229",
        
        # LLM Prompts
        "LLM_SYSTEM_PROMPT": """你是一个世界级的产品分析师和市场调研专家。你的任务是分析给定的实时网络搜索结果，以找出关于特定商品的全网最佳推荐。

你需要基于以下的搜索结果（包括网页标题、摘要和链接），为用户寻找的商品综合判断出 Top 3 推荐。

你的判断标准应该是：
1.  **专家评测 (Expert Reviews):** 是否被知名科技媒体、评测机构（如 消费者报告、Rtings.com、The Verge 等）高度评价。
2.  **用户口碑 (User Consensus):** 在论坛（如 Reddit）、电商平台上的普遍用户反馈如何。
3.  **综合价值 (Overall Value):** 结合性能、价格和功能，是否具有高性价比或绝对的性能优势。

你必须使用提供的 `report_top3_products` 工具来格式化你的答案。你不能，也绝不能，在没有搜索结果支持的情况下编造产品或信息。""",
        
        "LLM_USER_PROMPT_TEMPLATE": """请根据以下实时网络搜索结果，分析并推荐用户想要的 Top 3 商品。

用户搜索的关键词是："[USER_KEYWORD]"

以下是为你抓取的全网搜索结果（格式为：[标题] - [链接] - [摘要]）：

---[搜索结果开始]---
[SEARCH_RESULTS]
---[搜索结果结束]---

请立即分析这些材料，并调用 `report_top3_products` 工具返回你的 Top 3 推荐。""",
        
        "LLM_TOOL_DEFINITION": """{
  "name": "report_top3_products",
  "description": "用于报告分析得出的Top 3产品推荐。",
  "input_schema": {
    "type": "object",
    "properties": {
      "recommendations": {
        "type": "array",
        "description": "包含3个推荐商品的列表。",
        "items": {
          "type": "object",
          "properties": {
            "rank": {
              "type": "integer",
              "description": "排名 (1, 2, 或 3)"
            },
            "product_name": {
              "type": "string",
              "description": "商品的具体名称和型号 (例如 '索尼 WH-1000XM5')"
            },
            "description": {
              "type": "string",
              "description": "一段精炼的推荐理由 (2-3句话)，总结为什么它被推荐，基于搜索结果中的评测和口碑。"
            },
            "source_link": {
              "type": "string",
              "description": "从搜索结果中找到的最相关的一个链接 (例如，官方页面、权威评测文章或主要零售商链接)。"
            }
          },
          "required": ["rank", "product_name", "description", "source_link"]
        }
      }
    },
    "required": ["recommendations"]
  }
}""",
        
        # Default API keys (empty)
        "SERPER_API_KEY": "",
        "LLM_API_KEY": ""
    }