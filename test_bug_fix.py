"""
Test to verify the case-insensitive duplicate roll bug fix
"""

import requests
import json
import random
import string
import time

API_URL = "http://localhost:8000"
API_STUDENTS_URL = f"{API_URL}/api/students"

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_test(message):
    print(f"\n{YELLOW}▶ {message}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def generate_roll():
    return "BUG" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def create_student(name, email, roll):
    """Create a student"""
    response = requests.post(
        API_STUDENTS_URL,
        json={"name": name, "email": email, "roll": roll},
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 201:
        return response.json().get("_id") or response.json().get("id")
    return None

def test_case_sensitive_duplicate_fix():
    """Test that the case-insensitive duplicate bug is fixed"""
    
    print("\n" + "="*70)
    print("TESTING: Case-Insensitive Duplicate Roll Number Bug Fix")
    print("="*70)
    
    # Wait for API
    time.sleep(1)
    
    # Test 1: Create first student with exact roll
    print_test("TEST 1: Create first student with roll 'BugTestXYZ123'")
    original_roll = "BugTestXYZ123"
    student_id_1 = create_student("Bug Test Student 1", "bugtest1@example.com", original_roll)
    
    if student_id_1:
        print_success(f"Created student 1 with ID: {student_id_1}")
    else:
        print_error("Failed to create first student")
        return
    
    # Test 2: Create second student
    print_test("TEST 2: Create second student with different roll")
    student_id_2 = create_student("Bug Test Student 2", "bugtest2@example.com", generate_roll())
    
    if student_id_2:
        print_success(f"Created student 2 with ID: {student_id_2}")
    else:
        print_error("Failed to create second student")
        return
    
    # Test 3: Try to update second student with lowercase version of first student's roll
    print_test("TEST 3: Try to update student 2 with LOWERCASE version of student 1's roll")
    lowercase_roll = original_roll.lower()
    print(f"Original roll: {original_roll}")
    print(f"Lowercase roll: {lowercase_roll}")
    
    response = requests.put(
        f"{API_STUDENTS_URL}/{student_id_2}",
        json={"roll": lowercase_roll},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 400:
        error_detail = response.json().get("detail", "")
        print_success("✓ CORRECTLY REJECTED with 400 Bad Request")
        print_success(f"✓ Error message: {error_detail}")
        print_success("✓ BUG FIX VERIFIED: Case-insensitive duplicate detection is working!")
        return True
    elif response.status_code == 200:
        print_error("✗ INCORRECTLY ALLOWED the duplicate (BUG NOT FIXED)")
        print_error(f"✗ Response: {json.dumps(response.json(), indent=2)}")
        return False
    else:
        print_error(f"Unexpected status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

    # Test 4: Try with UPPERCASE version
    print_test("TEST 4: Try to update student 2 with UPPERCASE version of student 1's roll")
    uppercase_roll = original_roll.upper()
    print(f"Original roll: {original_roll}")
    print(f"Uppercase roll: {uppercase_roll}")
    
    response = requests.put(
        f"{API_STUDENTS_URL}/{student_id_2}",
        json={"roll": uppercase_roll},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 400:
        error_detail = response.json().get("detail", "")
        print_success("✓ CORRECTLY REJECTED with 400 Bad Request")
        print_success(f"✓ Error message: {error_detail}")
        return True
    elif response.status_code == 200:
        print_error("✗ INCORRECTLY ALLOWED the duplicate (BUG NOT FIXED)")
        print_error(f"✗ Response: {json.dumps(response.json(), indent=2)}")
        return False
    else:
        print_error(f"Unexpected status code: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_case_sensitive_duplicate_fix()
    
    print("\n" + "="*70)
    if success:
        print_success("✓ BUG FIX VERIFICATION: PASSED")
    else:
        print_error("✗ BUG FIX VERIFICATION: FAILED")
    print("="*70 + "\n")
