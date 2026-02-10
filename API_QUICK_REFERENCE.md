# FastAPI Student Management - Quick Reference Guide

## Phase 1: Student CRUD Operations

### Base URL
```
http://localhost:8000
```

### Endpoints Overview

#### 1. Health Check
```
GET /api/health
```
**Response (200)**:
```json
{
  "status": "✅ API is running",
  "database": "Connected to MongoDB"
}
```

---

#### 2. Create Student
```
POST /api/students
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "roll": "CS001"
}
```

**Response (201)**:
```json
{
  "_id": "6989db210d3bbfe92c291201",
  "name": "John Doe",
  "email": "john@example.com",
  "roll": "CS001"
}
```

**Error Cases**:
- 400: Roll number already exists or invalid input
- 500: Server error

---

#### 3. Get All Students
```
GET /api/students?skip=0&limit=10
```

**Query Parameters**:
- `skip` (optional): Number of students to skip (default: 0)
- `limit` (optional): Maximum results (default: 10, max: 100)

**Response (200)**:
```json
[
  {
    "_id": "6989db210d3bbfe92c291201",
    "name": "John Doe",
    "email": "john@example.com",
    "roll": "CS001"
  },
  {
    "_id": "6989db2d0d3bbfe92c291202",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "roll": "CS002"
  }
]
```

---

#### 4. Get Single Student (NEW)
```
GET /api/students/{student_id}
```

**URL Parameters**:
- `student_id`: MongoDB ObjectId

**Response (200)**:
```json
{
  "_id": "6989db210d3bbfe92c291201",
  "name": "John Doe",
  "email": "john@example.com",
  "roll": "CS001"
}
```

**Error Cases**:
- 400: Invalid ObjectId format
- 404: Student not found
- 500: Server error

---

#### 5. Update Student (NEW)
```
PUT /api/students/{student_id}
Content-Type: application/json
```

**URL Parameters**:
- `student_id`: MongoDB ObjectId

**Request Body** (all fields optional):
```json
{
  "name": "Updated Name",
  "email": "newemail@example.com",
  "roll": "CS999"
}
```

**Response (200)**:
```json
{
  "_id": "6989db210d3bbfe92c291201",
  "name": "Updated Name",
  "email": "newemail@example.com",
  "roll": "CS999"
}
```

**Error Cases**:
- 400: Invalid ObjectId or roll number already exists
- 404: Student not found
- 422: Invalid input (bad email, empty strings, too long, etc.)
- 500: Server error

**Important Notes**:
- All fields in request body are optional
- Can update individual fields without affecting others
- Roll number validation is **case-insensitive** ✓
- Email must be in valid format

---

#### 6. Delete Student
```
DELETE /api/students/{student_id}
```

**URL Parameters**:
- `student_id`: MongoDB ObjectId

**Response (200)**:
```json
{
  "message": "Student 'John Doe' deleted successfully"
}
```

**Error Cases**:
- 400: Invalid ObjectId format
- 404: Student not found
- 500: Server error

---

#### 7. Get Student Count
```
GET /api/students/count
```

**Response (200)**:
```json
{
  "total_students": 42
}
```

---

## Validation Rules

| Field | Rules | Example |
|-------|-------|---------|
| **name** | 1-100 characters | "John Doe" |
| **email** | Valid email format | "john@example.com" |
| **roll** | 1-50 characters, unique (case-insensitive) | "CS001" |

---

## HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Student successfully created |
| 400 | Bad Request | Invalid ID format, duplicate roll, invalid input |
| 404 | Not Found | Student ID doesn't exist |
| 422 | Unprocessable | Validation error (invalid email, empty fields, etc.) |
| 500 | Server Error | Database or server issue |

---

## Important Bug Fixes

### ✅ Case-Insensitive Roll Number Validation
- Roll numbers are now validated **case-insensitively**
- "CS001", "cs001", and "Cs001" are all treated as the **same roll number**
- This applies to both CREATE and UPDATE operations

---

## Usage Examples

### Create a Student
```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "roll": "IT001"
  }'
```

### Get a Specific Student
```bash
curl http://localhost:8000/api/students/6989db210d3bbfe92c291201
```

### Update a Student's Email
```bash
curl -X PUT http://localhost:8000/api/students/6989db210d3bbfe92c291201 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.new@example.com"
  }'
```

### Update a Student's Name and Roll
```bash
curl -X PUT http://localhost:8000/api/students/6989db210d3bbfe92c291201 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Smith",
    "roll": "IT002"
  }'
```

### Delete a Student
```bash
curl -X DELETE http://localhost:8000/api/students/6989db210d3bbfe92c291201
```

### Get All Students (First 10)
```bash
curl "http://localhost:8000/api/students?skip=0&limit=10"
```

### Search Students (With Pagination)
```bash
curl "http://localhost:8000/api/students?skip=5&limit=20"
```

---

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000 (React Development)
- http://localhost:5173 (Vite Development)
- http://localhost:8000 (API Server)
- http://127.0.0.1:3000, :5173, :8000
- Custom origins via environment variables

---

## MongoDB Connection

**Database**: `student_db`
**Collection**: `students`

**Connection String**: 
```
mongodb://localhost:27017/ (default)
```

Configure via `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=student_db
COLLECTION_NAME=students
```

---

## Testing

Three comprehensive test suites are provided:

1. **test_get_put_endpoints.py** - Basic functionality tests
2. **test_edge_cases.py** - Edge case and validation tests  
3. **test_bug_fix.py** - Bug fix verification

Run all tests:
```bash
python test_get_put_endpoints.py
python test_edge_cases.py
python test_bug_fix.py
```

---

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

**Last Updated**: February 9, 2026
**Version**: 1.0.0
**Status**: ✅ Production Ready
