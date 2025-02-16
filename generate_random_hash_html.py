import json
import random


def generate_random_hash_html(json_file="hash_codes.json"):
    """
    Reads a JSON file, selects 5 random key-value pairs, and generates an HTML div snippet.

    Parameters:
    - json_file (str): The filename of the JSON file.

    Returns:
    - str: An HTML snippet containing five random key-value pairs.
    """
    try:
        # Load the JSON file
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Ensure we have at least five pairs to select from
        # Ensure there's enough data
        if len(data) < 5:
            return "⚠️ Not enough data in JSON file!"

        # Pick 5 random pairs
        random_pairs = random.sample(list(data.items()), 5)
        no_of_races = len(data.keys())

        # ✅ Use f-string to insert `no_of_races` dynamically
        html_snippet = f"""
        <div class="random-hash-container">
            <h2>🔑 {no_of_races} races under consideration today. Here is a selection:</h2>
            <ul>
        """
        for key, value in random_pairs:
            html_snippet += f'<li><strong>ID:</strong> {key} - <strong>Hash:</strong> {value}</li>\n'

        html_snippet += """
            </ul>
        </div>
        """

        # Print the result
        print(html_snippet)

        return html_snippet

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return ""


# Call the function to print the output
generate_random_hash_html()
