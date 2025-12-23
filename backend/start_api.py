#!/usr/bin/env python3
"""
Start script for the Physical AI Book RAG API
"""
import subprocess
import sys
import os

def main():
    print("Starting Physical AI Book RAG API...")
    
    # Change to the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Run the API using uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "api:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"  # Enable auto-reload for development
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()