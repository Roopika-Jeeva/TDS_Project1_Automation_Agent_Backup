import requests
import time

BASE_URL = "http://localhost:8000"

def test_task(task_description, output_file=None):
    """ Sends a POST request to run a task and verifies the output if applicable. """
    print(f"\n🔹 Testing: {task_description}")
    response = requests.post(f"{BASE_URL}/run?task={task_description}")
    
    if response.status_code == 200:
        print("✅ Success:", response.json())
        if output_file:
            time.sleep(1)  # Wait a second before checking the file
            check_output(output_file)
    else:
        print("❌ Failed:", response.json())

def check_output(file_path):
    """ Sends a GET request to read a file and prints the content. """
    response = requests.get(f"{BASE_URL}/read?path={file_path}")
    
    if response.status_code == 200:
        print(f"📂 File ({file_path}) Content:\n", response.json().get("content", "No content"))
    else:
        print(f"❌ Error reading {file_path}: {response.json()}")

# ✅ Test Cases for Each Task
test_task("Install uv and run datagen.py", None)
test_task("Format /data/format.md with Prettier 3.4.2", "/data/format.md")
test_task("Count the number of Wednesdays in /data/dates.txt", "/data/dates-wednesdays.txt")
test_task("Sort contacts in /data/contacts.json", "/data/contacts-sorted.json")
test_task("Extract the first line of the 10 most recent log files in /data/logs", "/data/logs-recent.txt")
test_task("Extract the H1 headers from Markdown files in /data/docs", "/data/docs/index.json")
test_task("Extract the sender's email from /data/email.txt", "/data/email-sender.txt")
test_task("Extract the credit card number from /data/credit-card.png", "/data/credit-card.txt")
test_task("Find the most similar comments in /data/comments.txt", "/data/comments-similar.txt")
test_task("Get total sales for 'Gold' tickets from /data/ticket-sales.db", "/data/ticket-sales-gold.txt")

print("\n✅ All tasks tested! Review the output above.")

