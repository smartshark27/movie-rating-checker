import base64
import json
import requests

# This script fetches a list of media in a collection from the SBS On Demand catalogue.
# It uses the public API endpoint to retrieve collection data.

collection_urls = {
    "all-movies": "https://catalogue.pr.sbsod.com/collections/all-movies",
    "recently-added-movies": "https://catalogue.pr.sbsod.com/collections/recently-added-movies",
}
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


def get_sbs_media_list(collection="recently-added-movies"):
    """
    Fetch all media from a collection from the SBS On Demand catalogue.
    """
    if collection not in collection_urls:
        raise ValueError(
            f"Invalid collection '{collection}'. Must be one of {list(collection_urls.keys())}."
        )
    url = collection_urls[collection]

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

    media_list = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        cursor_dict["page"] = str(page)
        cursor = base64.b64encode(json.dumps(cursor_dict).encode()).decode()

        response = requests.get(url, headers=headers, params={"cursor": cursor})
        data = response.json()
        print(f"Response data: ---{data}---")

        if not data.get("items"):
            print("No more items found, stopping.")
            break

        media_list.extend(
            [
                {
                    "mediaType": item["entityType"],
                    "title": item["title"],
                    "year": str(item["releaseYear"]),
                    "sbsURL": "https://www.sbs.com.au/ondemand/movie/"
                    + item["slug"]
                    + "/"
                    + str(item["mpxMediaID"]),
                }
                for item in data["items"]
            ]
        )

    print(f"Total media found: {len(media_list)}")
    return media_list


if __name__ == "__main__":
    media_list = get_sbs_media_list("recently-added-movies")
    print("media:", media_list)


# Sample movie data structure from the API:
# {
#   "id": "52aec713-aab7-57a6-a1c7-1cc6e66f549e",
#   "entityType": "DYNAMIC_COLLECTION",
#   "localeID": "en",
#   "title": "Recently Added Movies",
#   "description": "Find a new favourite among our new release movies, returning classics, and all the languages of cinema.",
#   "slug": "recently-added-movies",
#   "displayType": "2x3",
#   "layout": "GRID",
#   "images": [
#     {
#       "id": "81c601ad-5ea3-5667-a525-9dabbb3e6f48",
#       "category": "16:9|1920|1080|BANNER"
#     },
#     {
#       "id": "05471ba4-c25f-569c-9a48-3bc696aef97d",
#       "category": "16:9|1920|1080|KEY_ART"
#     },
#     {
#       "id": "9e5a058f-5822-571e-a805-5a187d2fa592",
#       "category": "1:1|700|700|MASK"
#     },
#     {
#       "id": "09543c74-f1b3-53e1-83b0-6a25e5cbc1a4",
#       "category": "2:3|960|1440|BANNER"
#     },
#     {
#       "id": "8370b9bc-2979-5b61-af9a-9655a307107e",
#       "category": "2:3|960|1440|KEY_ART"
#     }
#   ],
#   "items": [
#     {
#       "id": "0f45e964-805d-54d5-9419-1f51b0c728e4",
#       "entityType": "MOVIE",
#       "title": "Iceman",
#       "slug": "iceman",
#       "description": "A Neolithic clan leader seeks vengeance for the brutal massacre of his people and the desecration of their holy shrine.",
#       "genres": ["Adventure", "Drama"],
#       "languages": ["German"],
#       "textTracks": [],
#       "availability": {
#         "start": "2025-10-07T13:50:00Z",
#         "end": "2025-11-06T13:50:00Z"
#       },
#       "hasAudioDescription": false,
#       "classificationID": "MA15+",
#       "images": [
#         {
#           "id": "c0979e7a-3af7-5f35-a677-88856dd9f9dc",
#           "category": "2:3|1920|2880|BANNER"
#         }
#       ],
#       "distributors": [{ "id": "558", "name": "Beta Film Gmbh & Co" }],
#       "cdpTitle": "Iceman",
#       "duration": "PT1H32M14S",
#       "mpxMediaID": 2173516867581,
#       "releaseYear": 2017
#     }
#   ],
#   "trailers": [],
#   "meta": {
#     "nextCursor": "eyJhdWRpbyI6IiIsImdlbnJlIjoiIiwibGFuZ3VhZ2UiOiIiLCJsaW1pdCI6IjEiLCJwYWdlIjoiMiIsInNvcnQiOiIiLCJzdWJ0aXRsZSI6IiIsInR5cGUiOiIifQ==",
#     "count": 1,
#     "total": 100
#   },
#   "filters": {
#     "audio": ["Audio Description"],
#     "type": ["Movie"],
#     "genre": [
#       "Action",
#       "Adventure",
#       "Biography",
#       "Comedy",
#       "Comedy drama",
#       "Crime drama",
#       "Dark comedy",
#       "Documentary",
#       "Drama",
#       "Family",
#       "Fantasy",
#       "Historical drama",
#       "Music",
#       "Musical comedy",
#       "Mystery",
#       "Rock",
#       "Romance",
#       "Romantic comedy",
#       "Thriller",
#       "War",
#       "Western"
#     ],
#     "language": [
#       "Arabic",
#       "Bengali",
#       "Czech",
#       "English",
#       "French",
#       "German",
#       "Greek",
#       "Hindi",
#       "Hungarian",
#       "Inuktitut",
#       "Italian",
#       "Japanese",
#       "Kannada",
#       "Korean",
#       "Kurdish",
#       "Latin",
#       "Malayalam",
#       "Mandarin Chinese",
#       "Marathi",
#       "Nepali",
#       "Portuguese",
#       "Punjabi",
#       "Russian",
#       "Samoan",
#       "Spanish",
#       "Tamil",
#       "Telugu",
#       "Tibetan",
#       "Turkish",
#       "Wolof"
#     ],
#     "subtitle": ["English (CC)"]
#   },
#   "allFilters": {
#     "audio": ["Audio Description"],
#     "type": ["Movie"],
#     "genre": [
#       "Action",
#       "Adventure",
#       "Biography",
#       "Comedy",
#       "Comedy drama",
#       "Crime drama",
#       "Dark comedy",
#       "Documentary",
#       "Drama",
#       "Family",
#       "Fantasy",
#       "Historical drama",
#       "Music",
#       "Musical comedy",
#       "Mystery",
#       "Rock",
#       "Romance",
#       "Romantic comedy",
#       "Thriller",
#       "War",
#       "Western"
#     ],
#     "language": [
#       "Arabic",
#       "Bengali",
#       "Czech",
#       "English",
#       "French",
#       "German",
#       "Greek",
#       "Hindi",
#       "Hungarian",
#       "Inuktitut",
#       "Italian",
#       "Japanese",
#       "Kannada",
#       "Korean",
#       "Kurdish",
#       "Latin",
#       "Malayalam",
#       "Mandarin Chinese",
#       "Marathi",
#       "Nepali",
#       "Portuguese",
#       "Punjabi",
#       "Russian",
#       "Samoan",
#       "Spanish",
#       "Tamil",
#       "Telugu",
#       "Tibetan",
#       "Turkish",
#       "Wolof"
#     ],
#     "subtitle": ["English (CC)"]
#   }
# }
