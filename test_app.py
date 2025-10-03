#!/usr/bin/env python3
"""
Simplified tests for temperature-collector-app
"""

import pytest
import os
import sys

# Add src to path
sys.path.insert(0, 'src')

def test_app_imports():
    """Test that the application can be imported without errors"""
    try:
        import app
        assert True
    except ImportError as e:
        pytest.fail(f"Application failed to import: {e}")

def test_app_structure():
    """Test that the application has the required structure"""
    assert os.path.exists("src/app.py"), "src/app.py should exist"
    assert os.path.exists("requirements.txt"), "requirements.txt should exist"
    assert os.path.exists("Dockerfile"), "Dockerfile should exist"

def test_requirements_file():
    """Test that requirements.txt is properly formatted"""
    with open("requirements.txt", "r") as f:
        requirements = f.read()
    
    assert "fastapi" in requirements.lower(), "FastAPI should be in requirements"
    assert "uvicorn" in requirements.lower(), "Uvicorn should be in requirements"

def test_dockerfile_security():
    """Test Dockerfile for security best practices"""
    with open("Dockerfile", "r") as f:
        dockerfile = f.read()
    
    assert "USER appuser" in dockerfile, "Dockerfile should run as non-root user"
    assert "HEALTHCHECK" in dockerfile, "Dockerfile should have health check"

def test_no_hardcoded_secrets():
    """Test that no hardcoded secrets are present in the code"""
    secret_patterns = [
        "password=",
        "secret=",
        "key=",
        "token=",
        "api_key"
    ]
    
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                
                for pattern in secret_patterns:
                    assert pattern not in content, f"Potential hardcoded secret found in {filepath}: {pattern}"

def test_app_endpoints():
    """Test that the application has the required endpoints"""
    with open("src/app.py", "r") as f:
        app_code = f.read()
    
    assert "@app.get(\"/\")" in app_code, "App should have root endpoint"
    assert "@app.get(\"/health\")" in app_code, "App should have health endpoint"
    assert "FastAPI" in app_code, "App should use FastAPI"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
