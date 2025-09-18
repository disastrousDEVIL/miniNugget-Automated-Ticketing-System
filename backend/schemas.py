from pydantic import BaseModel,HttpUrl
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    user_id: str
    order_id: str
    problem_text: str
    image_url: Optional[HttpUrl] = None
    restaurant_name: str   # ✅ new required field
class TicketOut(BaseModel):
    id: int
    user_id: str
    order_id: str
    problem_text: str
    image_url: Optional[str]
    status: str
    created_at: datetime
    restaurant_name: str
    reply_tag: Optional[str] = None
    reply_text: Optional[str] = None
    # final_confidence: Optional[float] = None  # Add this
    # decision: Optional[str] = None  # Add this