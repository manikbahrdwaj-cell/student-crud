"""
Test script for GET /api/students/{id} and PUT /api/students/{id} endpoints
"""

import requests
import json
import time
import subprocess
import sys
import os
import random
import string

# API Configuration
API_URL = "http://localhost:8000"
API_HEALTH_URL = f"{API_URL}/api/health"
API_STUDENTS_URL = f"{API_URL}/api/students"

def generate_unique_roll():
    """Generate a unique roll number"""
    return "TEST" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_test(message):
    """Print test message"""
    print(f"\n{YELLOW}▶ {message}{RESET}")

def print_success(message):
    """Print success message"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    """Print error message"""
    print(f"{RED}✗ {message}{RESET}")

def wait_for_api(timeout=10):
    """Wait for API to be ready"""
    print("\n⏳ Waiting for API to be ready...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(API_HEALTH_URL, timeout=2)
            if response.status_code == 200:
                print_success("API is ready!")
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    
    print_error(f"API did not start within {timeout} seconds")
    return False

def test_get_student_by_id(student_id):
    """Test GET /api/students/{id}"""
    print_test(f"Testing GET /api/students/{student_id}")
    
    try:
        response = requests.get(f"{API_STUDENTS_URL}/{student_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Check if _id or id field exists
            if "_id" in data or "id" in data:
                print_success("✓ ID field present in response")
                return data
            else:
                print_error("✗ Missing ID field in response")
                return None
        elif response.status_code == 404:
            print_error(f"Student not found: {response.json()}")
            return None
        elif response.status_code == 400:
            print_error(f"Invalid ID format: {response.json()}")
            return None
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return None

def test_put_student(student_id, update_data):
    """Test PUT /api/students/{id}"""
    print_test(f"Testing PUT /api/students/{student_id}")
    print(f"Update data: {json.dumps(update_data, indent=2)}")
    
    try:
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Verify the update
            for key, value in update_data.items():
                if key in data and data[key] == value:
                    print_success(f"✓ {key} updated correctly: {value}")
                else:
                    print_error(f"✗ {key} not updated correctly")
            
            return data
        elif response.status_code == 404:
            print_error(f"Student not found: {response.json()}")
            return None
        elif response.status_code == 400:
            print_error(f"Validation error: {response.json()}")
            return None
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return None

def test_create_student(name, email, roll):
    """Create a test student"""
    print_test(f"Creating test student: {name}")
    
    try:
        response = requests.post(
            API_STUDENTS_URL,
            json={"name": name, "email": email, "roll": roll},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            student_id = data.get("_id") or data.get("id")
            print_success(f"Student created with ID: {student_id}")
            return student_id
        else:
            print_error(f"Failed to create student: {response.json()}")
            return None
    
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return None

def main():
    """Main test execution"""
    print("\n" + "="*60)
    print("TESTING GET /api/students/{id} AND PUT /api/students/{id}")
    print("="*60)
    
    # Wait for API to be ready
    if not wait_for_api():
        print_error("Cannot proceed - API is not running")
        return
    
    print("\n" + "="*60)
    print("TEST 1: Create a student for testing")
    print("="*60)
    
    student_id = test_create_student("Test Student", "test@example.com", generate_unique_roll())
    
    if not student_id:
        print_error("Cannot proceed - failed to create test student")
        return
    
    print("\n" + "="*60)
    print("TEST 2: Get student by ID")
    print("="*60)
    
    student = test_get_student_by_id(student_id)
    
    if not student:
        print_error("Cannot proceed - failed to get student")
        return
    
    print("\n" + "="*60)
    print("TEST 3: Update student with PUT")
    print("="*60)
    
    update_data = {
        "name": "Updated Student Name",
        "email": "updated@example.com"
    }
    
    test_put_student(student_id, update_data)
    
    print("\n" + "="*60)
    print("TEST 4: Verify update with GET")
    print("="*60)
    
    updated_student = test_get_student_by_id(student_id)
    
    print("\n" + "="*60)
    print("TEST 5: Test invalid student ID")
    print("="*60)
    
    test_get_student_by_id("invalid_id_format")
    
    print("\n" + "="*60)
    print("TEST 6: Test non-existent student ID")
    print("="*60)
    
    test_get_student_by_id("507f1f77bcf86cd799439999")
    
    print("\n" + "="*60)
    print("TEST 7: Test duplicate roll number on update")
    print("="*60)
    
    # Create another student
    student_id_2 = test_create_student("Another Student", "another@example.com", generate_unique_roll())
    
    if student_id_2:
        # Try to update first student with duplicate roll
        print_test(f"Trying to update {student_id} with existing roll TEST002")
        test_put_student(student_id, {"roll": "TEST002"})
    
    print("\n" + "="*60)
    print("TEST 8: Test partial update (only name)")
    print("="*60)
    
    test_put_student(student_id, {"name": "Partially Updated Name"})
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
