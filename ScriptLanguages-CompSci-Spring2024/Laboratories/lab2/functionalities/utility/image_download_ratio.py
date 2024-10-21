# image_download_ratio.py
import sys
import json

def calculate_image_download_ratio():
    image_count = 0
    other_count = 0
    for line in sys.stdin:
        try:
            log_entry = json.loads(line)
            request_line = log_entry["request_line"].lower()
            if any(ext in request_line for ext in [".gif", ".jpg", ".jpeg", ".xbm"]):
                image_count += 1
            else:
                other_count += 1
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)
    
    total = image_count + other_count
    if total > 0:
        ratio = image_count / total
        print(f"Image download ratio: {ratio:.3f} (Images: {image_count}, Others: {other_count})")
    else:
        print("No valid requests found.")

if __name__ == "__main__":
    calculate_image_download_ratio()
