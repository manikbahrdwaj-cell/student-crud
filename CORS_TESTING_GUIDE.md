# CORS Configuration Testing Guide - Phase 1

## Overview
This guide helps you verify that CORS is properly configured and working with your Student Management API.

---

## 1. Prerequisites

### Required Services Running
Before testing CORS, ensure these services are running:

1. **MongoDB Server**
   ```bash
   mongod --dbpath /path/to/mongo/data
   ```

2. **FastAPI Backend (Terminal 1)**
   ```bash
   cd c:\Users\manik.bhardwaj\.vscode\python
   python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Optional: Frontend Development Server (Terminal 2)**
   ```bash
   npm start  # or yarn start
   # Runs on http://localhost:3000 or http://localhost:5173
   ```

---

## 2. CORS Configuration Current Status

### ✅ Configured CORS Settings

**File: `.env`**
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:8000
```

**File: `api.py`**
```python
cors_config = {
    "allow_origins": ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    "allow_headers": [
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ],
    "expose_headers": ["Content-Type", "X-Total-Count"],
    "max_age": 600  # 10 minutes
}
app.add_middleware(CORSMiddleware, **cors_config)
```

**File: `app.py`**
```python
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

---

## 3. Testing CORS Using cURL

### Test 1: Health Check with CORS Headers
```bash
curl -i -H "Origin: http://localhost:3000" \
  http://localhost:8000/api/health
```

**Expected Response Headers:**
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
```

### Test 2: Preflight Request (OPTIONS)
```bash
curl -i -X OPTIONS \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  http://localhost:8000/api/students
```

**Expected Response Headers:**
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
Access-Control-Allow-Headers: Content-Type, Authorization, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers
Access-Control-Max-Age: 600
Access-Control-Allow-Credentials: true
```

### Test 3: GET Request with CORS
```bash
curl -i -H "Origin: http://localhost:3000" \
  http://localhost:8000/api/students
```

### Test 4: POST Request with CORS
```bash
curl -i -X POST \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Student", "email": "test@example.com", "roll": "TEST001"}' \
  http://localhost:8000/api/students
```

### Test 5: Test from Non-Allowed Origin (should fail)
```bash
curl -i -H "Origin: http://unauthorized-site.com" \
  http://localhost:8000/api/students
```

**Expected Response:**
- No `Access-Control-Allow-Origin` header (request blocked)

---

## 4. Testing CORS Using JavaScript/Fetch

### Test 1: Simple GET Request
```javascript
const API_URL = 'http://localhost:8000/api';

fetch(`${API_URL}/students`, {
  method: 'GET',
  headers: { 
    'Content-Type': 'application/json'
  },
  credentials: 'include'
})
.then(response => {
  console.log('Response Status:', response.status);
  console.log('CORS Headers:', {
    'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
    'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
  });
  return response.json();
})
.then(data => console.log('Data:', data))
.catch(error => console.error('Error:', error));
```

### Test 2: POST Request with CORS
```javascript
const API_URL = 'http://localhost:8000/api';

fetch(`${API_URL}/students`, {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json'
  },
  credentials: 'include',
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    roll: 'STU001'
  })
})
.then(response => response.json())
.then(data => console.log('Created:', data))
.catch(error => console.error('CORS Error:', error));
```

### Test 3: Axios Configuration (React)
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true  // Important for CORS with credentials
});

// GET request
api.get('/students')
  .then(response => console.log('Students:', response.data))
  .catch(error => console.error('CORS Error:', error.message));

// POST request
api.post('/students', {
  name: 'John Doe',
  email: 'john@example.com',
  roll: 'STU001'
})
.then(response => console.log('Created:', response.data))
.catch(error => console.error('Error:', error.message));
```

---

## 5. Testing CORS Using Python Requests

```python
import requests
import json

API_URL = 'http://localhost:8000/api'

# Test 1: GET request
headers = {
    'Origin': 'http://localhost:3000',
    'Content-Type': 'application/json'
}

response = requests.get(f'{API_URL}/students', headers=headers)
print(f"Status: {response.status_code}")
print(f"CORS Headers: {response.headers.get('Access-Control-Allow-Origin')}")
print(f"Data: {response.json()}")

# Test 2: POST request
student_data = {
    'name': 'Jane Smith',
    'email': 'jane@example.com',
    'roll': 'STU002'
}

response = requests.post(
    f'{API_URL}/students',
    headers=headers,
    json=student_data
)
print(f"\nCreated Student:")
print(f"Status: {response.status_code}")
print(f"Data: {response.json()}")
```

---

## 6. Troubleshooting CORS Issues

### Issue 1: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Cause:** Frontend origin not in `ALLOWED_ORIGINS`

**Solution:**
1. Verify your frontend URL:
   - React (create-react-app): http://localhost:3000
   - Vite: http://localhost:5173
   - Custom: http://your-domain:port

2. Update `.env` file:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://your-domain:port
   ```

3. Restart the FastAPI server:
   ```bash
   # Press Ctrl+C to stop
   # Then run again
   python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

### Issue 2: "CORS policy: Response to preflight request doesn't pass validation"

**Cause:** Missing headers in CORS config

**Solution:**
- Check that required headers are in `allow_headers`
- Verify `Content-Type` is included
- Check that `OPTIONS` method is in `allow_methods`

### Issue 3: Credentials Not Sent

**Cause:** Missing `withCredentials` or `credentials: 'include'`

**Solution - Fetch:**
```javascript
fetch(url, {
  credentials: 'include'  // Add this
})
```

**Solution - Axios:**
```javascript
axios.create({
  withCredentials: true  // Add this
})
```

### Issue 4: Backend Logging Shows Wrong Origins

**Solution:**
1. Check `.env` file for typos
2. Ensure `.env` is in the same directory as `api.py`
3. Restart the API server
4. Check the console output for:
   ```
   ✅ CORS configured for origins: [...]
   ```

---

## 7. Browser Developer Tools Testing

### Chrome/Edge Developer Tools

1. **Open DevTools** (F12)
2. **Go to Network Tab**
3. **Make a request from your frontend**
4. **Click the request** (e.g., POST /api/students)
5. **Check Response Headers** for:
   - `access-control-allow-origin`
   - `access-control-allow-credentials`
   - `access-control-allow-methods`
   - `access-control-allow-headers`

### Check for Preflight Request

1. In Network tab, look for `OPTIONS` request to same endpoint
2. Response should include CORS headers above
3. If preflight fails, subsequent request won't be sent

---

## 8. CORS Configuration Checklist

- [x] FastAPI installed and `CORSMiddleware` imported
- [x] CORS middleware added to `api.py`
- [x] CORS middleware added to `app.py`
- [x] `.env` file created with `ALLOWED_ORIGINS`
- [x] `python-dotenv` in requirements.txt
- [x] All required HTTP methods listed: GET, POST, PUT, DELETE, OPTIONS, PATCH
- [x] Required headers included: Content-Type, Authorization, Accept, Origin, etc.
- [x] `allow_credentials=True` set
- [x] `max_age` configured (preflight cache)
- [x] MongoDB connection working
- [x] API server can start without errors

---

## 9. Useful Commands

### Start API Server
```bash
cd c:\Users\manik.bhardwaj\.vscode\python
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Check if Port 8000 is in Use
```powershell
netstat -ano | findstr :8000
```

### Kill Process on Port 8000
```powershell
taskkill /PID <PID> /F
```

### Test Connectivity to MongoDB
```bash
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); client.admin.command('ping'); print('MongoDB Connected!')"
```

### View API Documentation
- Go to: http://localhost:8000/docs (Swagger UI)
- Go to: http://localhost:8000/redoc (ReDoc)

---

## 10. Next Steps

After verifying CORS is working:

1. ✅ **Test all CRUD endpoints** (GET, POST, PUT, DELETE)
2. ✅ **Test from frontend application** (React/Vue)
3. ✅ **Test authentication headers** (if applicable)
4. ✅ **Test error handling** (4xx, 5xx responses)
5. ✅ **Deploy to production** (update ALLOWED_ORIGINS for production domain)

---

## Additional Resources

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN: CORS Explained](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [cURL Documentation](https://curl.se/docs/)

---

**Last Updated:** February 10, 2026
**Status:** ✅ CORS Configuration Complete
