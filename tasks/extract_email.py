import openai
import os
import re

def run():
    try:
        # Set OpenAI API key and base URL
        openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
        openai.api_key = os.getenv("AIPROXY_TOKEN")

        # Read the email file content
        with open("/data/email.txt", "r", encoding="utf-8") as f:
            email_content = f.read()

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract the sender's email address from the following email message."},
                {"role": "user", "content": email_content}
            ],
            temperature=0.2
        )

        # Extract email from response
        extracted_email = response["choices"][0]["message"]["content"].strip()

        # Validate email format
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        match = re.search(email_pattern, extracted_email)
        if match:
            extracted_email = match.group(0)
        else:
            return {"error": "No valid email found"}, 400

        # Save extracted email to file (if the file does not exist, it will be created)
        with open("/data/email-sender.txt", "w", encoding="utf-8") as f:
            f.write(extracted_email)

        return {"status": "success"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
