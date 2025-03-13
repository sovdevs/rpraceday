import os
import time
import subprocess

# Define paths
races_folder = r"C:\Users\996mu\PycharmProjects\rpraceday\static\races"
hash_codes_file = r"C:\Users\996mu\PycharmProjects\rpraceday\hash_codes.json"
generate_hashes_script = r"C:\Users\996mu\PycharmProjects\rpraceday\generate_hashes.py"
generate_random_html_script = r"C:\Users\996mu\PycharmProjects\rpraceday\generate_random_hash_html.py"

def delete_files_in_folder(folder_path):
    """Deletes all files in the specified folder."""
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"❌ Error deleting {file_path}: {e}")
    else:
        print(f"⚠️ Folder not found: {folder_path}")

def delete_file(file_path):
    """Deletes a single file, ignoring errors if it doesn't exist."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"⚠️ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error deleting {file_path}: {e}")

def run_script(script_path):
    """Runs a Python script using subprocess."""
    try:
        print(f"Running script: {script_path}")
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running script {script_path}: {e}")

if __name__ == "__main__":
    print("🚀 Starting cleanup process...")

    # Step 1: Delete all files in the races folder
    delete_files_in_folder(races_folder)

    # Step 2: Delete the hash_codes.json file
    delete_file(hash_codes_file)

    # Step 3: Run generate_hashes.py
    run_script(generate_hashes_script)

    # Step 4: Wait for 60 seconds before running the next script
    print("⏳ Waiting 60 seconds before running the next script...")
    time.sleep(60)

    # Step 5: Run generate_random_hash_html.py
    run_script(generate_random_html_script)

    print("✅ Process completed successfully!")
