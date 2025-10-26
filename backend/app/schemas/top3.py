from pydantic import BaseModel, Field
from typing import List, Optional

class ProductRecommendation(BaseModel):
    """
    Product recommendation schema
    """
    rank: int = Field(..., description="Ranking position (1, 2, or 3)")
    product_name: str = Field(..., description="Product name and model")
    description: str = Field(..., description="Recommendation reason (2-3 sentences)")
    source_link: str = Field(..., description="Source link for the recommendation")

class KeywordRequest(BaseModel):
    """
    Request schema for getting top 3 recommendations
    """
    keyword: str = Field(..., min_length=1, max_length=100, description="Product keyword to search for")

class Top3Response(BaseModel):
    """
    Response schema for top 3 recommendations
    """
    status: str = Field(..., description="Response status")
    data: List[ProductRecommendation] = Field(..., description="List of top 3 recommendations")

class ProductRecommendationInDB(BaseModel):
    """
    Schema for storing product recommendations in database (if needed)
    """
    id: Optional[int] = None
    keyword: str
    rank: int
    product_name: str
    description: str
    source_link: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True