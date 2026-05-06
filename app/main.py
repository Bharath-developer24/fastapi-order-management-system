from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status

from app.model.payment import Payment
from app.schemas.product import ProductCreate, ProductRead
from app.schemas.product import ProductCreate

from .database import SessionLocal, Base, engine
from app.utils.security import get_current_user, hash_password, verify_password, create_token

from app.model import User, Order , Product, Payment

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.payment import PaymentCreate, PaymentRead


app = FastAPI()

Base.metadata.create_all(bind=engine)

from app.dependencies import get_db


@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: SessionLocal = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
    new_user = User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(user: UserLogin, db: SessionLocal = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    token = create_token({"sub": existing_user.email})
        
    return {"access_token": token, "token_type": "bearer"}


@app.post("/orders", response_model=OrderRead)
def create_order(order: OrderCreate, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    product_qty = db.query(Product).filter(Product.id == order.product_id).first()
    if product_qty.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    product_qty.stock -= order.quantity
    
    new_order = Order(
                item=order.item,
                user_id=current_user.id,
                status="pending",
                quantity=order.quantity,
                product_id=order.product_id)
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@app.post("/orders/bulk", response_model=list[OrderRead])
def create_orders(orders: list[OrderCreate], db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id.in_([order.product_id for order in orders])).all()
    product_qty = {p.id: p.stock for p in product}
    for order in orders:
        if order.product_id not in product_qty or product_qty[order.product_id] < order.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product  {order.item}")
        
        product_qty[order.product_id] -= order.quantity    
        product_to_update = db.query(Product).filter(Product.id == order.product_id).first()
        product_to_update.stock = product_qty[order.product_id]
        
    new_orders = []
    for order in orders:
        new_order = Order(
            item=order.item,
            user_id=current_user.id,
            product_id=order.product_id,
            status=order.status if order.status else "pending",
            quantity=order.quantity,
        )
        new_orders.append(new_order)


    db.add_all(new_orders)
    db.commit()
    for order in new_orders:
        db.refresh(order)
    return new_orders


@app.get("/orders", response_model=list[OrderRead])
def get_orders(page: int = 1, page_size: int = 5, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    skip = (page - 1) * page_size
    orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(page_size).all()
    return orders

@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: SessionLocal = Depends(get_db), current_user : User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}")
def update_order(order_id: int, order_update: OrderCreate, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.item = order_update.item
    order.status = order_update.status
    db.commit()
    db.refresh(order)
    return {
        "message": "Order updated successfully",
        "order": order
    }

@app.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return  {
        "message": "Order status updated successfully",
        "order": order
    }

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}


@app.get("/users/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/all_users", response_model=list[UserResponse])
def get_all_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return users



@app.post("/payments", response_model=PaymentRead)
def create_payment(payment: PaymentCreate, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_payment = db.query(Payment).filter(Payment.order_id == payment.order_id).first() 
    
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment for this order already exists")  
    new_payment = Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        payment_status=payment.payment_status if payment.payment_status else "pending",
        payment_at=payment.payment_status == "completed" and datetime.utcnow() or None
    )
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@app.get("/payments/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.patch("/payments/{payment_id}/status")
def update_payment_status(payment_id: int, payment_status: str, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.payment_status = payment_status
    payment.payment_at = payment_status == "completed" and datetime.utcnow() or None
    db.commit()
    db.refresh(payment)
    return {
        "message": "Payment status updated successfully",
        "payment": payment
    }



@app.get("/products", response_model=list[ProductRead])
def get_products(db: SessionLocal = Depends(get_db)):
    products = db.query(Product).all()
    return products



@app.post("/products",response_model=ProductRead)
def create_product(product: ProductCreate, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_product = Product(name=product.name, description=product.description, price=product.price, stock=product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



@app.post("/products/bulk", response_model=list[ProductRead])
def create_products(products: list[ProductCreate], db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_products = []
    for product in products:
        new_product = Product(name=product.name, description=product.description, price=product.price, stock=product.stock)
        new_products.append(new_product)

    db.add_all(new_products)
    db.commit()
    for product in new_products:
        db.refresh(product)
    return new_products
