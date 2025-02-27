from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import json
import hashlib
from datetime import datetime
app = Flask(__name__, static_folder="static")  # Ensure static folder is recognized

RACE_TXT_DIR = "static/races"
HASH_FILE = "hash_codes.json"

# Load hash codes
if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r", encoding="utf-8") as f:
        hash_codes = json.load(f)
else:
    hash_codes = {}

def generate_daily_cheat_code():
    """Generates a daily changing cheat hash based on the current date."""
    today_str = datetime.today().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
    return hashlib.md5(today_str.encode()).hexdigest()[:8]  # Shortened to 8 characters

@app.route("/", methods=["GET", "POST"])
def index():
    race_data = None
    error = None
    race_id = None
    entered_hash = None

    cheat_hash = generate_daily_cheat_code()
    print(f"📌 Today's Cheat Code: {cheat_hash}")  # ✅ Prints the daily cheat code

    if request.method == "POST":
        race_id = request.form.get("race_id", "").strip()
        entered_hash = request.form.get("hash_code", "").strip()
        print(len(hash_codes))
        if not race_id:
            error = "❌ Please enter a race ID."
        elif race_id not in hash_codes:
            error = "❌ Invalid race ID. No data found."
        elif entered_hash != hash_codes.get(race_id) and entered_hash != cheat_hash:  # ✅ Allow cheat hash
            error = "❌ Incorrect hash code. Access denied."
        else:
            txt_file_path = os.path.join(RACE_TXT_DIR, f"{race_id}.txt")
            if os.path.exists(txt_file_path):
                with open(txt_file_path, "r", encoding="utf-8") as file:
                    race_data = file.read()
            else:
                error = f"❌ No race found for ID {race_id}."

    return render_template("index4.html", race_data=race_data, race_id=race_id, hash_code=entered_hash, error=error)

@app.route("/download", methods=["POST"])
def download_txt():
    race_id = request.form.get("race_id", "").strip()
    entered_hash = request.form.get("hash_code", "").strip()

    if not race_id or race_id not in hash_codes:
        return "Invalid race ID.", 400

    correct_hash = hash_codes.get(race_id)

    if entered_hash != correct_hash:
        return "❌ ERROR: Incorrect hash code. Access denied.", 403

    txt_file_path = os.path.join(RACE_TXT_DIR, f"{race_id}.txt")

    if os.path.exists(txt_file_path):
        return send_file(txt_file_path, as_attachment=True)
    else:
        return "File not found.", 404

if __name__ == "__main__":
    app.run(debug=True)
