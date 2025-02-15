import json
import os

def run():
    try:
        file_path = "/data/contacts.json"
        output_path = "/data/contacts-sorted.json"

        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}, 400

        with open(file_path, "r") as f:
            contacts = json.load(f)

        sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

        with open(output_path, "w") as f:
            json.dump(sorted_contacts, f, indent=4)

        return {"status": "success"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
