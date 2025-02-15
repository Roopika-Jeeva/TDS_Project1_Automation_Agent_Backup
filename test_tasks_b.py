import os
import json
import pytest
import requests
import sqlite3
import duckdb
from PIL import Image
from tasks import tasks_phase_b

DATA_DIR = "/data/"
TEST_DB = os.path.join(DATA_DIR, "test.db")
TEST_DUCKDB = os.path.join(DATA_DIR, "test.duckdb")
TEST_CSV = os.path.join(DATA_DIR, "test.csv")

# Ensure test directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

### **B3: Test Fetch API Data**
def test_fetch_api_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Sample API
    output_file = os.path.join(DATA_DIR, "api_output.json")

    response, status_code = tasks_phase_b.fetch_api_data(url, output_file)
    assert status_code == 200
    assert os.path.exists(output_file)

    with open(output_file, "r") as f:
        data = json.load(f)
    assert "title" in data

### **B4: Test Clone and Commit a Git Repo**
def test_clone_and_commit():
    repo_url = "https://github.com/octocat/Hello-World.git"  # Public repo
    commit_message = "Test commit"

    response, status_code = tasks_phase_b.clone_and_commit(repo_url, commit_message)
    assert status_code == 200

### **B5: Test Run SQL Query (SQLite & DuckDB)**
@pytest.fixture(scope="module")
def setup_db():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.commit()
    conn.close()

    ddb = duckdb.connect(TEST_DUCKDB)
    ddb.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    ddb.execute("INSERT INTO users VALUES (1, 'Alice')")
    ddb.close()

def test_run_sql_query(setup_db):
    sqlite_query = "SELECT name FROM users WHERE id = 1"
    duckdb_query = "SELECT name FROM users WHERE id = 1"

    sqlite_response, sqlite_status = tasks_phase_b.run_sql_query(TEST_DB, sqlite_query)
    duckdb_response, duckdb_status = tasks_phase_b.run_sql_query(TEST_DUCKDB, duckdb_query)

    assert sqlite_status == 200
    assert duckdb_status == 200
    assert sqlite_response["data"] == duckdb_response["data"] == [('Alice',)]

### **B6: Test Web Scraping**
def test_scrape_website():
    test_url = "https://example.com"
    output_file = os.path.join(DATA_DIR, "scraped.html")

    response, status_code = tasks_phase_b.scrape_website(test_url, output_file)
    assert status_code == 200
    assert os.path.exists(output_file)

### **B7: Test Image Compression**
def test_compress_resize_image():
    input_image = os.path.join(DATA_DIR, "test_image.jpg")
    output_image = os.path.join(DATA_DIR, "compressed.jpg")

    # Create a sample image
    img = Image.new("RGB", (2000, 2000), color="red")
    img.save(input_image)

    response, status_code = tasks_phase_b.compress_resize_image(input_image, output_image, size=(800, 800))
    assert status_code == 200
    assert os.path.exists(output_image)

### **B8: Test Audio Transcription**
@pytest.mark.skip(reason="Requires OpenAI API Token")
def test_transcribe_audio():
    input_audio = os.path.join(DATA_DIR, "test_audio.mp3")
    output_transcription = os.path.join(DATA_DIR, "transcription.txt")

    response, status_code = tasks_phase_b.transcribe_audio(input_audio, output_transcription)
    assert status_code == 200
    assert os.path.exists(output_transcription)

### **B9: Test Markdown to HTML Conversion**
def test_convert_markdown_to_html():
    input_md = os.path.join(DATA_DIR, "test.md")
    output_html = os.path.join(DATA_DIR, "converted.html")

    with open(input_md, "w") as f:
        f.write("# Hello World\nThis is a test markdown file.")

    response, status_code = tasks_phase_b.convert_markdown_to_html(input_md, output_html)
    assert status_code == 200
    assert os.path.exists(output_html)

### **B10: Test CSV Filtering**
def test_filter_csv():
    with open(TEST_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerow({"name": "Alice", "age": "30"})
        writer.writerow({"name": "Bob", "age": "25"})

    with open(TEST_CSV, "r") as f:
        response = requests.get(f"http://localhost:8000/filter_csv?file={TEST_CSV}&column=name&value=Alice")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Alice"

### **Run all tests**
if __name__ == "__main__":
    pytest.main()
