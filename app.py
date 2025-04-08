from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os
import json
import hashlib
from datetime import datetime
import requests
app = Flask(__name__, static_folder="static")  # Ensure static folder is recognized
app.secret_key = 'bollox'  # Required for flash messages
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


#https://api.telegram.org/bot7856304734:AAES5Q2j3tI4OLlo6A5w1GXnkHka4nx836w/getUpdates
def send_telegram_alert(new_email):
    bot_token = "7856304734:AAES5Q2j3tI4OLlo6A5w1GXnkHka4nx836w"
    chat_id = "6147599687"
    message = f"📥 New subscriber: {new_email}"

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message}
        )
        if response.ok:
            print("✅ Telegram alert sent.")
        else:
            print(f"⚠️ Telegram alert failed: {response.text}")
    except Exception as e:
        print(f"❌ Error sending Telegram alert: {e}")


# ✅ Generate Cheat Code on Startup
cheat_hash = generate_daily_cheat_code()
print(f"📌 Today's Cheat Code: {cheat_hash}")  # ✅ This will now run at app startup
@app.route("/", methods=["GET", "POST"])
def index():
    race_data = None
    error = None
    race_id = None
    entered_hash = None


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

    return render_template("index.html", race_data=race_data, race_id=race_id, hash_code=entered_hash, error=error)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip()
    send_telegram_alert(email)
    # Simple email validation
    if '@' not in email:
        flash('❌ Please enter a valid email address', 'danger')
        return redirect(url_for('index'))

    # Create emails.txt if it doesn't exist
    if not os.path.exists('emails.txt'):
        open('emails.txt', 'w').close()

    # Check for duplicates
    with open('emails.txt', 'r') as f:
        existing_emails = f.read().splitlines()

    if email in existing_emails:
        flash("ℹ️ You are already subscribed!", "info")
        return redirect(url_for('index'))

    # Save email
    with open('emails.txt', 'a') as f:
        f.write(f"{email}\n")


    flash('✅ Thank you for subscribing!', 'success')
    return redirect(url_for('index'))



@app.route("/download", methods=["POST"])
def download_txt():
    race_id = request.form.get("race_id", "").strip()

    if not race_id:
        return "Invalid race ID.", 400

    txt_file_path = os.path.join(RACE_TXT_DIR, f"{race_id}.txt")

    if os.path.exists(txt_file_path):
        return send_file(txt_file_path, as_attachment=True)
    else:
        return "File not found.", 404


if __name__ == "__main__":
    app.run(debug=True)
