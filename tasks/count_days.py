import os
import datetime

def run():
    try:
        file_path = "/data/dates.txt"
        output_path = "/data/dates-wednesdays.txt"

        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}, 400

        wednesday_count = 0
        failed_dates = []

        date_formats = [
            "%Y-%m-%d",
            "%Y/%m/%d %H:%M:%S",
            "%d-%b-%Y",
            "%b %d, %Y"
        ]

        with open(file_path, "r") as f:
            for line in f:
                date_str = line.strip()
                date_obj = None

                for fmt in date_formats:
                    try:
                        date_obj = datetime.datetime.strptime(date_str, fmt)
                        break  # Stop checking once parsed
                    except ValueError:
                        continue
                
                if date_obj:
                    if date_obj.weekday() == 2:  # Wednesday
                        wednesday_count += 1
                else:
                    failed_dates.append(date_str)

        with open(output_path, "w") as f:
            f.write(str(wednesday_count))

        if failed_dates:
            with open("/mnt/data/failed_dates.txt", "w") as f:
                f.write("\n".join(failed_dates))

        return {"status": "success", "wednesday_count": wednesday_count}, 200

    except Exception as e:
        return {"error": str(e)}, 500

