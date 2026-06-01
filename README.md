# Inventory & Order Management System (IOMS)

A modern, production-quality SaaS dashboard for managing products, customers, orders, and inventory.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pytest
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Shadcn UI (Custom), React Query, Recharts
- **Containerization**: Docker, Docker Compose

## Features
- **Dashboard**: High-level metrics, inventory summary charts, low-stock alerts.
- **Product Management**: Track SKU, category, price, and stock levels.
- **Customer Management**: Maintain customer contact information.
- **Order Management**: Create orders, automatically calculate totals, and dynamically reduce stock. Prevents ordering out-of-stock items.
- **Authentication**: JWT-based secure authentication.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed.
- (Optional) Node.js 18+ and Python 3.11+ for local non-Docker development.

### Running with Docker (Recommended)

1. Rename the environment files:
   - `backend/.env.example` -> `backend/.env`
   - `frontend/.env.example` -> `frontend/.env`

2. Start the application:
   ```bash
   docker-compose up --build -d
   ```

3. The application will be available at:
   - Frontend: http://localhost:5173
   - Backend API Docs: http://localhost:8000/docs

4. To seed the database with initial data and an admin user, run:
   ```bash
   docker exec -it ioms_backend python seed.py
   ```

5. Log in to the frontend with:
   - **Email**: `admin@example.com`
   - **Password**: `password`

### Testing

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
pytest tests/
```
