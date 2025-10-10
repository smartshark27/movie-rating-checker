import base64
import json
import requests

# This script fetches a list of media in a collection from the SBS On Demand catalogue.
# It uses the public API endpoint to retrieve collection data.

collection_urls = {
    "movies-all": "https://catalogue.pr.sbsod.com/collections/all-movies",
    "movies-recently-added": "https://catalogue.pr.sbsod.com/collections/recently-added-movies",
    "shows-bingeable-box-sets": "https://catalogue.pr.sbsod.com/collections/bingeable-box-sets",
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
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break

        data = response.json()

        if not data.get("items"):
            print("No more items found, stopping.")
            break

        media_list.extend(
            [
                {
                    "mediaType": get_media_type(item),
                    "title": item["title"],
                    "year": str(item["releaseYear"]) if "releaseYear" in item else None,
                    "sbsURL": get_media_url(item),
                }
                for item in data["items"]
            ]
        )

    print(f"Total media found: {len(media_list)}")
    return media_list


def get_media_type(media):
    entity_type = media["entityType"]
    if entity_type == "MOVIE":
        return "movie"
    elif entity_type == "TV_SERIES":
        return "show"
    else:
        print(f"Unknown entity type '{entity_type}' for item '{media['title']}'")
        return "unknown"


def get_media_url(media):
    media_type = get_media_type(media)
    if media_type == "movie":
        return (
            "https://www.sbs.com.au/ondemand/movie/"
            + media["slug"]
            + "/"
            + str(media["mpxMediaID"])
        )
    elif media_type == "show":
        return "https://www.sbs.com.au/ondemand/show/" + media["slug"]
    else:
        return None


if __name__ == "__main__":
    media_list = get_sbs_media_list()
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


# Sample show data structure from the API:
# {
#   "id": "d0254adb-3a04-5b11-a9b3-8102886dc367",
#   "entityType": "CURATED_COLLECTION",
#   "localeID": "en",
#   "title": "Bingeable Box Sets",
#   "description": "Make the time fly with full seasons of your favourite shows. There's a genre to match every mood. ",
#   "slug": "bingeable-box-sets",
#   "displayType": "16x9",
#   "layout": "GRID",
#   "images": [
#     {
#       "id": "2ace917e-6a2d-5a75-93bf-6370863623c8",
#       "category": "16:9|1920|1080|BANNER"
#     },
#     {
#       "id": "d4050124-1fe0-5f85-bfbd-308e1b50853b",
#       "category": "16:9|1920|1080|KEY_ART"
#     },
#     {
#       "id": "06c96524-2db5-546b-bee0-0bd46aa74cff",
#       "category": "1:1|700|700|MASK"
#     },
#     {
#       "id": "c5cdce49-94c6-5c7d-893b-2bc4b798fadf",
#       "category": "2:3|960|1440|BANNER"
#     },
#     {
#       "id": "c5cdce49-94c6-5c7d-893b-2bc4b798fadf",
#       "category": "2:3|960|1440|KEY_ART"
#     }
#   ],
#   "items": [
#     {
#       "id": "c0ee228a-28c6-5a84-a6e5-053d0044f4cb",
#       "entityType": "TV_SERIES",
#       "title": "The People vs Robodebt",
#       "slug": "the-people-vs-robodebt",
#       "description": "Uncovers the human story of the notorious robodebt scandal and the Australians who took a stand.",
#       "genres": ["Documentary", "Docudrama"],
#       "languages": ["English"],
#       "textTracks": [
#         { "localeID": "ko", "language": "한국어", "type": "SUBTITLE" },
#         { "localeID": "vi", "language": "Tiếng Việt", "type": "SUBTITLE" },
#         { "localeID": "zh-Hans", "language": "简体中文", "type": "SUBTITLE" },
#         { "localeID": "ar", "language": "العربية", "type": "SUBTITLE" },
#         { "localeID": "zh-Hant", "language": "繁體中文", "type": "SUBTITLE" },
#         { "localeID": "en", "language": "English", "type": "CAPTION" }
#       ],
#       "availability": {
#         "start": "2025-09-23T16:00:00Z",
#         "end": "2030-09-23T12:59:59Z"
#       },
#       "hasAudioDescription": true,
#       "classificationID": "M",
#       "images": [
#         {
#           "id": "af171460-8e8e-5de0-9020-f77454b64fbc",
#           "category": "16:9|1920|1080|BANNER"
#         }
#       ],
#       "distributors": [
#         { "id": "20864", "name": "Cjz (Cordell Jigsaw Zapruder)" }
#       ],
#       "seasonCount": 1,
#       "featured": {
#         "id": "f1a79dc3-a39d-5f29-b540-e4fb5c5309b3",
#         "entityType": "TV_EPISODE",
#         "tagLine": "Start Here",
#         "title": "Episode 1",
#         "description": "When two young Australians suddenly receive debt letters demanding they pay Centrelink thousands of dollars, they don’t realise they’re caught up in what will become one of the biggest scandals in Australian history – Robodebt.",
#         "duration": "PT53M3S",
#         "availability": {
#           "start": "2025-09-23T16:00:00Z",
#           "end": "2030-09-23T12:59:59Z"
#         },
#         "hasAudioDescription": false,
#         "mpxMediaID": 2448763971866,
#         "images": [
#           {
#             "id": "29f5a463-3431-5204-805b-5f4523023d1c",
#             "category": "16:9|3840|2160|KEY_ART"
#           }
#         ]
#       }
#     }
#   ],
#   "trailers": [],
#   "meta": {
#     "nextCursor": "eyJhdWRpbyI6IiIsImdlbnJlIjoiIiwibGFuZ3VhZ2UiOiIiLCJsaW1pdCI6IjEiLCJwYWdlIjoiMiIsInNvcnQiOiIiLCJzdWJ0aXRsZSI6IiIsInR5cGUiOiIifQ==",
#     "count": 1,
#     "total": 101
#   },
#   "filters": {
#     "audio": ["Audio Description"],
#     "type": ["TV Show"],
#     "genre": [
#       "Action",
#       "Adventure",
#       "Animated",
#       "Biography",
#       "Comedy",
#       "Comedy drama",
#       "Competition reality",
#       "Cooking",
#       "Crime",
#       "Crime drama",
#       "Dark comedy",
#       "Docudrama",
#       "Documentary",
#       "Drama",
#       "Fantasy",
#       "Historical drama",
#       "History",
#       "Horror",
#       "Miniseries",
#       "Music",
#       "Musical",
#       "Mystery",
#       "Nature",
#       "Outdoors",
#       "Politics",
#       "Pro wrestling",
#       "Romance",
#       "Science fiction",
#       "Sitcom",
#       "Thriller",
#       "Travel",
#       "War",
#       "Western"
#     ],
#     "language": [
#       "Danish",
#       "Dutch",
#       "English",
#       "Finnish",
#       "French",
#       "German",
#       "Icelandic",
#       "Italian",
#       "Norwegian",
#       "Polish",
#       "Spanish",
#       "Swedish"
#     ],
#     "subtitle": [
#       "English (CC)",
#       "Tiếng Việt",
#       "العربية",
#       "हिन्दी",
#       "简体中文",
#       "繁體中文",
#       "한국어"
#     ]
#   },
#   "allFilters": {
#     "audio": ["Audio Description"],
#     "type": ["TV Show"],
#     "genre": [
#       "Action",
#       "Adventure",
#       "Animated",
#       "Biography",
#       "Comedy",
#       "Comedy drama",
#       "Competition reality",
#       "Cooking",
#       "Crime",
#       "Crime drama",
#       "Dark comedy",
#       "Docudrama",
#       "Documentary",
#       "Drama",
#       "Fantasy",
#       "Historical drama",
#       "History",
#       "Horror",
#       "Miniseries",
#       "Music",
#       "Musical",
#       "Mystery",
#       "Nature",
#       "Outdoors",
#       "Politics",
#       "Pro wrestling",
#       "Romance",
#       "Science fiction",
#       "Sitcom",
#       "Thriller",
#       "Travel",
#       "War",
#       "Western"
#     ],
#     "language": [
#       "Danish",
#       "Dutch",
#       "English",
#       "Finnish",
#       "French",
#       "German",
#       "Icelandic",
#       "Italian",
#       "Norwegian",
#       "Polish",
#       "Spanish",
#       "Swedish"
#     ],
#     "subtitle": [
#       "English (CC)",
#       "Tiếng Việt",
#       "العربية",
#       "हिन्दी",
#       "简体中文",
#       "繁體中文",
#       "한국어"
#     ]
#   }
# }
