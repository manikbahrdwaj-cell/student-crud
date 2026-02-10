# CORS Quick Reference Guide

## For Frontend Developers

### React/Vue Axios Configuration
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true // Include cookies if needed
});

// Now use api.get(), api.post(), etc.
api.get('/students')
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

### React Fetch Configuration
```javascript
const API_URL = 'http://localhost:8000/api';

// GET request
fetch(`${API_URL}/students`, {
  method: 'GET',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include'
})
.then(r => r.json())
.then(data => console.log(data));

// POST request
fetch(`${API_URL}/students`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    roll: 'STU001'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

## For Backend Developers

### Start Development Servers

**Terminal 1 - FastAPI Backend:**
```bash
cd /path/to/project
python api.py
# or
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - React Frontend (if using React):**
```bash
cd student-registration
npm start
# Runs on http://localhost:3000
```

**Terminal 3 - MongoDB:**
```bash
mongod --dbpath /path/to/mongo/data
```

### Check CORS Status
```bash
# Check if CORS headers are present
curl -i -H "Origin: http://localhost:3000" http://localhost:8000/api/students
```

### Common Development Origins

| Framework | Port | URL |
|-----------|------|-----|
| React (create-react-app) | 3000 | http://localhost:3000 |
| Vite (React/Vue) | 5173 | http://localhost:5173 |
| Next.js | 3000 | http://localhost:3000 |
| FastAPI Docs | 8000 | http://localhost:8000 |
| Flask/FastAPI | 5000 | http://localhost:5000 |

### Adding a New Origin

1. Open `.env` file
2. Update `ALLOWED_ORIGINS`:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://your-new-origin:port
   ```
3. Restart the API

## Troubleshooting

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Cause:** Origin not in `ALLOWED_ORIGINS`

**Fix:**
1. Check your frontend URL (port, protocol, domain)
2. Add it to `.env` ALLOWED_ORIGINS
3. Restart API
4. Restart frontend dev server
5. Clear browser cache (Ctrl+Shift+Delete)

### Error: "CORS policy: Response to preflight request doesn't pass"

**Cause:** Missing headers in CORS config

**Fix:**
- Ensure `Content-Type` is in `allow_headers`
- Verify `OPTIONS` method is in `allow_methods`
- Check the exact header names in the preflight request

### Credentials Not Sent with Requests

**Issue:** Authentication headers/cookies not being sent

**Fix:**
- Frontend: Use `credentials: 'include'` in fetch or `withCredentials: true` in axios
- Backend: Ensure `allow_credentials=True` in CORS config
- Already configured: ✅

## API Response Examples

### GET /api/students
```bash
curl -H "Origin: http://localhost:3000" \
  http://localhost:8000/api/students

Response:
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "roll": "STU001"
  }
]
```

### POST /api/students
```bash
curl -X POST \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/students \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "roll": "STU002"
  }'

Response:
{
  "_id": "507f1f77bcf86cd799439012",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "roll": "STU002"
}
```

## Environment Configuration Summary

| Setting | Development | Production |
|---------|-------------|-----------|
| ALLOWED_ORIGINS | localhost:3000, localhost:5173 | yourdomain.com |
| allow_credentials | True | True |
| allow_methods | GET, POST, PUT, DELETE, OPTIONS, PATCH | Same or minimal |
| DEBUG | True | False |
| API_HOST | 0.0.0.0 | Your server IP |
| API_PORT | 8000 | 8000 or 80/443 |

## Files Reference

- **Main API:** [api.py](api.py)
- **Template API:** [app.py](app.py)
- **Configuration:** [.env](.env)
- **Full Docs:** [CORS_CONFIGURATION.md](CORS_CONFIGURATION.md)
- **Implementation Status:** [CORS_IMPLEMENTATION_STATUS.md](CORS_IMPLEMENTATION_STATUS.md)

## API Documentation

Access FastAPI Swagger UI:
```
http://localhost:8000/docs
```

Access ReDoc (alternative documentation):
```
http://localhost:8000/redoc
```

## Health Check
```bash
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/health

Response:
{
  "status": "✅ API is running",
  "database": "Connected to MongoDB"
}
```

---

**Last Updated:** February 9, 2026  
**Status:** Production Ready ✅
