import subprocess
import os
import re

def run(task_description=""):
    try:
        # Install uv if not already installed
        subprocess.run(["pip", "install", "uv"], check=True)
        subprocess.run(["pip", "install", "faker"], check=True)

        # Extract email from task description
        match = re.search(r"with `([^`]+)` as the only argument", task_description)
        email = match.group(1) if match else "user@example.com"  # Default to expected value

        # Run datagen.py with the extracted email
        subprocess.run(["python", "data/datagen.py", email], check=True)

        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
