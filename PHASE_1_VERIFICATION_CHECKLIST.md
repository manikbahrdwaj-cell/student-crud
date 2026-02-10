# Phase 1: Verification Checklist

Use this checklist to verify Phase 1 implementation is working correctly.

---

## ✅ Pre-Flight Checks

- [ ] MongoDB is running (local or Atlas)
- [ ] Python 3.8+ is installed
- [ ] Project folder is `c:\Users\manik.bhardwaj\.vscode\python`
- [ ] `.env` file exists and is configured
- [ ] Dependencies are installed (`pip install -r requirements.txt`)

---

## ✅ Server Startup

- [ ] Run: `uvicorn app:app --reload`
- [ ] See message: "Uvicorn running on http://0.0.0.0:8000"
- [ ] No errors in startup

---

## ✅ API Documentation

**Access Swagger UI**:
- [ ] Open: http://localhost:8000/docs
- [ ] See list of endpoints
- [ ] All endpoints have descriptions
- [ ] Can expand and test endpoints

**Access ReDoc**:
- [ ] Open: http://localhost:8000/redoc
- [ ] See organized documentation

---

## ✅ Health Check

**Test endpoint**: `GET /`

```bash
curl http://localhost:8000/
```

- [ ] Status: 200
- [ ] Response includes "healthy" status

---

## ✅ Create Student

**Test endpoint**: `POST /api/students`

```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "roll": "CS001"
  }'
```

- [ ] Status: 201 Created
- [ ] Response includes `_id`, `name`, `email`, `roll`
- [ ] Can see student in database

---

## ✅ Get All Students

**Test endpoint**: `GET /api/students`

```bash
curl http://localhost:8000/api/students
```

- [ ] Status: 200
- [ ] Returns array of students
- [ ] Each student has `_id`, `name`, `email`, `roll`

---

## ✅ Get Single Student

**Test endpoint**: `GET /api/students/{id}`

Use the `_id` from create test above

```bash
curl http://localhost:8000/api/students/{id}
```

- [ ] Status: 200
- [ ] Returns single student object
- [ ] Correct student data

---

## ✅ Update Student

**Test endpoint**: `PUT /api/students/{id}`

```bash
curl -X PUT http://localhost:8000/api/students/{id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe"}'
```

- [ ] Status: 200
- [ ] Name is updated
- [ ] Other fields unchanged
- [ ] Embedding is regenerated

---

## ✅ Delete Student

**Test endpoint**: `DELETE /api/students/{id}`

```bash
curl -X DELETE http://localhost:8000/api/students/{id}
```

- [ ] Status: 204 No Content
- [ ] Student no longer in database
- [ ] Verify with GET /api/students

---

## ✅ Error Handling

**Test 1: Duplicate Roll**
```bash
# Create first student
curl -X POST http://localhost:8000/api/students \
  -d '{"name":"A","email":"a@example.com","roll":"UNIQUE001"}'

# Try to create another with same roll
curl -X POST http://localhost:8000/api/students \
  -d '{"name":"B","email":"b@example.com","roll":"UNIQUE001"}'
```
- [ ] Second request returns 409 Conflict
- [ ] Message mentions "already exists"

**Test 2: Invalid Email**
```bash
curl -X POST http://localhost:8000/api/students \
  -d '{"name":"Test","email":"invalid","roll":"CS999"}'
```
- [ ] Status: 422 Unprocessable Entity
- [ ] Message mentions email validation

**Test 3: Missing Fields**
```bash
curl -X POST http://localhost:8000/api/students \
  -d '{"name":"Test"}'
```
- [ ] Status: 422 Unprocessable Entity
- [ ] Message lists missing fields

**Test 4: Invalid ID**
```bash
curl http://localhost:8000/api/students/invalid
```
- [ ] Status: 400 Bad Request
- [ ] Message mentions invalid ID format

**Test 5: Non-existent Student**
```bash
curl http://localhost:8000/api/students/507f1f77bcf86cd799439011
```
- [ ] Status: 404 Not Found
- [ ] Message says student not found

---

## ✅ Run Test Suite

```bash
python test_phase1_api.py
```

- [ ] All tests pass
- [ ] No assertion errors
- [ ] Output shows ✅ ALL TESTS PASSED!

---

## ✅ CORS Configuration

If testing from different origin:
- [ ] CORS headers present in response
- [ ] `Access-Control-Allow-Origin` header visible
- [ ] No CORS errors in browser console

---

## ✅ Environment Variables

Check `.env` file:
- [ ] MONGODB_URL is set
- [ ] DATABASE_NAME is set
- [ ] COLLECTION_NAME is set
- [ ] ALLOWED_ORIGINS includes your frontend URL
- [ ] File is in root project directory

---

## ✅ Documentation

- [ ] `PHASE_1_API_DOCUMENTATION.md` exists and is readable
- [ ] `PHASE_1_QUICK_REFERENCE.md` exists
- [ ] `PHASE_1_IMPLEMENTATION_GUIDE.md` exists
- [ ] All files have proper content

---

## ✅ Code Quality

```bash
# Check for syntax errors
python -m py_compile app.py
python -m py_compile models.py
python -m py_compile test_phase1_api.py
```

- [ ] No syntax errors reported

---

## ✅ Database

- [ ] MongoDB connection successful
- [ ] `student_db` database exists
- [ ] `students` collection created
- [ ] Can see documents in collection

**MongoDB Commands** (in MongoDB shell):
```javascript
use student_db
db.students.find().pretty()
```

- [ ] Can see created students

---

## ✅ Swagger/OpenAPI

In Swagger UI (http://localhost:8000/docs):

- [ ] POST /api/students section expanded
  - [ ] "Try it out" button works
  - [ ] Can test creating student
  
- [ ] GET /api/students section expanded
  - [ ] "Try it out" button works
  - [ ] Can test retrieving students
  
- [ ] GET /api/students/{student_id} section expanded
  - [ ] Parameter field shows `student_id`
  - [ ] "Try it out" works
  
- [ ] PUT /api/students/{student_id} section expanded
  - [ ] Parameter and body fields show
  - [ ] "Try it out" works
  
- [ ] DELETE /api/students/{student_id} section expanded
  - [ ] Parameter field shows
  - [ ] "Try it out" works

---

## ✅ Response Models

In Swagger, check Models section:

- [ ] StudentCreate model visible
  - [ ] Shows required fields: name, email, roll
  - [ ] Shows email validation
  
- [ ] StudentResponse model visible
  - [ ] Shows _id field
  - [ ] Shows all student fields
  
- [ ] StudentUpdate model visible
  - [ ] Shows optional fields

---

## ✅ Backward Compatibility

Test legacy endpoints (optional):

**Old endpoint**: `GET /home`
```bash
curl http://localhost:8000/home
```
- [ ] Returns HTML page (legacy endpoint)

**Old endpoint**: `POST /register`
```bash
curl -X POST http://localhost:8000/register \
  -d "name=Test&email=test@example.com&roll=LEGACY01"
```
- [ ] Works with form data

---

## ✅ Performance

- [ ] First request takes ~1-2 seconds (embedding generation)
- [ ] Subsequent requests are fast (<500ms)
- [ ] No memory leaks after multiple requests
- [ ] Database responses are efficient

---

## 🎉 Final Verification

- [ ] All CRUD operations work
- [ ] All error cases handled
- [ ] Tests pass
- [ ] Documentation complete
- [ ] No syntax errors
- [ ] CORS working
- [ ] Database connected
- [ ] API documented (Swagger/ReDoc)

---

## 📋 Completed Checklist Summary

Count the checkmarks:
- **Pre-Flight**: ___ / 5
- **Server Startup**: ___ / 3
- **API Documentation**: ___ / 3
- **Health Check**: ___ / 2
- **Create Student**: ___ / 3
- **Get All**: ___ / 3
- **Get Single**: ___ / 3
- **Update**: ___ / 4
- **Delete**: ___ / 3
- **Error Handling**: ___ / 12
- **Test Suite**: ___ / 3
- **CORS**: ___ / 3
- **Environment**: ___ / 5
- **Documentation**: ___ / 4
- **Code Quality**: ___ / 3
- **Database**: ___ / 4
- **Swagger**: ___ / 16
- **Response Models**: ___ / 5
- **Backward Compatibility**: ___ / 2
- **Performance**: ___ / 4
- **Final**: ___ / 8

**Total Checks**: 119

👉 **If all boxes checked**: Phase 1 is ✅ COMPLETE and working!

---

## Next Actions

When all checks pass:
1. ✅ Phase 1 verification complete
2. 👉 Proceed to Phase 2: React Project Setup
3. See REACT_MIGRATION_PLAN.md for Phase 2 details

---

## Troubleshooting

If any check fails, see:
- `PHASE_1_IMPLEMENTATION_GUIDE.md` - Troubleshooting section
- `PHASE_1_API_DOCUMENTATION.md` - Technical details
- Code comments in `app.py`

---

**Last Updated**: February 2026
**Phase 1 Status**: ✅ READY FOR VERIFICATION
