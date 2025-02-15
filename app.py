from flask import Flask, request, jsonify
import os
import json
from tasks import (
    format,
    count_days,
    sort_contacts,
    extract_email,
    detect_credit_card,
    ticket_sales,
    install_uv,
    extract_logs,
    extract_markdown_headers,
    find_similar_comments
)

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_task():
    task = request.args.get('task', '').lower()
    if not task:
        return jsonify({"error": "Task description missing"}), 400

    try:
        if "install uv" in task or "datagen" in task:
            return install_uv.run()
        elif "format" in task:
            return format.run()
        elif "wednesday" in task:
            return count_days.run()
        elif "sort contacts" in task or "contacts" in task:
            return sort_contacts.run()
        elif "extract email" in task or "sender's email" in task or "email" in task:
            return extract_email.run()
        elif "credit card" in task or "card" in task:
            return detect_credit_card.run()
        elif "ticket sales" in task or "total sales" in task or "Gold" in task:
            return ticket_sales.run()
        elif "log files" in task or "logs" in task:
            return extract_logs.run()
        elif "markdown" in task or "headers" in task:
            return extract_markdown_headers.run()
        elif "similar comments" in task or"comments" in task:
            return find_similar_comments.run()
        # Phase B Tasks
        elif "fetch api" in task or "fetch" in task:
            return tasks_phase_b.fetch_api_data(request.args.get("url"), request.args.get("output"))
        elif "clone git" in task or "git clone" in task or "clone repository" in task:
            return tasks_phase_b.clone_and_commit(request.args.get("repo"), request.args.get("message"))
        elif "run sql" in task or "sql run" in task:
            return tasks_phase_b.run_sql_query(request.args.get("db"), request.args.get("query"))
        elif "scrape website" in task or "scrape" in task:
            return tasks_phase_b.scrape_website(request.args.get("url"), request.args.get("output"))
        elif "compress image" in task or "compress" in task:
            return tasks_phase_b.compress_resize_image(request.args.get("input"), request.args.get("output"))
        elif "transcribe audio" in task or "transcribe" in task:
            return tasks_phase_b.transcribe_audio(request.args.get("input"), request.args.get("output"))
        elif "convert markdown" in task or "convert html" in task:
            return tasks_phase_b.convert_markdown_to_html(request.args.get("input"), request.args.get("output"))
        
        else:
            return jsonify({"error": "Unknown task"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path', '')

    if not os.path.exists(file_path):
        return "File not found", 404  # Return raw error message instead of JSON

    with open(file_path, 'r') as f:
        content = f.read()

    return content, 200  # Return raw file content (No JSON Wrapping)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
