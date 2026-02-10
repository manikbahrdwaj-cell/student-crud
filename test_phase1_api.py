"""
Phase 1 API Testing - Student CRUD Operations
Test file to validate all REST API endpoints for Student CRUD operations
"""

import requests
import json
from pprint import pprint

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test data
test_student_1 = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "roll": "CS001"
}

test_student_2 = {
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "roll": "CS002"
}

test_student_update = {
    "name": "John Updated",
    "email": "john.updated@example.com"
}

def print_response(title, response):
    """Helper function to print API responses"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:")
        pprint(response.json())
    except:
        print(f"Response: {response.text}")
    print()


def test_health_check():
    """Test 1: Health Check"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Health Check", response)
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_student():
    """Test 2: Create a new student"""
    response = requests.post(
        f"{BASE_URL}/api/students",
        json=test_student_1
    )
    print_response("Create Student", response)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_student_1["name"]
    assert data["email"] == test_student_1["email"]
    assert data["roll"] == test_student_1["roll"]
    assert "_id" in data
    return data["_id"]


def test_create_duplicate_roll():
    """Test 3: Try to create student with duplicate roll number"""
    # First create a student
    requests.post(f"{BASE_URL}/api/students", json=test_student_1)
    
    # Try to create another with same roll
    response = requests.post(
        f"{BASE_URL}/api/students",
        json=test_student_1
    )
    print_response("Create Student with Duplicate Roll", response)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_get_all_students():
    """Test 4: Get all students"""
    # Clear and create some test data
    response = requests.get(f"{BASE_URL}/api/students")
    print_response("Get All Students", response)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_student(student_id):
    """Test 5: Get a single student"""
    response = requests.get(f"{BASE_URL}/api/students/{student_id}")
    print_response("Get Single Student", response)
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == student_id


def test_get_invalid_student_id():
    """Test 6: Try to get student with invalid ID"""
    response = requests.get(f"{BASE_URL}/api/students/invalid_id")
    print_response("Get Student with Invalid ID", response)
    assert response.status_code == 400
    assert "Invalid" in response.json()["detail"]


def test_get_nonexistent_student():
    """Test 7: Try to get non-existent student"""
    # Use a valid ObjectId that doesn't exist
    fake_id = "507f1f77bcf86cd799439011"
    response = requests.get(f"{BASE_URL}/api/students/{fake_id}")
    print_response("Get Non-existent Student", response)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_student(student_id):
    """Test 8: Update a student"""
    response = requests.put(
        f"{BASE_URL}/api/students/{student_id}",
        json=test_student_update
    )
    print_response("Update Student", response)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_student_update["name"]
    assert data["email"] == test_student_update["email"]


def test_update_with_duplicate_roll(student_id):
    """Test 9: Try to update with duplicate roll"""
    # Create another student first
    requests.post(f"{BASE_URL}/api/students", json=test_student_2)
    
    # Try to update first student with second student's roll
    update_data = {"roll": test_student_2["roll"]}
    response = requests.put(
        f"{BASE_URL}/api/students/{student_id}",
        json=update_data
    )
    print_response("Update Student with Duplicate Roll", response)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_delete_student(student_id):
    """Test 10: Delete a student"""
    response = requests.delete(f"{BASE_URL}/api/students/{student_id}")
    print_response("Delete Student", response)
    assert response.status_code == 204


def test_delete_nonexistent_student():
    """Test 11: Try to delete non-existent student"""
    fake_id = "507f1f77bcf86cd799439011"
    response = requests.delete(f"{BASE_URL}/api/students/{fake_id}")
    print_response("Delete Non-existent Student", response)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_validation_errors():
    """Test 12: Test input validation"""
    # Missing required field
    invalid_student = {
        "name": "Test Student"
        # Missing email and roll
    }
    response = requests.post(
        f"{BASE_URL}/api/students",
        json=invalid_student
    )
    print_response("Create Student with Missing Fields", response)
    assert response.status_code == 422


def test_invalid_email():
    """Test 13: Test invalid email validation"""
    invalid_student = {
        "name": "Test Student",
        "email": "invalid-email",
        "roll": "CS999"
    }
    response = requests.post(
        f"{BASE_URL}/api/students",
        json=invalid_student
    )
    print_response("Create Student with Invalid Email", response)
    assert response.status_code == 422


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("PHASE 1: STUDENT CRUD API TESTING")
    print("="*60)
    
    try:
        # Basic tests
        test_health_check()
        
        # Create tests
        student_id = test_create_student()
        test_create_duplicate_roll()
        
        # Read tests
        test_get_all_students()
        test_get_single_student(student_id)
        test_get_invalid_student_id()
        test_get_nonexistent_student()
        
        # Update tests
        test_update_student(student_id)
        test_update_with_duplicate_roll(student_id)
        
        # Delete tests
        test_delete_student(student_id)
        test_delete_nonexistent_student()
        
        # Validation tests
        test_validation_errors()
        test_invalid_email()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: Cannot connect to API at {BASE_URL}")
        print("Make sure the FastAPI server is running:")
        print("  uvicorn app:app --reload")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
