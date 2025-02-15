import os
import json

def run():
    try:
        index = {}
        docs_path = "/data/docs/"

        # Walk through all files and subdirectories
        for root, _, files in os.walk(docs_path):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)

                    # Get path relative to /data/docs/
                    relative_path = os.path.relpath(file_path, docs_path).replace("\\", "/")

                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            if line.startswith("# "):  # First H1 header
                                index[relative_path] = line.strip("# ").strip()
                                break  # Stop after first header

        # Save the index file
        output_path = "/mnt/data/docs/index.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)

        return {"status": "success", "files_indexed": len(index)}, 200

    except Exception as e:
        return {"error": str(e)}, 500
