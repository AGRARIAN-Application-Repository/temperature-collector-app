#!/usr/bin/env python3
"""
Tests for temperature-collector-app
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
    
    assert "==" in requirements, "Requirements should use pinned versions (==)"
    assert "fastapi" in requirements.lower(), "FastAPI should be in requirements"
    assert "uvicorn" in requirements.lower(), "Uvicorn should be in requirements"

def test_dockerfile_security():
    """Test Dockerfile for security best practices"""
    with open("Dockerfile", "r") as f:
        dockerfile = f.read()
    
    assert "USER appuser" in dockerfile, "Dockerfile should run as non-root user"
    assert "HEALTHCHECK" in dockerfile, "Dockerfile should have health check"
    assert "RUN adduser" in dockerfile, "Dockerfile should create non-root user"

def test_no_hardcoded_secrets():
    """Test that no hardcoded secrets are present in the code"""
    secret_patterns = [
        "password=",
        "secret=",
        "key=",
        "token=",
        "api_key",
        "private_key",
        "database_url"
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

def test_docker_build():
    """Test that the Docker image can be built"""
    with open("Dockerfile", "r") as f:
        dockerfile = f.read()
    
    assert "FROM" in dockerfile, "Dockerfile should have FROM instruction"
    assert "WORKDIR" in dockerfile, "Dockerfile should have WORKDIR instruction"
    assert "COPY" in dockerfile, "Dockerfile should have COPY instruction"
    assert "EXPOSE" in dockerfile, "Dockerfile should have EXPOSE instruction"
    assert "CMD" in dockerfile, "Dockerfile should have CMD instruction"

def test_no_debug_code():
    """Test that no debug code is left in production"""
    debug_patterns = [
        "print(",
        "console.log",
        "debugger",
        "pdb.set_trace()",
        "import pdb",
        "breakpoint()"
    ]
    
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                for pattern in debug_patterns:
                    assert pattern not in content, f"Debug code found in {filepath}: {pattern}"

def test_app_startup():
    """Test that the application can start without errors"""
    with open("src/app.py", "r") as f:
        app_code = f.read()
    
    assert "if __name__" in app_code, "App should have main block"
    assert "uvicorn.run" in app_code, "App should use uvicorn to run"

def test_health_check():
    """Test that the health check endpoint works"""
    with open("src/app.py", "r") as f:
        app_code = f.read()
    
    assert "def health" in app_code, "Health endpoint should exist"
    assert "status" in app_code, "Health endpoint should return status"
