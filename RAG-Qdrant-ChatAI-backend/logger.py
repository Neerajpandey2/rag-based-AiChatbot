import json

def log_line(results, filename="qa_log.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

# import json
# from datetime import datetime

# def log_line(results, filename="qa_log.json", label=None):
#     log_data = {
#         "timestamp": datetime.now().isoformat(),
#         "label": label,
#         "data": results
#     }
#     with open(filename, "a", encoding="utf-8") as f:  # append instead of overwrite
#         f.write(json.dumps(log_data, ensure_ascii=False, indent=4) + "\n")

