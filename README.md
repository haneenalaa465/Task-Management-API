# Task Management API

A comprehensive task management API built with FastAPI, SQLModel, and Pydantic.

## Features

### Core Features
- ✅ Full CRUD operations for tasks
- ✅ Data validation with Pydantic
- ✅ SQLite database with SQLModel ORM
- ✅ Automatic API documentation
- ✅ Comprehensive error handling
- ✅ Pagination support
- ✅ Filtering by status and priority

### Bonus Features
- ✅ Advanced filtering with multiple simultaneous filters
- ✅ Sorting by different fields (created_at, updated_at, due_date, title, priority, status)
- ✅ Text search in title and description
- ✅ Bulk operations (update/delete multiple tasks)
- ✅ Unit tests with pytest
- ✅ Docker support with docker-compose
- ✅ Environment configuration
- ✅ Health check endpoint
- ✅ CORS middleware

## Quick Start

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/haneenalaa465/Task-Management-API
   cd task-management-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Option 2: Docker

1. **Using Docker Compose (Recommended)**
   ```bash
   docker-compose up --build
   ```

2. **Using Docker only**
   ```bash
   docker build -t task-api .
   docker run -p 8000:8000 task-api
   ```

## API Documentation

Once running, visit:
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc
- **API Info**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `POST /tasks` - Create task
- `GET /tasks` - List tasks (with filtering, sorting, pagination)
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `GET /tasks/status/{status}` - Get tasks by status
- `GET /tasks/priority/{priority}` - Get tasks by priority

### Bonus Endpoints
- `PUT /tasks/bulk` - Bulk update tasks
- `DELETE /tasks/bulk` - Bulk delete tasks

## Example Usage

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Complete project documentation",
       "description": "Write comprehensive API documentation",
       "priority": "high",
       "due_date": "2024-12-31T23:59:59"
     }'
```

### List Tasks with Filters
```bash
curl "http://localhost:8000/tasks?status=pending&priority=high&search=project&sort_by=due_date&sort_order=asc&skip=0&limit=10"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "completed",
       "description": "Documentation completed successfully"
     }'
```

### Bulk Update Tasks
```bash
curl -X PUT "http://localhost:8000/tasks/bulk" \
     -H "Content-Type: application/json" \
     -d '{
       "task_ids": [1, 2, 3],
       "update_data": {
         "status": "in_progress",
         "assigned_to": "John Doe"
       }
     }'
```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

## Environment Variables

Create a `.env` file:
```env
DATABASE_URL=sqlite:///./tasks.db
ENVIRONMENT=development
DEBUG=True
```

## Task Model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier |
| title | String | Required, Max 200 chars | Task title |
| description | String | Optional, Max 1000 chars | Task description |
| status | Enum | Required, Default: "pending" | Task status |
| priority | Enum | Required, Default: "medium" | Task priority |
| created_at | DateTime | Auto-generated | Creation timestamp |
| updated_at | DateTime | Optional | Last update timestamp |
| due_date | DateTime | Optional | Task deadline |
| assigned_to | String | Optional, Max 100 chars | Assignee name |

### Enums
- **TaskStatus**: pending, in_progress, completed, cancelled
- **TaskPriority**: low, medium, high, urgent

## Advanced Features

### Filtering
- Filter by status: `?status=pending`
- Filter by priority: `?priority=high`
- Search in title/description: `?search=project`
- Combine filters: `?status=pending&priority=high&search=urgent`

### Sorting
- Sort by field: `?sort_by=due_date`
- Sort order: `?sort_order=asc` or `?sort_order=desc`
- Available sort fields: created_at, updated_at, due_date, title, priority, status

### Pagination
- Skip records: `?skip=20`
- Limit results: `?limit=10`
- Response includes pagination metadata

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Development

### Project Structure
```
task_management_api/
├── main.py              # FastAPI app
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── database.py          # DB configuration
├── crud.py              # Database operations
├── routers/
│   └── tasks.py         # API routes
├── tests/
│   └── test_tasks.py    # Unit tests
├── requirements.txt     # Dependencies
├── Dockerfile          # Docker config
└── docker-compose.yml  # Docker compose
```

### Adding New Features
1. Define models in `models.py`
2. Create schemas in `schemas.py`
3. Add CRUD operations in `crud.py`
4. Create routes in `routers/`
5. Add tests in `tests/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request
