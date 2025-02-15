import os
import openai

def run():
    try:
        # Find the correct filename
        possible_filenames = ["credit-card.png", "credit_card.png"]
        directory = "/data/"
        files = os.listdir(directory)

        file_path = None
        for filename in possible_filenames:
            if filename in files:
                file_path = os.path.join(directory, filename)
                break

        if not file_path:
            return {"error": "File not found: credit_card.png"}, 400

        # Open the correct file
        with open(file_path, "rb") as f:
            image_data = f.read()

        # Call OpenAI LLM to extract credit card number
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract the credit card number from the provided image."},
                {"role": "user", "content": image_data}
            ],
            temperature=0.2
        )

        extracted_number = response["choices"][0]["message"]["content"].strip()
        extracted_number = extracted_number.replace(" ", "")  # Remove spaces

        # Save extracted credit card number
        with open("/data/credit-card.txt", "w", encoding="utf-8") as f:
            f.write(extracted_number)

        return {"status": "success"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
