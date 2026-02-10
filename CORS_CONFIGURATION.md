# CORS Configuration - Phase 1: Backend API Development

## Overview
CORS (Cross-Origin Resource Sharing) enables secure communication between your backend API and frontend applications running on different domains/ports.

## Current Implementation

### 1. **FastAPI CORS Middleware**

#### In `api.py` (Main REST API)
```python
ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")]

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

#### In `app.py` (Template/Form API)
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

### 2. **Environment Configuration (.env)**

```env
# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:8000

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=student_db
COLLECTION_NAME=students

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## CORS Configuration Parameters Explained

| Parameter | Value | Explanation |
|-----------|-------|-------------|
| `allow_origins` | List of URLs | Specifies which frontend origins can access the API |
| `allow_credentials` | `True` | Allows cookies and authentication headers |
| `allow_methods` | GET, POST, PUT, DELETE, OPTIONS, PATCH | HTTP methods allowed from frontend |
| `allow_headers` | Content-Type, Authorization, etc. | Request headers allowed from frontend |
| `expose_headers` | Content-Type, X-Total-Count | Response headers exposed to frontend |
| `max_age` | 600 (seconds) | Browser preflight cache duration |

## Allowed Origins

Currently configured for development and testing:

- **React (Port 3000)**: `http://localhost:3000`
- **Vite (Port 5173)**: `http://localhost:5173` (Modern React/Vue dev server)
- **FastAPI (Port 8000)**: `http://localhost:8000`
- **Localhost**: `http://127.0.0.1:3000/5173/8000`

### Adding New Origins

To add more allowed origins, update `.env`:

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://your-domain.com,https://your-domain.com
```

## How CORS Works

### 1. **Preflight Request (OPTIONS)**
Before sending actual requests (POST, PUT, DELETE), browsers send an OPTIONS request to check if the API allows the request.

Example:
```
OPTIONS /api/students HTTP/1.1
Host: localhost:8000
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
```

### 2. **API Response**
If the origin is allowed, the API responds with:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: content-type
Access-Control-Max-Age: 600
```

### 3. **Actual Request**
If preflight passes, the browser sends the actual request.

## Testing CORS Configuration

### Using cURL

```bash
# Test simple GET request
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/students

# Test preflight OPTIONS request
curl -X OPTIONS \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  http://localhost:8000/api/students
```

### Using Python requests

```python
import requests

# Test with CORS headers
headers = {"Origin": "http://localhost:3000"}
response = requests.get("http://localhost:8000/api/students", headers=headers)
print(response.headers.get("Access-Control-Allow-Origin"))
```

### Using JavaScript/Frontend

```javascript
// Fetch API automatically handles CORS
fetch('http://localhost:8000/api/students', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include'  // Include cookies if needed
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## Production Configuration

For production deployment, update `.env` with your domain:

```env
# Production CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com

# Security
DEBUG=False
API_HOST=0.0.0.0  # Or your server IP
API_PORT=8000
```

## Security Best Practices

1. **Restrict Origins**: Don't use `"*"` in production - specify exact domains
2. **Use HTTPS**: In production, only allow HTTPS origins
3. **Credentials**: Only set `allow_credentials=True` if actually needed
4. **Headers**: Specify only necessary headers instead of allowing all
5. **Methods**: Allow only required HTTP methods
6. **Max Age**: Keep preflight cache duration reasonable (600s = 10 min)

## Common Issues & Solutions

### Issue: CORS Error in Browser Console
```
Access to XMLHttpRequest at 'http://localhost:8000/api/students' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution**: 
- Ensure your frontend origin is in `ALLOWED_ORIGINS` in `.env`
- Verify the API is running with proper CORS middleware
- Check browser console for exact error message

### Issue: Preflight Request Fails
**Solution**: 
- Ensure `OPTIONS` method is in `allow_methods`
- Verify all required headers are in `allow_headers`
- Check API is properly configured with CORSMiddleware

### Issue: Credentials Not Sent
**Solution**: 
- Set `allow_credentials=True` in CORS config
- In frontend, use `credentials: 'include'` in fetch/axios requests

## Environment Variables Reference

```env
# Frontend Development Origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Or for specific domain
ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com

# Separate origins with commas (no spaces between values)
```

## API Health Check with CORS

Access the health check endpoint to verify CORS is working:

```bash
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/health
```

Response should include:
```
Access-Control-Allow-Origin: http://localhost:3000
```

## Related Files

- **Main API**: [api.py](api.py#L44-L60)
- **Template API**: [app.py](app.py#L1-L25)
- **Environment Config**: [.env](.env)
- **Requirements**: [requirements.txt](requirements.txt)

## References

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
