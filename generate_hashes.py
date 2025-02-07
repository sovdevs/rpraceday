import json
import hashlib
import os

# ✅ Get the current working directory
RACE_DIR = "C:\\Users\\996mu\\PycharmProjects\\DA_VisuqalComp1\\rpscrape\\races"
HASH_FILE = "hash_codes.json"

# Load existing hashes
if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r", encoding="utf-8") as f:
        hash_codes = json.load(f)
else:
    hash_codes = {}

# ✅ Generate a hash for each race_id in the current directory
for filename in os.listdir(RACE_DIR):
    if filename.endswith(".txt"):
        race_id = filename.replace(".txt", "")
        if race_id not in hash_codes:
            hash_value = hashlib.sha256(race_id.encode()).hexdigest()[:8]  # Shortened 8-char hash
            hash_codes[race_id] = hash_value

# ✅ Save the updated hash codes
with open(HASH_FILE, "w", encoding="utf-8") as f:
    json.dump(hash_codes, f, indent=4)

print(f"✅ Hash codes generated and saved in {HASH_FILE}")
