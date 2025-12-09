"""
Test script to verify backend is working correctly
Run after starting the backend server
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print('='*60)

def test_health():
    """Test health endpoint"""
    print_step(1, "Testing Health Check")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Health check passed!")

def test_register():
    """Test user registration"""
    print_step(2, "Testing User Registration")
    
    # Generate unique email
    timestamp = int(time.time())
    test_email = f"test{timestamp}@example.com"
    
    data = {
        "email": test_email,
        "full_name": "Test User",
        "password": "password123",
        "role": "researcher"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Registration passed!")
    
    return test_email

def test_login(email):
    """Test user login"""
    print_step(3, "Testing User Login")
    
    data = {
        "email": email,
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 200
    assert "access_token" in result
    print("✅ Login passed!")
    
    return result["access_token"]

def test_get_me(token):
    """Test getting current user"""
    print_step(4, "Testing Get Current User")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Get current user passed!")

def test_create_project(token):
    """Test creating a project"""
    print_step(5, "Testing Create Project")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Test Pharmaceutical Project",
        "molecule_name": "Aspirin",
        "description": "Testing project creation"
    }
    
    response = requests.post(f"{BASE_URL}/projects", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 201
    print("✅ Create project passed!")
    
    return result["id"]

def test_list_projects(token):
    """Test listing projects"""
    print_step(6, "Testing List Projects")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/projects", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {len(result)} project(s)")
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 200
    print("✅ List projects passed!")

def test_execute_agent(token, project_id):
    """Test agent execution"""
    print_step(7, "Testing Agent Execution")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "project_id": project_id,
        "agent_type": "patent_search",
        "input_text": "Search for aspirin-related patents"
    }
    
    response = requests.post(f"{BASE_URL}/agents/execute", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Agent execution passed!")

def test_get_logs(token):
    """Test getting agent logs"""
    print_step(8, "Testing Get Agent Logs")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/agents/logs", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {len(result)} log(s)")
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 200
    print("✅ Get logs passed!")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 PHARMAPILOT BACKEND TEST SUITE")
    print("="*60)
    
    try:
        # Run tests
        test_health()
        email = test_register()
        token = test_login(email)
        test_get_me(token)
        project_id = test_create_project(token)
        test_list_projects(token)
        test_execute_agent(token, project_id)
        test_get_logs(token)
        
        # Success message
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 Your backend is working perfectly!")
        print("\nYou can now:")
        print("1. Start your frontend (npm run dev in Client folder)")
        print("2. Register and login through the UI")
        print("3. Start building your AI agents")
        print("\nAPI Documentation: http://localhost:8000/docs")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend!")
        print("Make sure the backend is running: uvicorn app.main:app --reload --port 8000")
        print("Or use the quick start: .\\start.ps1 or start.bat")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    main()
