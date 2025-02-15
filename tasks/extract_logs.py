import os

def run():
    try:
        logs_dir = "/data/logs"
        log_files = sorted(
            [f for f in os.listdir(logs_dir) if f.endswith(".log")],
            key=lambda x: os.path.getmtime(os.path.join(logs_dir, x)),
            reverse=True
        )[:10]

        with open("/data/logs-recent.txt", "w") as output:
            for log_file in log_files:
                with open(os.path.join(logs_dir, log_file), "r") as log:
                    first_line = log.readline().strip()
                    output.write(first_line + "\n")

        return {"status": "success"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
