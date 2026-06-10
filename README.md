# FastAPI CRUD Application

A simple yet complete CRUD (Create, Read, Update, Delete) application built with FastAPI and SQLAlchemy.

## Features

- **Create Users**: Add new users to the system
- **Read Users**: Retrieve all users or a specific user by ID
- **Update Users**: Modify user information
- **Delete Users**: Remove users from the system
- **PostgreSQL Integration**: Persistent data storage
- **Type Safety**: Full type hints throughout the codebase
- **API Documentation**: Auto-generated Swagger UI and ReDoc

## Project Structure

```
fastapi-crud/
├── models/          # SQLAlchemy ORM models
├── routers/         # API endpoint routers
├── schemas/         # Pydantic request/response schemas
├── main.py          # Application entry point
├── db.py            # Database configuration
├── pyproject.toml   # Project dependencies
└── .env.example     # Environment variables template
```

## Requirements

- Python 3.10+
- PostgreSQL 12+
- UV (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vijolouis01/fastapi-crud.git
cd fastapi-crud
```

2. Install dependencies using UV:
```bash
uv sync
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the application:
```bash
uv run fastapi dev main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Users

- **POST** `/users/` - Create a new user
- **GET** `/users/` - Get all users
- **GET** `/users/{user_id}` - Get a specific user
- **PUT** `/users/{user_id}` - Update a user
- **DELETE** `/users/{user_id}` - Delete a user

## Example Usage

```bash
# Create a user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# Get all users
curl "http://localhost:8000/users/"

# Get a specific user
curl "http://localhost:8000/users/1"

# Update a user
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'

# Delete a user
curl -X DELETE "http://localhost:8000/users/1"
```

## Documentation

- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## License

MIT
