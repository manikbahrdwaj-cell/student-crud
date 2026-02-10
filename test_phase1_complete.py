"""
Phase 1 API Testing Script
Tests all CRUD endpoints and validates responses
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

class APITester:
    def __init__(self):
        self.test_results = []
        self.created_student_id = None
        self.session = requests.Session()
    
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"\n{status}: {test_name}")
        if message:
            print(f"   {message}")
        self.test_results.append({"test": test_name, "passed": passed})
    
    def test_health_check(self):
        """Test 1: Health Check"""
        try:
            response = self.session.get(f"{API_URL}/health")
            passed = response.status_code == 200
            self.log_result(
                "Health Check",
                passed,
                f"Status: {response.status_code}, Response: {response.json()}"
            )
            return passed
        except Exception as e:
            self.log_result("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_create_student(self):
        """Test 2: Create Student (POST)"""
        try:
            student_data = {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "roll": "CS001"
            }
            response = self.session.post(f"{API_URL}/students", json=student_data)
            
            # Check status code
            if response.status_code != 201:
                self.log_result(
                    "Create Student (POST /api/students)",
                    False,
                    f"Expected 201, got {response.status_code}: {response.text}"
                )
                return False
            
            data = response.json()
            self.created_student_id = data.get("_id")
            
            # Validate response structure
            required_fields = ["_id", "name", "email", "roll"]
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                self.log_result(
                    "Create Student (POST /api/students)",
                    False,
                    f"Missing fields: {missing_fields}"
                )
                return False
            
            self.log_result(
                "Create Student (POST /api/students)",
                True,
                f"Created student with ID: {self.created_student_id}"
            )
            return True
        except Exception as e:
            self.log_result("Create Student", False, f"Error: {str(e)}")
            return False
    
    def test_get_all_students(self):
        """Test 3: Get All Students (GET)"""
        try:
            response = self.session.get(f"{API_URL}/students")
            
            if response.status_code != 200:
                self.log_result(
                    "Get All Students (GET /api/students)",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
                return False
            
            data = response.json()
            if not isinstance(data, list):
                self.log_result(
                    "Get All Students",
                    False,
                    f"Expected list, got {type(data)}"
                )
                return False
            
            self.log_result(
                "Get All Students (GET /api/students)",
                True,
                f"Retrieved {len(data)} students"
            )
            return True
        except Exception as e:
            self.log_result("Get All Students", False, f"Error: {str(e)}")
            return False
    
    def test_get_student_count(self):
        """Test 4: Get Student Count"""
        try:
            response = self.session.get(f"{API_URL}/students/count")
            
            if response.status_code != 200:
                self.log_result(
                    "Get Student Count (GET /api/students/count)",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
                return False
            
            data = response.json()
            count = data.get("total_students", -1)
            
            self.log_result(
                "Get Student Count (GET /api/students/count)",
                True,
                f"Total students: {count}"
            )
            return True
        except Exception as e:
            self.log_result("Get Student Count", False, f"Error: {str(e)}")
            return False
    
    def test_get_single_student(self):
        """Test 5: Get Single Student (GET with ID)"""
        if not self.created_student_id:
            self.log_result("Get Single Student", False, "No student ID from creation test")
            return False
        
        try:
            response = self.session.get(f"{API_URL}/students/{self.created_student_id}")
            
            if response.status_code != 200:
                self.log_result(
                    f"Get Single Student (GET /api/students/{self.created_student_id})",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
                return False
            
            data = response.json()
            self.log_result(
                "Get Single Student",
                True,
                f"Retrieved student: {data.get('name')}"
            )
            return True
        except Exception as e:
            self.log_result("Get Single Student", False, f"Error: {str(e)}")
            return False
    
    def test_update_student(self):
        """Test 6: Update Student (PUT)"""
        if not self.created_student_id:
            self.log_result("Update Student", False, "No student ID from creation test")
            return False
        
        try:
            update_data = {
                "name": "Jane Doe",
                "email": "jane.doe@example.com"
            }
            response = self.session.put(
                f"{API_URL}/students/{self.created_student_id}",
                json=update_data
            )
            
            if response.status_code != 200:
                self.log_result(
                    "Update Student (PUT)",
                    False,
                    f"Expected 200, got {response.status_code}"
                )
                return False
            
            data = response.json()
            if data.get("name") == "Jane Doe":
                self.log_result(
                    "Update Student (PUT /api/students/{id})",
                    True,
                    f"Updated student name to: {data.get('name')}"
                )
                return True
            else:
                self.log_result(
                    "Update Student",
                    False,
                    f"Name update failed: {data.get('name')}"
                )
                return False
        except Exception as e:
            self.log_result("Update Student", False, f"Error: {str(e)}")
            return False
    
    def test_duplicate_roll_number(self):
        """Test 7: Duplicate Roll Number Prevention"""
        if not self.created_student_id:
            self.log_result("Duplicate Roll Prevention", False, "No student ID from creation test")
            return False
        
        try:
            duplicate_data = {
                "name": "Another Student",
                "email": "another@example.com",
                "roll": "CS001"  # Same roll as first student
            }
            response = self.session.post(f"{API_URL}/students", json=duplicate_data)
            
            if response.status_code == 400:
                self.log_result(
                    "Duplicate Roll Number Prevention",
                    True,
                    "Correctly rejected duplicate roll number with 400 status"
                )
                return True
            else:
                self.log_result(
                    "Duplicate Roll Number Prevention",
                    False,
                    f"Expected 400, got {response.status_code}: {response.text}"
                )
                return False
        except Exception as e:
            self.log_result("Duplicate Roll Prevention", False, f"Error: {str(e)}")
            return False
    
    def test_invalid_email(self):
        """Test 8: Invalid Email Validation"""
        try:
            invalid_data = {
                "name": "Invalid Email",
                "email": "not-an-email",  # Invalid email
                "roll": "CS999"
            }
            response = self.session.post(f"{API_URL}/students", json=invalid_data)
            
            if response.status_code == 422:
                self.log_result(
                    "Invalid Email Validation",
                    True,
                    "Correctly rejected invalid email with 422 status"
                )
                return True
            else:
                self.log_result(
                    "Invalid Email Validation",
                    False,
                    f"Expected 422, got {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Invalid Email Validation", False, f"Error: {str(e)}")
            return False
    
    def test_invalid_student_id(self):
        """Test 9: Invalid ObjectId Format"""
        try:
            response = self.session.get(f"{API_URL}/students/invalid-id-format")
            
            if response.status_code == 400:
                self.log_result(
                    "Invalid ObjectId Format",
                    True,
                    "Correctly rejected invalid ID format with 400 status"
                )
                return True
            else:
                self.log_result(
                    "Invalid ObjectId Format",
                    False,
                    f"Expected 400, got {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Invalid ObjectId Format", False, f"Error: {str(e)}")
            return False
    
    def test_non_existent_student(self):
        """Test 10: Non-existent Student (404)"""
        try:
            fake_id = "507f1f77bcf86cd799439999"
            response = self.session.get(f"{API_URL}/students/{fake_id}")
            
            if response.status_code == 404:
                self.log_result(
                    "Non-existent Student (404)",
                    True,
                    "Correctly returned 404 for non-existent student"
                )
                return True
            else:
                self.log_result(
                    "Non-existent Student",
                    False,
                    f"Expected 404, got {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Non-existent Student", False, f"Error: {str(e)}")
            return False
    
    def test_delete_student(self):
        """Test 11: Delete Student (DELETE)"""
        if not self.created_student_id:
            self.log_result("Delete Student", False, "No student ID from creation test")
            return False
        
        try:
            response = self.session.delete(f"{API_URL}/students/{self.created_student_id}")
            
            if response.status_code in [200, 204]:
                # Verify student is deleted
                verify_response = self.session.get(f"{API_URL}/students/{self.created_student_id}")
                if verify_response.status_code == 404:
                    self.log_result(
                        "Delete Student (DELETE /api/students/{id})",
                        True,
                        f"Successfully deleted student and verified non-existence"
                    )
                    return True
                else:
                    self.log_result(
                        "Delete Student",
                        False,
                        f"Student still exists after deletion"
                    )
                    return False
            else:
                self.log_result(
                    "Delete Student",
                    False,
                    f"Expected 200/204, got {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_result("Delete Student", False, f"Error: {str(e)}")
            return False
    
    def print_summary(self):
        """Print test summary"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = total - passed
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        print("="*60)
        
        if failed == 0:
            print("\n🎉 All tests passed! Phase 1 implementation is working correctly.")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*60)
        print("PHASE 1 API TEST SUITE")
        print("="*60)
        print(f"Base URL: {BASE_URL}")
        print("="*60)
        
        # Run tests in order
        self.test_health_check()
        self.test_create_student()
        self.test_get_all_students()
        self.test_get_student_count()
        self.test_get_single_student()
        self.test_update_student()
        self.test_duplicate_roll_number()
        self.test_invalid_email()
        self.test_invalid_student_id()
        self.test_non_existent_student()
        self.test_delete_student()
        
        # Print summary
        self.print_summary()


if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=2)
        tester = APITester()
        tester.run_all_tests()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API at http://localhost:8000")
        print("\nMake sure the API is running:")
        print("  python api.py")
        print("\nOr:")
        print("  python -m uvicorn api:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
