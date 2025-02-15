import sqlite3
import os

def run():
    try:
        db_path = "/data/ticket-sales.db"
        output_path = "/data/ticket-sales-gold.txt"

        if not os.path.exists(db_path):
            return {"error": f"Database not found: {db_path}"}, 400

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Normalize ticket type to avoid case-sensitive mismatches
        cursor.execute("""
            SELECT SUM(units * price) 
            FROM tickets 
            WHERE LOWER(type) = 'gold'
        """)
        total_sales = cursor.fetchone()[0]

        conn.close()

        if total_sales is None:
            total_sales = 0.0

        # Write the exact expected output format (2 decimal places)
        with open(output_path, "w") as f:
            f.write(f"{total_sales:.2f}")

        return {"status": "success"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
