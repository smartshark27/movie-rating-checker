import requests

MAX_PAGES = 20  # Maximum number of pages to fetch

url = "https://10.com.au/api/shows"
collection_genre_ids = {
    "movies": "61761",  # "https://10.com.au/shows/movie",
    "shows-comedy": "23547",  # "https://10.com.au/shows/comedy"
    "shows-drama": "23552",  # "https://10.com.au/shows/drama"
    "shows-kids": "23833",  # "https://10.com.au/shows/kids"
}


def get_10play_media_list(collection="shows-drama"):
    """
    Fetch all media from a collection from the 10 Play catalogue.
    """
    if collection not in collection_genre_ids:
        raise ValueError(
            f"Invalid collection '{collection}'. Must be one of {list(collection_genre_ids.keys())}."
        )
    genre_id = collection_genre_ids[collection]

    params = {
        "skipIdList": "",
        "genreId": genre_id,
        "sort": "popular",
        "sortDirection": "descending",
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-AU,en;q=0.9",
        "Priority": "u=3, i",
        "Referer": "https://10.com.au/shows/drama",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0",
    }

    media_list = []
    for i in range(MAX_PAGES):
        print(f"Fetching page {i}...")
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()

            if "items" in data:
                media_list.extend(
                    [
                        {
                            "mediaType": get_media_type(item),
                            "title": item["name"],
                            "10PlayURL": item["url"],
                        }
                        for item in data["items"]
                    ]
                )

            ids = [str(item["id"]) for item in data["items"]]
            params["skipIdList"] += "," if params["skipIdList"] else ""
            params["skipIdList"] += ",".join(ids)

            if not data.get("hasMore", False):
                print(f"No more pages after page {i}.")
                break
        else:
            print(f"Failed to fetch page {i}. Status code: {response.status_code}")
            raise ConnectionError("Failed to fetch 10play collection page")

    print(f"Total media found from 10 Play: {len(media_list)}")
    return media_list


def get_media_type(item):
    """
    Determine the media type (movie or show) from a 10 Play item.
    """
    return "movie" if item["type"] else "show"


if __name__ == "__main__":
    media_list = get_10play_media_list()
    print("media:", media_list)


# Example API response structure:
# {
#     "hasMore": true,
#     "items": [
#         {
#             "id": 1396951,
#             "epgData": {
#                 "seriesCridId": [
#                     "83520"
#                 ]
#             },
#             "tpId": "MTU5NjkzMQ==",
#             "name": "Curfew",
#             "url": "https://10.com.au/curfew",
#             "genres": [
#                 "Drama"
#             ],
#             "genreDisplayNames": [
#                 ""
#             ],
#             "secondaryGenres": [],
#             "poster": {
#                 "url": "https://10.com.au/ip/s3/2025/10/13/f02b2814473fc6694a71bef0f0db732a-1396957.jpg?image-profile=image_poster&io=portrait",
#                 "retinaUrl": "https://10.com.au/ip/s3/2025/10/13/f02b2814473fc6694a71bef0f0db732a-1396957.jpg?image-profile=image_poster&io=portrait&dpr=2",
#                 "lazyLoad": true,
#                 "alt": null,
#                 "placeholderUrl": "/images/Placeholder-Poster-193x293.png"
#             },
#             "landscape": {
#                 "url": "https://10.com.au/ip/s3/2025/10/13/3463c17688780481b2231d5a3f4b3df4-1396955.jpg?image-profile=image_full&io=landscape",
#                 "retinaUrl": "https://10.com.au/ip/s3/2025/10/13/3463c17688780481b2231d5a3f4b3df4-1396955.jpg?image-profile=image_full&io=landscape&dpr=2",
#                 "lazyLoad": true,
#                 "alt": null,
#                 "placeholderUrl": "/images/Placeholder-Full-1024x577.png"
#             },
#             "showRatingClassification": "None",
#             "aliases": [],
#             "hiddenFeatures": {
#                 "search": false,
#                 "autoSurfacing": false,
#                 "footerLinks": false,
#                 "showsIndex": false
#             },
#             "adOpsInformation": {
#                 "showNameTargeting": "curfew"
#             },
#             "videoCount": {
#                 "episodesCount": 6,
#                 "extrasCount": 0,
#                 "otherCount": 0
#             },
#             "type": "standard"
#         }
#     ]
# }
