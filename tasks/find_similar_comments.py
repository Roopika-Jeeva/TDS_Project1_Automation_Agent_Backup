import os
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def run():
    try:
        openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
        openai.api_key = os.getenv("AIPROXY_TOKEN")

        input_path = "/data/comments.txt"
        output_path = "/data/comments-similar.txt"

        if not os.path.exists(input_path):
            return {"error": f"File not found: {input_path}"}, 400

        # Read comments
        with open(input_path, "r", encoding="utf-8") as f:
            comments = [line.strip() for line in f if line.strip()]

        if len(comments) < 2:
            return {"error": "Not enough comments for similarity comparison"}, 400

        # Get embeddings
        response = openai.Embedding.create(
            input=comments,
            model="text-embedding-ada-002"
        )
        embeddings = np.array([e["embedding"] for e in response["data"]])

        # Compute cosine similarity
        similarity_matrix = cosine_similarity(embeddings)
        np.fill_diagonal(similarity_matrix, 0)  # Ignore self-similarity
        most_similar_indices = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
        comment1, comment2 = comments[most_similar_indices[0]], comments[most_similar_indices[1]]

        # Write most similar comments
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"{comment1}\n{comment2}")

        return {"status": "success"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
