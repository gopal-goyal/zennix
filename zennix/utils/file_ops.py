import os
from datetime import datetime

def save_file(content: str, output_path: str, filename: str = "README.md", timestamp: bool = True):
    # Add timestamp to filename if needed
    if timestamp:
        name, ext = os.path.splitext(filename)
        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{time_str}{ext}"

    full_path = os.path.join(output_path, filename)

    # Ensure directory exists
    os.makedirs(output_path, exist_ok=True)

    # Write file
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved: {full_path}")
