import json
import random

## April 6th version.
def generate_random_hash_html(json_file="hash_codes.json"):
    """
    Reads a JSON file, selects 5 random key-value pairs, and generates a styled Bootstrap snippet.

    Parameters:
    - json_file (str): Path to the JSON file.

    Returns:
    - str: An HTML snippet with selected hashes.
    """
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        if len(data) < 5:
            return "⚠️ Not enough data in JSON file!"

        random_pairs = random.sample(list(data.items()), 5)
        no_of_races = len(data)

        # ✅ HTML snippet in Bootstrap badge+code format
        html_snippet = f"""
            <!-- Right Column (Info) -->
            <div class="col-md-4">
                <div class="random-hash-container p-4 rounded-3 shadow">
                    <h2 class="h4 mb-3">🔑 {no_of_races} races under consideration. Here's a selection:</h2>
                    <ul class="list-unstyled">
        """

        for key, value in random_pairs:
            html_snippet += f"""
                        <li class="mb-2">
                            <span class="badge bg-primary">{key}</span>
                            <code>{value}</code>
                        </li>
            """

        html_snippet += """
                    </ul>
                </div>
            </div>
        """

        print(html_snippet)
        return html_snippet

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return ""


# Call the function to print the output
generate_random_hash_html()
