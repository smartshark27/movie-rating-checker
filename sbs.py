import base64
import json
import requests

# This script fetches a list of movies from the SBS On Demand catalogue.
# It uses the public API endpoint to retrieve movie data.

url = "https://catalogue.pr.sbsod.com/collections/all-movies"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en",
    "Origin": "https://www.sbs.com.au",
    "Priority": "u=3,i",
    "Referer": "https://www.sbs.com.au/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0",
}
items_per_page = "100"
max_pages = 20
output_file = "sbs_movies.json"


def get_all_movies():
    """
    Fetch all movies from the SBS On Demand catalogue.
    """
    # Build the cursor query param
    cursor_dict = {
        "audio": "",
        "genre": "",
        "language": "",
        "limit": items_per_page,
        "page": "1",
        "sort": "",
        "subtitle": "",
        "type": "",
    }

    movies = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        cursor_dict["page"] = str(page)
        cursor = base64.b64encode(json.dumps(cursor_dict).encode()).decode()

        response = requests.get(url, headers=headers, params={"cursor": cursor})
        data = response.json()

        if not data.get("items"):
            print("No more items found, stopping.")
            break

        movies.extend(
            [
                {"title": item["title"], "releaseYear": item["releaseYear"]}
                for item in data["items"]
            ]
        )

    print(f"Total movies found: {len(movies)}")
    return movies


def save_to_json_file(data, filename):
    """
    Save a list of dictionaries to a JSON file.

    :param data: List of dictionaries to save
    :param filename: Name of the JSON file
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



movies = get_all_movies()
save_to_json_file(movies, output_file)
