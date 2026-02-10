# Phase 1: Quick Reference & Implementation Guide

## ✅ What's Implemented

### REST API Endpoints
```
POST   /api/students              → Create new student
GET    /api/students              → Get all students  
GET    /api/students/{id}         → Get single student
PUT    /api/students/{id}         → Update student
DELETE /api/students/{id}         → Delete student
```

### Features
- ✅ Input validation with Pydantic
- ✅ Error handling with proper HTTP status codes
- ✅ MongoDB integration
- ✅ CORS configuration for React frontend
- ✅ Environment configuration (.env)
- ✅ Duplicate roll number prevention
- ✅ ObjectId validation
- ✅ Text embeddings generation
- ✅ Comprehensive test suite

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB
Edit `.env`:
```dotenv
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=student_db
COLLECTION_NAME=students
```

### 3. Start API Server
```bash
uvicorn app:app --reload
```
→ Server runs at: `http://localhost:8000`

### 4. Access Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Test the API
```bash
python test_phase1_api.py
```

---

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | FastAPI application with CRUD endpoints |
| `models.py` | Pydantic validation models |
| `.env` | Environment configuration |
| `test_phase1_api.py` | Comprehensive test suite |
| `requirements.txt` | Python dependencies |

---

## API Examples

### Create Student
```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","roll":"CS001"}'
```

### Get All
```bash
curl http://localhost:8000/api/students
```

### Update
```bash
curl -X PUT http://localhost:8000/api/students/{id} \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane"}'
```

### Delete
```bash
curl -X DELETE http://localhost:8000/api/students/{id}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 201 | Created |
| 200 | Success |
| 204 | No Content (deleted) |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict (duplicate) |
| 422 | Validation Error |
| 500 | Server Error |

---

## Response Examples

### Success (201 Created)
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "John Doe",
  "email": "john@example.com",
  "roll": "CS001"
}
```

### Error (409 Conflict)
```json
{
  "detail": "Roll number 'CS001' already exists"
}
```

### Error (422 Validation)
```json
{
  "detail": [
    {
      "type": "value_error.email",
      "loc": ["body", "email"],
      "msg": "invalid email format"
    }
  ]
}
```

---

## Environment Variables

```dotenv
# MongoDB
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=student_db
COLLECTION_NAME=students

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000
```

---

## Testing

### Run All Tests
```bash
python test_phase1_api.py
```

### Test Categories
- Health check
- Create (valid, duplicate)
- Read (all, single, invalid, non-existent)
- Update (valid, duplicate roll)
- Delete (valid, non-existent)
- Validation (missing fields, invalid email)

---

## Common Issues & Solutions

**MongoDB Connection Error**
- Check MongoDB is running
- Verify MONGODB_URL in .env

**Port 8000 Already in Use**
- Change port: `--port 8001`
- Or kill process: `lsof -ti:8000 | xargs kill -9`

**Import Errors**
- Run: `pip install -r requirements.txt`

**CORS Errors**
- Add frontend URL to ALLOWED_ORIGINS in .env

---

## Next Phase (Phase 2)

React project setup with:
- React Router
- Axios
- Tailwind CSS
- Component structure

See: REACT_MIGRATION_PLAN.md for Phase 2 details

---

## Important Notes

1. **Roll Number**: Must be unique across all students
2. **Email**: Must be valid email format
3. **ID**: Use returned `_id` for updates/deletes
4. **Embeddings**: Auto-generated for ML features
5. **Backward Compatibility**: Old template endpoints still work

---

**Status**: ✅ Phase 1 Complete - Ready for Phase 2
