# Welcome to Your Miaoda Project
Miaoda Application Link URL
    URL:https://medo.dev/projects/app-8avkpm7095hd

# Canteen Manager Dashboard

A Python Flask application for canteen managers to view and manage student orders.

## Features

- View all orders with student details (name, roll number, branch, year)
- Real-time statistics dashboard
- Order details with itemized list
- Auto-refresh every 30 seconds
- Clean and responsive UI

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd manager-app
pip install -r requirements.txt
```

### 2. Environment Variables

The app reads from the `.env` file in the parent directory. Make sure it contains:

```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Run the Application

```bash
python app.py
```

The manager dashboard will be available at: `http://localhost:5000`

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/orders` - Get all orders with student details
- `GET /api/orders/stats` - Get order statistics

## Dashboard Features

### Statistics Cards
- **Total Orders**: Total number of orders placed
- **Total Revenue**: Total revenue from all orders
- **Today's Orders**: Number of orders placed today
- **Today's Revenue**: Revenue generated today

### Order Cards
Each order displays:
- Order ID and timestamp
- Student information (name, roll number, branch, year)
- Itemized list of products ordered
- Total amount
- Order status

## Technology Stack

- **Backend**: Python Flask
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
