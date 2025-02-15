import subprocess
import os
import re

def run(task_description=""):
    try:
        file_path = "/data/format.md"

        # Ensure file exists
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}, 400

        # Extract Prettier version (default to 3.4.2)
        match = re.search(r"prettier\s*@?([\d.]+)", task_description.lower())
        prettier_version = match.group(1) if match else "3.4.2"

        # Run Prettier
        result = subprocess.run(
            ["npx", f"prettier@{prettier_version}", "--write", file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {"error": result.stderr}, 500

        return {"status": "success"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
