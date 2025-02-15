import os
import json
import requests
import sqlite3
import duckdb
import subprocess
import markdown
from PIL import Image
from git import Repo
import openai
import csv
from bs4 import BeautifulSoup
from flask import request, jsonify

# Ensure OpenAI API key is set
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
openai.api_key = os.getenv("AIPROXY_TOKEN")

# Security enforcement: Restrict all actions to /data directory
DATA_DIR = "/data/"

def check_path_safety(path):
    """Ensure the path is inside /data"""
    if not path.startswith(DATA_DIR):
        raise PermissionError(f"Access denied: {path} is outside {DATA_DIR}")

### **B3: Fetch data from an API and save it**
def fetch_api_data(api_url, output_file):
    try:
        check_path_safety(output_file)
        response = requests.get(api_url)
        response.raise_for_status()
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4)
        
        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

### **B4: Clone a Git repo and make a commit**
def clone_and_commit(repo_url, commit_message):
    try:
        repo_dir = os.path.join(DATA_DIR, "repo")
        check_path_safety(repo_dir)

        if not os.path.exists(repo_dir):
            Repo.clone_from(repo_url, repo_dir)

        repo = Repo(repo_dir)
        repo.git.add(A=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()

        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

### **B5: Run a SQL query on a SQLite or DuckDB database**
def run_sql_query(db_path, query):
    try:
        check_path_safety(db_path)

        if db_path.endswith(".db"):
            conn = sqlite3.connect(db_path)
        elif db_path.endswith(".duckdb"):
            conn = duckdb.connect(db_path)
        else:
            return {"error": "Unsupported database format"}, 400

        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return {"status": "success", "data": results}, 200
    except Exception as e:
        return {"error": str(e)}, 500

### **B6: Extract data from a website (scraping)**
def scrape_website(url, output_file):
    try:
        check_path_safety(output_file)

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

### **B7: Compress or resize an image**
def compress_resize_image(input_path, output_path, size=(800, 800)):
    try:
        check_path_safety(input_path)
        check_path_safety(output_path)

        img = Image.open(input_path)
        img = img.resize(size)
        img.save(output_path, quality=80, optimize=True)

        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

### **B8: Transcribe audio from an MP3 file**
def transcribe_audio(audio_path, output_file):
    try:
        check_path_safety(audio_path)
        check_path_safety(output_file)

        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript["text"])

        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

### **B9: Convert Markdown to HTML**
def convert_markdown_to_html(md_file, html_file):
    try:
        check_path_safety(md_file)
        check_path_safety(html_file)

        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
        
        html_content = markdown.markdown(md_content)

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

### **B10: CSV Filtering API**
def filter_csv():
    csv_path = request.args.get("file")
    column = request.args.get("column")
    value = request.args.get("value")
    check_path_safety(csv_path)

    if not os.path.exists(csv_path):
        return {"error": f"File not found: {csv_path}"}, 404

    filtered_data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get(column) == value:
                filtered_data.append(row)

    return jsonify(filtered_data), 200
