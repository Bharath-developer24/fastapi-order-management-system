# Order Management Backend System

A production-style backend application built using FastAPI and PostgreSQL for managing products, orders, payments, and inventory workflows.

---

## 🚀 Features

### Authentication
- User Signup
- User Login
- JWT Authentication
- Protected APIs

### Products
- Create Products
- Get Products
- Product Inventory Management
- Stock Validation

### Orders
- Create Orders
- Bulk Order Creation
- User-Specific Orders
- Order Status Updates
- Pagination Support

### Payments
- Create Payments
- Payment Status Handling
- Automatic Order Status Update After Payment

### Advanced Backend Features
- SQLAlchemy ORM Relationships
- Foreign Keys
- Nested API Responses
- Inventory Stock Reduction
- Environment Variable Configuration (.env)
- Timestamp Tracking

---

## 🛠️ Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication
- Python
- Uvicorn

---

## 📂 Project Structure

```bash
order_management/
│
├── app/
│   ├── model/
│   ├── schemas/
│   ├── utils/
│   ├── database.py
│   ├── main.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/order-management-fastapi.git
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv project_env
```

---

### 3️⃣ Activate Virtual Environment

#### Windows

```bash
project_env\Scripts\activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/order_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256
```

---

### 6️⃣ Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register user |
| POST | `/login` | Login user |

---

### Products

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Create product |
| GET | `/products` | Get products |

---

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders` | Create order |
| POST | `/orders/bulk` | Bulk create orders |
| GET | `/orders` | Get user orders |
| PUT | `/orders/{id}` | Update order |

---

### Payments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders/{id}/payment` | Create payment |

---

## 🔐 Authentication

Protected APIs require JWT token.

Example Header:

```text
Authorization: Bearer your_token
```

---

## 📈 Future Improvements

- Search & Filter APIs
- Soft Delete
- Docker Support
- Alembic Migrations

---

## 👨‍💻 Author

Bharath Akuleti
