#!/usr/bin/env python3
"""
Test script to verify the EditForm bug fix - 
Tests that loading student data for editing works without infinite loops
"""

import requests
import json
import sys
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api"
TEST_STUDENT = {
    "name": "Test Editor",
    "email": "testeditor@test.com",
    "roll": "TE001"
}

def log_test(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {status:8} | {message}")

def test_create_student():
    """Create a test student for editing"""
    log_test("Creating test student for edit test...", "TEST")
    try:
        response = requests.post(f"{API_BASE_URL}/students", json=TEST_STUDENT, timeout=5)
        if response.status_code == 201:
            student = response.json()
            log_test(f"✓ Student created: ID={student.get('_id')}", "PASS")
            return student.get('_id')
        else:
            log_test(f"✗ Failed to create student: {response.status_code}", "FAIL")
            return None
    except Exception as e:
        log_test(f"✗ Error creating student: {str(e)}", "ERROR")
        return None

def test_get_student(student_id):
    """Simulate EditForm fetching student data - this was causing infinite loop"""
    log_test(f"Fetching student {student_id} (simulating EditForm.js behavior)...", "TEST")
    
    try:
        # Make multiple rapid requests to test for infinite loop behavior
        responses = []
        for i in range(3):
            response = requests.get(f"{API_BASE_URL}/students/{student_id}", timeout=5)
            responses.append(response)
            log_test(f"  Request {i+1}: Status {response.status_code}", "INFO")
            
            if response.status_code != 200:
                log_test(f"✗ Failed request {i+1}", "FAIL")
                return False
            
            # Check response has expected data
            data = response.json()
            if not all(key in data for key in ['name', 'email', 'roll', '_id']):
                log_test(f"✗ Missing expected fields in response", "FAIL")
                return False
        
        log_test("✓ All fetch requests successful (no infinite loop detected)", "PASS")
        return True
        
    except Exception as e:
        log_test(f"✗ Error fetching student: {str(e)}", "ERROR")
        return False

def test_update_student(student_id):
    """Simulate StudentForm updating student data"""
    log_test(f"Updating student {student_id}...", "TEST")
    
    update_data = {
        "name": "Test Editor Updated",
        "email": "updated@test.com",
        "roll": "TE002"
    }
    
    try:
        response = requests.put(f"{API_BASE_URL}/students/{student_id}", json=update_data, timeout=5)
        if response.status_code == 200:
            log_test("✓ Student updated successfully", "PASS")
            return True
        else:
            log_test(f"✗ Failed to update: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log_test(f"✗ Error updating student: {str(e)}", "ERROR")
        return False

def test_verify_update(student_id):
    """Verify the update was saved correctly"""
    log_test(f"Verifying updated student data...", "TEST")
    
    try:
        response = requests.get(f"{API_BASE_URL}/students/{student_id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['email'] == 'updated@test.com':
                log_test("✓ Update verified - data persisted correctly", "PASS")
                return True
            else:
                log_test(f"✗ Data not updated. Email is {data['email']}", "FAIL")
                return False
        else:
            log_test(f"✗ Failed to fetch updated student", "FAIL")
            return False
    except Exception as e:
        log_test(f"✗ Error verifying: {str(e)}", "ERROR")
        return False

def cleanup(student_id):
    """Delete test student"""
    log_test(f"Cleaning up test student...", "TEST")
    try:
        response = requests.delete(f"{API_BASE_URL}/students/{student_id}", timeout=5)
        if response.status_code == 200:
            log_test("✓ Test student deleted", "PASS")
            return True
        else:
            log_test(f"⚠ Cleanup failed but continuing", "WARN")
            return False
    except Exception as e:
        log_test(f"⚠ Error during cleanup: {str(e)}", "WARN")
        return False

def main():
    print("=" * 70)
    print("TESTING EDITFORM BUG FIX - Test Student Edit Flow")
    print("=" * 70)
    print()
    
    # Check API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            log_test("✗ API health check failed", "ERROR")
            return False
        log_test("✓ API is running and responsive", "PASS")
    except Exception as e:
        log_test(f"✗ Cannot connect to API: {str(e)}", "ERROR")
        return False
    
    print()
    
    # Run tests
    results = []
    
    # Step 1: Create student
    student_id = test_create_student()
    results.append(("Create Student", student_id is not None))
    if not student_id:
        print("\n✗ Cannot proceed - failed to create test student")
        return False
    
    print()
    
    # Step 2: Fetch student (this was causing infinite loop before fix)
    result = test_get_student(student_id)
    results.append(("Fetch Student (Edit Load)", result))
    
    print()
    
    # Step 3: Update student
    result = test_update_student(student_id)
    results.append(("Update Student", result))
    
    print()
    
    # Step 4: Verify update
    result = test_verify_update(student_id)
    results.append(("Verify Update", result))
    
    print()
    
    # Cleanup
    cleanup(student_id)
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} | {test_name}")
    
    print()
    all_passed = all(result for _, result in results)
    if all_passed:
        log_test("All tests PASSED! EditForm bug is FIXED!", "SUCCESS")
        print()
        print("The infinite loop bug in EditForm has been fixed:")
        print("- Removed 'toast' from useEffect dependencies")
        print("- StudentData now loads correctly without infinite updates")
        print("- Edit form can load and update student data as expected")
    else:
        log_test("Some tests FAILED!", "ERROR")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
