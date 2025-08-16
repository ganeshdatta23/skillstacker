from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.postgres import get_db
from db.models import User, Order, Product
from api.auth import get_current_user
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = 1

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str
    created_at: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[OrderResponse])
def get_user_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's orders"""
    try:
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
        return orders
    except Exception as e:
        logger.error(f"Error retrieving orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new order"""
    try:
        # Get product
        product = db.query(Product).filter(Product.id == order_data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Calculate total
        total_amount = product.price * order_data.quantity
        
        # Create order
        order = Order(
            user_id=current_user.id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            total_amount=total_amount
        )
        
        db.add(order)
        db.commit()
        db.refresh(order)
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")