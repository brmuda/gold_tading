
# Gold Trading API

Django REST API for managing gold transactions with a simple web interface.

## Technologies
- Django 5.0.1
- Django REST Framework 3.14.0
- PostgreSQL
- Docker & Docker Compose
- Bootstrap 5.3.2



## Setup and Installation

1. Clone repository
```bash
git clone <repository-url>
cd gold_trading
```

2. Start services
```bash
docker-compose up --build
```

## Default Admin User
- Username: admin
- Password: 123456
- Phone: 09019601335

## API Endpoints

### Buy Gold
```http
POST /transactions/buy/
Content-Type: application/json

{
    "user_id": 1,
    "amount_rial": 5000000
}
```

### Sell Gold
```http
POST /transactions/sell/
Content-Type: application/json

{
    "user_id": 1,
    "gold_weight_gram": 0.5
}
```

### Transaction History 
```http
GET /transactions/user/{user_id}/
```

## Validation Rules
- Fixed gold price: 10,000,000 Rials/gram
- Users cannot sell more gold than their balance
- All transactions are stored in PostgreSQL
- Transaction status tracking: completed/failed

## Web Interface
Access the web interface at http://localhost:8000
- Buy/Sell gold with real-time validation
- View transaction history by user ID
- Responsive Bootstrap UI
```
