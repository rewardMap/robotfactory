
import requests

# OSF file download URL (direct link)


import requests
from pathlib import Path

# Get the path to the current script's directory
script_dir = Path(__file__).resolve().parent

file_url = "https://osf.io/download/6tsfd"
output_file = "BACS2sans.otf"  # You can give it a specific name with extension

# Send request
response = requests.get(file_url)

if response.status_code == 200:

    # Create the full path in the script's folder
    output_path = script_dir / output_file

    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"File downloaded successfully to: {output_path}")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
