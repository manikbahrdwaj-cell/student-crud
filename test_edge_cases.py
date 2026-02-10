"""
Advanced test script for edge cases and potential bugs
"""

import requests
import json
import random
import string

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
    return "ADV" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

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

def test_edge_cases():
    """Test edge cases and potential bugs"""
    print("\n" + "="*60)
    print("ADVANCED EDGE CASE TESTING")
    print("="*60)
    
    # Test 1: Empty PUT body update
    print_test("TEST 1: PUT with empty/no changes")
    student_id = create_student("Edge Test 1", "edge1@test.com", generate_roll())
    if student_id:
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id}",
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            student = response.json()
            print_success("Empty update handled gracefully")
            print(f"Student returned: {json.dumps(student, indent=2)}")
        else:
            print_error(f"Unexpected status: {response.text}")
    
    # Test 2: PUT with null values
    print_test("TEST 2: PUT with null/None values")
    student_id = create_student("Edge Test 2", "edge2@test.com", generate_roll())
    if student_id:
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id}",
            json={"name": None, "email": None},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print_success("Null values handled correctly")
        else:
            print_error(f"Response: {response.text}")
    
    # Test 3: Invalid email format on update
    print_test("TEST 3: PUT with invalid email format")
    student_id = create_student("Edge Test 3", "edge3@test.com", generate_roll())
    if student_id:
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id}",
            json={"email": "not-an-email"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print_success("Invalid email rejected with 422 Unprocessable Entity")
        else:
            print_error(f"Expected 422 but got {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Empty string values
    print_test("TEST 4: PUT with empty string values")
    student_id = create_student("Edge Test 4", "edge4@test.com", generate_roll())
    if student_id:
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id}",
            json={"name": "", "roll": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print_success("Empty strings rejected with 422")
        else:
            print_error(f"Expected 422 but got {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 5: Very long name/roll
    print_test("TEST 5: PUT with very long strings")
    student_id = create_student("Edge Test 5", "edge5@test.com", generate_roll())
    if student_id:
        long_name = "A" * 200  # Exceeds max_length of 100
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id}",
            json={"name": long_name},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print_success("Oversized strings rejected with 422")
        else:
            print_error(f"Expected 422 but got {response.status_code}")
            print(f"Response: {response.text}")
    
    # Test 6: Case sensitivity in roll number
    print_test("TEST 6: PUT with case variation in roll number")
    roll = generate_roll()
    student_id = create_student("Edge Test 6a", "edge6a@test.com", roll)
    student_id_2 = create_student("Edge Test 6b", "edge6b@test.com", generate_roll())
    
    if student_id and student_id_2:
        # Try to update second student with different case of first student's roll
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id_2}",
            json={"roll": roll.lower()},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print_success("Case-sensitive duplicate detection working (different case rejected)")
        elif response.status_code == 200:
            print_error("Case-insensitive duplicate detection - possible bug!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 7: GET with URL encoded ID
    print_test("TEST 7: GET with special characters in ID (if valid)")
    student_id = create_student("Edge Test 7", "edge7@test.com", generate_roll())
    if student_id:
        # Normal request (should work)
        response1 = requests.get(f"{API_STUDENTS_URL}/{student_id}")
        print(f"Normal GET Status: {response1.status_code}")
        if response1.status_code == 200:
            print_success("Normal GET works")
    
    # Test 8: Whitespace in names/roll
    print_test("TEST 8: PUT with leading/trailing whitespace")
    student_id = create_student("Edge Test 8", "edge8@test.com", generate_roll())
    if student_id:
        response = requests.put(
            f"{API_STUDENTS_URL}/{student_id}",
            json={"name": "  Name with spaces  ", "roll": "  ROLL  "},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            student = response.json()
            name = student.get("name", "")
            roll = student.get("roll", "")
            print(f"Stored name: '{name}'")
            print(f"Stored roll: '{roll}'")
            if name == "  Name with spaces  ":
                print_success("Whitespace preserved as-is")
            else:
                print_error("Whitespace was modified")
    
    # Test 9: Special characters in email
    print_test("TEST 9: PUT with special characters in email")
    student_id = create_student("Edge Test 9", "edge9@test.com", generate_roll())
    if student_id:
        special_emails = [
            "test+tag@example.com",  # Valid
            "test.name@example.com",  # Valid
            "test@sub.example.com",   # Valid
        ]
        for email in special_emails:
            response = requests.put(
                f"{API_STUDENTS_URL}/{student_id}",
                json={"email": email},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print_success(f"Email '{email}' accepted")
            else:
                print_error(f"Email '{email}' rejected: {response.status_code}")
    
    # Test 10: GET with modified ID (case sensitivity)
    print_test("TEST 10: GET with different case ObjectId (case-sensitivity test)")
    student_id = create_student("Edge Test 10", "edge10@test.com", generate_roll())
    if student_id and len(student_id) > 0:
        # ObjectId is case-insensitive in MongoDB
        response = requests.get(f"{API_STUDENTS_URL}/{student_id.upper()}")
        print(f"Original ID: {student_id}")
        print(f"Uppercase ID Status: {response.status_code}")
        if response.status_code == 200:
            print_success("ObjectId case handling works correctly")
        elif response.status_code == 400:
            print_error("ObjectId case-sensitivity issue detected")
    
    print("\n" + "="*60)
    print("EDGE CASE TESTING COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_edge_cases()
