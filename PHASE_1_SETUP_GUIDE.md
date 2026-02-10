# Phase 1: Backend API Development - Setup & Implementation Guide

## ✅ Status: COMPLETE & READY TO USE

---

## 📋 What's Implemented

### Backend API (FastAPI)
- ✅ **REST API Framework**: FastAPI with automatic OpenAPI documentation
- ✅ **Database**: MongoDB integration with PyMongo
- ✅ **Validation**: Pydantic models with automatic input validation
- ✅ **CORS**: Configured for React/Vite frontend development
- ✅ **Error Handling**: Comprehensive error responses with HTTP status codes
- ✅ **Logging**: Configured logging for debugging and monitoring

### Student CRUD Endpoints
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| **POST** | `/api/students` | Create new student | ✅ |
| **GET** | `/api/students` | Get all students (paginated) | ✅ |
| **GET** | `/api/students/count` | Get total student count | ✅ |
| **GET** | `/api/students/{id}` | Get specific student | ✅ |
| **PUT** | `/api/students/{id}` | Update student | ✅ |
| **DELETE** | `/api/students/{id}` | Delete student | ✅ |
| **GET** | `/api/health` | Health check | ✅ |

---

## 🔧 Environment Configuration

### `.env` File Setup
The `.env` file is already created with the following configuration:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=student_db
COLLECTION_NAME=students

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:8000
```

### Configuration Options

#### MongoDB Connection
- **Local MongoDB**: `mongodb://localhost:27017/`
- **MongoDB Atlas**:
  ```
  mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
  ```

#### CORS Origins
The following origins are allowed by default:
- `http://localhost:3000` - React dev server
- `http://localhost:5173` - Vite dev server
- `http://localhost:8000` - API server
- `http://127.0.0.1:3000` - React (localhost alias)
- `http://127.0.0.1:5173` - Vite (localhost alias)
- `http://127.0.0.1:8000` - API (localhost alias)

---

## 📦 Dependencies

### Required Packages
All packages are listed in `requirements.txt`:

```
fastapi==0.104.1           # Web framework
uvicorn[standard]==0.24.0  # ASGI server
pymongo==4.6.0             # MongoDB driver
pydantic==2.5.2            # Data validation
pydantic-settings==2.1.0   # Settings management
email-validator==2.1.0     # Email validation
python-dotenv==1.0.0       # Environment variables
gunicorn==21.2.0           # Production server
```

### Installation
```bash
# Navigate to project directory
cd c:\Users\manik.bhardwaj\.vscode\python

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Getting Started

### Step 1: Verify MongoDB is Running

#### Option A: Local MongoDB
```bash
# Check if MongoDB is running
mongod --version

# Start MongoDB (if not running as service)
mongod
```

#### Option B: MongoDB Atlas (Cloud)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a project and cluster
3. Get your connection string
4. Update `.env`:
   ```env
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=student_db
   COLLECTION_NAME=students
   ```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start the API Server

#### Development Mode (with auto-reload)
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode
```bash
gunicorn api:app -w 4 -b 0.0.0.0:8000 --access-logfile -
```

#### Expected Output
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
✅ Connected to MongoDB: student_db.students
✅ CORS configured for origins: http://localhost:3000, ...
```

---

## 📚 API Documentation

### Automatic Documentation
Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Example API Requests

#### 1. Create a Student
```bash
curl -X POST "http://localhost:8000/api/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "roll": "CS001"
  }'
```

**Response (201 Created)**:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "roll": "CS001"
}
```

#### 2. Get All Students
```bash
curl "http://localhost:8000/api/students?skip=0&limit=10"
```

**Response (200 OK)**:
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "roll": "CS001"
  }
]
```

#### 3. Get Specific Student
```bash
curl "http://localhost:8000/api/students/507f1f77bcf86cd799439011"
```

#### 4. Update Student
```bash
curl -X PUT "http://localhost:8000/api/students/507f1f77bcf86cd799439011" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
  }'
```

#### 5. Delete Student
```bash
curl -X DELETE "http://localhost:8000/api/students/507f1f77bcf86cd799439011"
```

#### 6. Health Check
```bash
curl "http://localhost:8000/api/health"
```

---

## 🧪 Testing the API

### Using Python Requests
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Create student
response = requests.post(
    f"{BASE_URL}/students",
    json={
        "name": "Alice Smith",
        "email": "alice@example.com",
        "roll": "CS002"
    }
)
print(response.json())
```

### Using JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:8000/api/students', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Bob Wilson',
    email: 'bob@example.com',
    roll: 'CS003'
  })
});
const data = await response.json();
console.log(data);
```

### Using Postman
1. Import API collection from `/docs`
2. Set Base URL: `http://localhost:8000`
3. Test all endpoints with provided examples

---

## 🔍 Data Validation

### Student Model Validation

#### Field Requirements
- **name**: 
  - Required
  - Length: 1-100 characters
  - Type: String

- **email**: 
  - Required
  - Must be valid email format
  - Type: EmailStr (validated by email-validator)

- **roll**: 
  - Required
  - Length: 1-50 characters
  - Type: String
  - Must be unique (case-insensitive)

### Error Responses

#### 400 Bad Request - Duplicate Roll
```json
{
  "detail": "Roll number 'CS001' already exists"
}
```

#### 400 Bad Request - Invalid Email
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```

#### 404 Not Found
```json
{
  "detail": "Student with ID '507f1f77bcf86cd799439011' not found"
}
```

---

## 📊 Database Schema

### MongoDB Collection: `students`

```javascript
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  name: "John Doe",
  email: "john.doe@example.com",
  roll: "CS001"
}
```

### Indexes
- Recommended: Create unique index on `roll` field for faster lookups
  ```javascript
  db.students.createIndex({ "roll": 1 }, { unique: true })
  ```

---

## 🔐 CORS Configuration

### What is CORS?
Cross-Origin Resource Sharing (CORS) allows frontend applications on different domains to access the API.

### Current Configuration
- Allowed Origins: localhost:3000, localhost:5173, localhost:8000
- Allowed Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
- Allowed Headers: Content-Type, Authorization, Accept, Origin, etc.
- Credentials: Enabled
- Max Age: 600 seconds

### Adding More Origins
Edit `.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://example.com,http://another-domain.com
```

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```
❌ Failed to connect to MongoDB: connection refused
```

**Solution**:
1. Verify MongoDB is running: `mongod --version`
2. Check MONGODB_URL in `.env`
3. For Atlas: Ensure IP whitelist includes your machine

### Port Already in Use
```
Address already in use
```

**Solution**:
```bash
# Use a different port
uvicorn api:app --port 8001
```

### Import Error
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:
```bash
pip install -r requirements.txt
```

### CORS Error in Frontend
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution**:
1. Check origin URL matches ALLOWED_ORIGINS in `.env`
2. Verify frontend is running on configured port
3. Restart API server after modifying `.env`

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `api.py` | Main FastAPI application with all CRUD endpoints |
| `models.py` | Pydantic models for data validation |
| `requirements.txt` | Python dependencies |
| `.env` | Environment configuration |
| `PHASE_1_SETUP_GUIDE.md` | This file - Setup and usage guide |

---

## ✅ Verification Checklist

Before considering Phase 1 complete, verify:

- [ ] `.env` file exists and is configured
- [ ] MongoDB is running (local or Atlas)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] API server starts without errors: `uvicorn api:app --reload`
- [ ] Health check passes: `curl http://localhost:8000/api/health`
- [ ] Can create student via POST /api/students
- [ ] Can retrieve students via GET /api/students
- [ ] Can update student via PUT /api/students/{id}
- [ ] Can delete student via DELETE /api/students/{id}
- [ ] API docs available at http://localhost:8000/docs
- [ ] CORS works from frontend (3000, 5173, 8000)

---

## 🎯 Next Steps

After Phase 1 is verified working:

1. **Phase 2**: Frontend development with React/Vite
2. **Phase 3**: Student form UI components
3. **Phase 4**: Error handling and advanced features
4. **Phase 5**: Authentication and authorization
5. **Phase 6**: Deployment and production setup

---

## 📝 Notes

- All timestamps are in UTC
- IDs are MongoDB ObjectId (24-character hex strings)
- Email validation uses standard email-validator package
- Logging can be extended for production monitoring
- Database transactions can be added for multi-step operations

---

**Generated**: 2026-02-10  
**Status**: ✅ Phase 1 Complete and Ready for Testing
