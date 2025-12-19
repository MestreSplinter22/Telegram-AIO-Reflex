"""API endpoints for GiftCard table operations using Reflex ORM."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import reflex as rx
from ...models.models import GiftCard

app = FastAPI()

class GiftCardCreate(BaseModel):
    code: str
    category: str
    value: float
    cost_price: float
    selling_price: float
    status: str = "active"
    redeemed_by: Optional[str] = None

class GiftCardResponse(BaseModel):
    id: int
    code: str
    category: str
    value: float
    cost_price: float
    selling_price: float
    status: str
    created_at: datetime
    redeemed_by: Optional[str] = None
    redeemed_at: Optional[datetime] = None

def register_giftcards_routes(fastapi_app: FastAPI):
    """Register gift card API routes with the FastAPI app."""
    
    @fastapi_app.post("/api/giftcards", response_model=GiftCardResponse)
    async def create_giftcard(giftcard: GiftCardCreate):
        """Create a new gift card."""
        try:
            with rx.session() as session:
                new_giftcard = GiftCard(
                    code=giftcard.code,
                    category=giftcard.category,
                    value=giftcard.value,
                    cost_price=giftcard.cost_price,
                    selling_price=giftcard.selling_price,
                    status=giftcard.status,
                    redeemed_by=giftcard.redeemed_by,
                    created_at=datetime.utcnow()
                )
                session.add(new_giftcard)
                session.commit()
                session.refresh(new_giftcard)
                
                return GiftCardResponse(
                    id=new_giftcard.id,
                    code=new_giftcard.code,
                    category=new_giftcard.category,
                    value=new_giftcard.value,
                    cost_price=new_giftcard.cost_price,
                    selling_price=new_giftcard.selling_price,
                    status=new_giftcard.status,
                    created_at=new_giftcard.created_at,
                    redeemed_by=new_giftcard.redeemed_by,
                    redeemed_at=new_giftcard.redeemed_at
                )
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating gift card: {str(e)}")

    @fastapi_app.get("/api/giftcards", response_model=list[GiftCardResponse])
    async def get_all_giftcards():
        """Get all gift cards."""
        try:
            with rx.session() as session:
                giftcards = session.query(GiftCard).all()
                return [
                    GiftCardResponse(
                        id=giftcard.id,
                        code=giftcard.code,
                        category=giftcard.category,
                        value=giftcard.value,
                        cost_price=giftcard.cost_price,
                        selling_price=giftcard.selling_price,
                        status=giftcard.status,
                        created_at=giftcard.created_at,
                        redeemed_by=giftcard.redeemed_by,
                        redeemed_at=giftcard.redeemed_at
                    )
                    for giftcard in giftcards
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching gift cards: {str(e)}")

    @fastapi_app.get("/api/giftcards/{code}", response_model=GiftCardResponse)
    async def get_giftcard_by_code(code: str):
        """Get gift card by code."""
        try:
            with rx.session() as session:
                giftcard = session.query(GiftCard).filter(GiftCard.code == code).first()
                if not giftcard:
                    raise HTTPException(status_code=404, detail=f"Gift card with code '{code}' not found")
                
                return GiftCardResponse(
                    id=giftcard.id,
                    code=giftcard.code,
                    category=giftcard.category,
                    value=giftcard.value,
                    cost_price=giftcard.cost_price,
                    selling_price=giftcard.selling_price,
                    status=giftcard.status,
                    created_at=giftcard.created_at,
                    redeemed_by=giftcard.redeemed_by,
                    redeemed_at=giftcard.redeemed_at
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching gift card: {str(e)}")

    @fastapi_app.get("/api/giftcards/category/{category}", response_model=list[GiftCardResponse])
    async def get_giftcards_by_category(category: str):
        """Get all gift cards by category."""
        try:
            with rx.session() as session:
                giftcards = session.query(GiftCard).filter(GiftCard.category == category).all()
                return [
                    GiftCardResponse(
                        id=giftcard.id,
                        code=giftcard.code,
                        category=giftcard.category,
                        value=giftcard.value,
                        cost_price=giftcard.cost_price,
                        selling_price=giftcard.selling_price,
                        status=giftcard.status,
                        created_at=giftcard.created_at,
                        redeemed_by=giftcard.redeemed_by,
                        redeemed_at=giftcard.redeemed_at
                    )
                    for giftcard in giftcards
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching gift cards by category: {str(e)}")

    @fastapi_app.get("/api/giftcards/status/{status}", response_model=list[GiftCardResponse])
    async def get_giftcards_by_status(status: str):
        """Get all gift cards by status."""
        try:
            with rx.session() as session:
                giftcards = session.query(GiftCard).filter(GiftCard.status == status).all()
                return [
                    GiftCardResponse(
                        id=giftcard.id,
                        code=giftcard.code,
                        category=giftcard.category,
                        value=giftcard.value,
                        cost_price=giftcard.cost_price,
                        selling_price=giftcard.selling_price,
                        status=giftcard.status,
                        created_at=giftcard.created_at,
                        redeemed_by=giftcard.redeemed_by,
                        redeemed_at=giftcard.redeemed_at
                    )
                    for giftcard in giftcards
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching gift cards by status: {str(e)}")

    @fastapi_app.put("/api/giftcards/{code}", response_model=GiftCardResponse)
    async def update_giftcard(code: str, giftcard: GiftCardCreate):
        """Update gift card by code."""
        try:
            with rx.session() as session:
                existing_giftcard = session.query(GiftCard).filter(GiftCard.code == code).first()
                if not existing_giftcard:
                    raise HTTPException(status_code=404, detail=f"Gift card with code '{code}' not found")
                
                existing_giftcard.category = giftcard.category
                existing_giftcard.value = giftcard.value
                existing_giftcard.cost_price = giftcard.cost_price
                existing_giftcard.selling_price = giftcard.selling_price
                existing_giftcard.status = giftcard.status
                existing_giftcard.redeemed_by = giftcard.redeemed_by
                session.commit()
                session.refresh(existing_giftcard)
                
                return GiftCardResponse(
                    id=existing_giftcard.id,
                    code=existing_giftcard.code,
                    category=existing_giftcard.category,
                    value=existing_giftcard.value,
                    cost_price=existing_giftcard.cost_price,
                    selling_price=existing_giftcard.selling_price,
                    status=existing_giftcard.status,
                    created_at=existing_giftcard.created_at,
                    redeemed_by=existing_giftcard.redeemed_by,
                    redeemed_at=existing_giftcard.redeemed_at
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating gift card: {str(e)}")

    @fastapi_app.delete("/api/giftcards/{code}")
    async def delete_giftcard(code: str):
        """Delete gift card by code."""
        try:
            with rx.session() as session:
                giftcard = session.query(GiftCard).filter(GiftCard.code == code).first()
                if not giftcard:
                    raise HTTPException(status_code=404, detail=f"Gift card with code '{code}' not found")
                
                session.delete(giftcard)
                session.commit()
                return {"message": f"Gift card with code '{code}' deleted successfully"}
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting gift card: {str(e)}")