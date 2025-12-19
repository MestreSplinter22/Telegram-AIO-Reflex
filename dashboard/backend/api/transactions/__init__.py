"""API endpoints for Transaction table operations using Reflex ORM."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import reflex as rx
from ...models.models import Transaction

app = FastAPI()

class TransactionCreate(BaseModel):
    user_id: str
    type: str  # deposit, purchase, refund, manual_adjustment
    amount: float
    description: str
    status: str = "pending"
    pix_key: Optional[str] = None
    extra_data: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: str
    type: str
    amount: float
    description: str
    status: str
    timestamp: datetime
    pix_key: Optional[str] = None
    extra_data: Optional[str] = None

def register_transactions_routes(fastapi_app: FastAPI):
    """Register transaction API routes with the FastAPI app."""
    
    @fastapi_app.post("/api/transactions", response_model=TransactionResponse)
    async def create_transaction(transaction: TransactionCreate):
        """Create a new transaction."""
        try:
            with rx.session() as session:
                new_transaction = Transaction(
                    user_id=transaction.user_id,
                    type=transaction.type,
                    amount=transaction.amount,
                    description=transaction.description,
                    status=transaction.status,
                    pix_key=transaction.pix_key,
                    extra_data=transaction.extra_data,
                    timestamp=datetime.utcnow()
                )
                session.add(new_transaction)
                session.commit()
                session.refresh(new_transaction)
                
                return TransactionResponse(
                    id=new_transaction.id,
                    user_id=new_transaction.user_id,
                    type=new_transaction.type,
                    amount=new_transaction.amount,
                    description=new_transaction.description,
                    status=new_transaction.status,
                    timestamp=new_transaction.timestamp,
                    pix_key=new_transaction.pix_key,
                    extra_data=new_transaction.extra_data
                )
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")

    @fastapi_app.get("/api/transactions", response_model=list[TransactionResponse])
    async def get_all_transactions():
        """Get all transactions."""
        try:
            with rx.session() as session:
                transactions = session.query(Transaction).all()
                return [
                    TransactionResponse(
                        id=transaction.id,
                        user_id=transaction.user_id,
                        type=transaction.type,
                        amount=transaction.amount,
                        description=transaction.description,
                        status=transaction.status,
                        timestamp=transaction.timestamp,
                        pix_key=transaction.pix_key,
                        extra_data=transaction.extra_data
                    )
                    for transaction in transactions
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching transactions: {str(e)}")

    @fastapi_app.get("/api/transactions/{transaction_id}", response_model=TransactionResponse)
    async def get_transaction_by_id(transaction_id: int):
        """Get transaction by ID."""
        try:
            with rx.session() as session:
                transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
                if not transaction:
                    raise HTTPException(status_code=404, detail=f"Transaction with ID '{transaction_id}' not found")
                
                return TransactionResponse(
                    id=transaction.id,
                    user_id=transaction.user_id,
                    type=transaction.type,
                    amount=transaction.amount,
                    description=transaction.description,
                    status=transaction.status,
                    timestamp=transaction.timestamp,
                    pix_key=transaction.pix_key,
                    extra_data=transaction.extra_data
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching transaction: {str(e)}")

    @fastapi_app.get("/api/transactions/user/{user_id}", response_model=list[TransactionResponse])
    async def get_transactions_by_user(user_id: str):
        """Get all transactions for a specific user."""
        try:
            with rx.session() as session:
                transactions = session.query(Transaction).filter(Transaction.user_id == user_id).all()
                return [
                    TransactionResponse(
                        id=transaction.id,
                        user_id=transaction.user_id,
                        type=transaction.type,
                        amount=transaction.amount,
                        description=transaction.description,
                        status=transaction.status,
                        timestamp=transaction.timestamp,
                        pix_key=transaction.pix_key,
                        extra_data=transaction.extra_data
                    )
                    for transaction in transactions
                ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user transactions: {str(e)}")

    @fastapi_app.put("/api/transactions/{transaction_id}", response_model=TransactionResponse)
    async def update_transaction(transaction_id: int, transaction: TransactionCreate):
        """Update transaction by ID."""
        try:
            with rx.session() as session:
                existing_transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
                if not existing_transaction:
                    raise HTTPException(status_code=404, detail=f"Transaction with ID '{transaction_id}' not found")
                
                existing_transaction.user_id = transaction.user_id
                existing_transaction.type = transaction.type
                existing_transaction.amount = transaction.amount
                existing_transaction.description = transaction.description
                existing_transaction.status = transaction.status
                existing_transaction.pix_key = transaction.pix_key
                existing_transaction.extra_data = transaction.extra_data
                session.commit()
                session.refresh(existing_transaction)
                
                return TransactionResponse(
                    id=existing_transaction.id,
                    user_id=existing_transaction.user_id,
                    type=existing_transaction.type,
                    amount=existing_transaction.amount,
                    description=existing_transaction.description,
                    status=existing_transaction.status,
                    timestamp=existing_transaction.timestamp,
                    pix_key=existing_transaction.pix_key,
                    extra_data=existing_transaction.extra_data
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating transaction: {str(e)}")

    @fastapi_app.delete("/api/transactions/{transaction_id}")
    async def delete_transaction(transaction_id: int):
        """Delete transaction by ID."""
        try:
            with rx.session() as session:
                transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
                if not transaction:
                    raise HTTPException(status_code=404, detail=f"Transaction with ID '{transaction_id}' not found")
                
                session.delete(transaction)
                session.commit()
                return {"message": f"Transaction with ID '{transaction_id}' deleted successfully"}
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting transaction: {str(e)}")